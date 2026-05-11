from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

import os
import time
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Flink 작업 시작...")
    
    # DataStream 실행 환경 생성
    # Table API/SQL로 작성한 쿼리도 최종적으로는 Flink 스트리밍 Job으로 실행됩니다.
    env = StreamExecutionEnvironment.get_execution_environment()

    # Table API 실행 모드를 Streaming으로 설정합니다.
    # Kafka topic은 계속 데이터가 들어오는 unbounded source이므로 streaming mode가 적합합니다.
    # StreamTableEnvironment는 DataStream 실행 환경 위에서 Table API/SQL을 실행할 때 사용합니다.
    env_settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    table_env = StreamTableEnvironment.create(env, environment_settings=env_settings)
    
    # Flink Job에 전달할 전역 파라미터 예시입니다.
    # Python logging.basicConfig나 Flink Log4j 로그 레벨을 직접 바꾸는 설정은 아닙니다.
    table_env.get_config().get_configuration().set_string("pipeline.global-job-parameters.logger.level", "INFO")
    
    # Kafka SQL connector JAR 등록
    # Table API에서 'connector' = 'kafka', 'upsert-kafka'를 사용하려면 connector JAR가 필요합니다.
    kafka_jar = os.path.join(os.path.abspath('.'), 'flink-sql-connector-kafka-3.3.0-1.19.jar')
    logger.info(f"사용하는 JAR 파일 경로: {kafka_jar}")
    if not os.path.exists(kafka_jar):
        logger.error(f"JAR 파일이 존재하지 않습니다: {kafka_jar}")
        return
    
    table_env.get_config().get_configuration().set_string("pipeline.jars", f"file://{kafka_jar}")
    
    # Kafka source table 정의
    # user_behaviors topic의 JSON 메시지를 Flink SQL에서 조회 가능한 동적 테이블로 매핑합니다.
    # proctime은 실제 Kafka 메시지 필드가 아니라, Flink가 처리 시각 기준으로 생성하는 processing-time 컬럼입니다.
    try:
        logger.info("Kafka 소스 테이블 생성 시도...")
        table_env.execute_sql("""
        CREATE TABLE kafka_source (
            user_id STRING,
            item_id STRING,
            category STRING,
            behavior STRING,
            ts TIMESTAMP(3),
            proctime AS PROCTIME()
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'user_behaviors',
            'properties.bootstrap.servers' = 'localhost:9092',
            'properties.group.id' = 'flink-consumer-group',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json',
            'json.fail-on-missing-field' = 'false',
            'json.ignore-parse-errors' = 'true'
        )
        """)
        logger.info("Kafka 소스 테이블 생성 성공")
    except Exception as e:
        logger.error(f"소스 테이블 생성 중 오류 발생: {e}")
        return
    
    # Kafka sink table 정의
    # GROUP BY 집계 결과는 같은 key의 count가 계속 바뀌는 update stream입니다.
    # 일반 kafka sink는 update/delete 변경 로그를 처리할 수 없으므로 upsert-kafka sink를 사용합니다.
    # PRIMARY KEY는 upsert 메시지의 key가 되며, 같은 (category, behavior)의 최신 집계값을 덮어씁니다.
    try:
        logger.info("Kafka 싱크 테이블 생성 시도...")
        table_env.execute_sql("""
        CREATE TABLE kafka_sink (
            category STRING,
            behavior STRING,
            behavior_count BIGINT,
            update_time TIMESTAMP(3),
            PRIMARY KEY (category, behavior) NOT ENFORCED
        ) WITH (
            'connector' = 'upsert-kafka',
            'topic' = 'behavior_stats',
            'properties.bootstrap.servers' = 'localhost:9092',
            'key.format' = 'json',
            'value.format' = 'json',
            'properties.group.id' = 'flink-sink-group'
        )
        """)
        logger.info("Kafka 싱크 테이블 생성 성공")
    except Exception as e:
        logger.error(f"싱크 테이블 생성 중 오류 발생: {e}")
        return
    
    # SQL 쿼리 등록 및 작업 제출
    try:
        logger.info("SQL 쿼리 실행 시도...")
        stmt_set = table_env.create_statement_set()
        stmt_set.add_insert_sql("""
        INSERT INTO kafka_sink
        SELECT 
            category,
            behavior,
            COUNT(*) AS behavior_count,
            CURRENT_TIMESTAMP as update_time
        FROM kafka_source
        GROUP BY category, behavior
        """)
        # 위 쿼리는 스트리밍 상태 기반 집계입니다.
        # Flink는 (category, behavior)를 key로 나누고, 각 key별 COUNT 값을 내부 keyed state에 저장합니다.
        # 새 이벤트가 들어오면 해당 key의 count state를 읽고 증가시킨 뒤, 갱신된 결과를 upsert-kafka로 내보냅니다.
        
        # 작업 실행 및 JobClient 가져오기
        job_client = stmt_set.execute().get_job_client()
        
        if job_client:
            job_id = job_client.get_job_id()
            logger.info(f"작업이 성공적으로 제출되었습니다. 작업 ID: {job_id}")
            
            # 작업 상태 확인
            monitor_job(job_client)
        else:
            logger.error("작업 클라이언트를 가져올 수 없습니다.")
    except Exception as e:
        logger.error(f"작업 실행 중 오류 발생: {e}")

def monitor_job(job_client):
    """작업 상태에 대한 로그를 출력합니다."""
    try:
        # 작업 상태 확인
        # Flink Job 상태 값
        # RUNNING    : Flink 작업이 현재 실행 중
        # FINISHED   : 작업이 성공적으로 완료됨
        # FAILED     : 작업 실패
        # CANCELED   : 작업이 중단됨
        # RESTARTING : 작업이 재시작 중
        
        job_status = job_client.get_job_status().result()

        logger.info(f"현재 작업 상태: {job_status}")
        
        # 샘플 데이터 생성 안내입니다. 이 코드는 Kafka topic 내용을 직접 조회하지 않습니다.
        logger.info("Kafka 토픽에 샘플 데이터가 있는지 확인해주세요.")
        logger.info("샘플 데이터가 없다면 kafka_producer.py를 실행하여 테스트 데이터를 생성하세요.")
        
        # 작업 실행 중 상태 확인
        print("\n작업 확인 시작 (10초마다 상태 확인, Ctrl+C로 종료)")
        for i in range(6):  # 60초 동안 확인
            time.sleep(10)
            try:
                current_status = job_client.get_job_status().result()
                print(f"[{i+1}/6] 현재 작업 상태: {current_status}")
                
                # 선택적: 작업 메트릭스 확인 (PyFlink API가 지원하는 경우)
                # 이 부분은 PyFlink 버전에 따라 다를 수 있습니다
                if hasattr(job_client, 'get_job_metrics'):
                    metrics = job_client.get_job_metrics()
                    print(f"작업 메트릭스: {metrics}")
            except Exception as e:
                print(f"상태 확인 중 오류 발생: {e}")
        
        print("\n확인 완료. 작업은 계속 실행 중입니다.")
        print("결과를 확인하려면 다음 명령어를 실행하세요:")
        print("kafka-console-consumer().sh) --topic behavior_stats --bootstrap-server localhost:9092 --from-beginning")
        
    except Exception as e:
        logger.error(f"작업 확인 중 오류 발생: {e}")

if __name__ == '__main__':
    main()
    
