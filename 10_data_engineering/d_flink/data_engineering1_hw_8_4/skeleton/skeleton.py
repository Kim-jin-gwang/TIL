# 실습 힌트
# - 목표: PyFlink Table API 배치 모드에서 제공 CSV를 테이블로 만들고 섹터별 집계를 SQL로 실행합니다.
# - input_path는 data/finance_data.csv를 가리키며, 임시 샘플 데이터는 생성하지 않습니다.
# - (1)은 파일 시스템 CSV를 finance 테이블로 등록하는 CREATE TABLE 문입니다.
# - (2)는 finance 테이블에서 sector별 총 거래액, 평균 가격, 총 거래량, 거래 건수를 구하는 SELECT 문입니다.
# - result.collect()로 출력하므로 INSERT 쿼리가 아니라 SELECT 쿼리를 작성하세요.

# TODO 안내
# - CREATE TABLE은 finance 이름과 finance_data.csv 컬럼 순서를 맞춥니다.
# - price와 volume은 집계 가능한 숫자 타입으로 선언합니다.
# - SELECT는 sector로 그룹화하고 총 거래액(price * volume), 평균 price, 총 volume, 거래 건수를 출력합니다.

from pyflink.table import EnvironmentSettings, TableEnvironment
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_float(value):
    """집계 결과가 비어 있거나 파싱 실패로 None이 들어와도 출력이 깨지지 않게 처리합니다."""
    return "N/A" if value is None else f"{float(value):,.2f}"

def format_int(value):
    """정수 집계 결과를 천 단위 구분자로 출력합니다."""
    return "N/A" if value is None else f"{int(value):,}"

def main():
    logger.info("Flink 배치 처리 시작")

    env_settings = EnvironmentSettings.in_batch_mode()
    table_env = TableEnvironment.create(env_settings)

    config = table_env.get_config().get_configuration()
    config.set_string("parallelism.default", "1")

    # 제공된 실습 CSV 파일 경로
    # __file__ 기준으로 경로를 만들면 answer/skeleton 어느 위치에서 실행해도 data 파일을 안정적으로 찾습니다.
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, "data", "finance_data.csv")

    # TODO (1): 소스 테이블 정의
    # - 테이블 이름은 finance로 만듭니다.
    # - finance_data.csv의 컬럼 순서에 맞춰 5개 필드를 선언합니다.
    #   stock_code, sector, price, volume, transaction_date
    # - 집계 계산에 쓰는 price와 volume은 숫자 타입으로 선언해야 합니다.
    # - WITH 절에서는 filesystem connector, path=input_path, csv format을 사용합니다.
    # - CSV에 헤더가 추가되어도 숫자 파싱 실패로 전체 실행이 멈추지 않게 parse error 무시 옵션을 포함합니다.
    source_ddl = f"""
        CREATE TABLE finance(
            stock_code STRING,
            sector STRING,
            price DOUBLE,
            volume BIGINT,
            transaction_date STRING
        ) WITH (
            'connector' = 'filesystem',
            'path'='{input_path}',
            'format'='csv',
            'csv.ignore-parse-errors'='true'
        )
"""
    table_env.execute_sql(source_ddl)

    # TODO (2): SQL 쿼리 작성 및 실행
    # - FROM 대상은 위에서 만든 finance 테이블입니다.
    # - 그룹화 기준은 sector 하나입니다.
    # - 출력 컬럼 순서는 아래 print 형식과 맞춰야 합니다.
    #   1) sector
    #   2) price * volume의 합계
    #   3) price의 평균
    #   4) volume의 합계
    #   5) 거래 건수
    # - 컬럼 별칭은 출력 row 인덱스에는 영향이 없지만, 의미가 드러나도록 작성하세요.
    result = table_env.execute_sql("""
        SELECT 
            sector, 
            SUM(price * volume) AS total_amount,
            AVG(price) AS avg_price,
            SUM(volume) AS total_volume,
            COUNT(*) AS transaction_count
        FROM finance
        GROUP BY sector
    """)

    print("\n=== 섹터별 금융 데이터 요약 ===")
    print("섹터\t총 거래액\t평균 가격\t총 거래량\t거래 건수")
    print("-" * 80)

    with result.collect() as results:
        for row in results:
            print(
                f"{row[0]}\t"
                f"{format_float(row[1])}\t"
                f"{format_float(row[2])}\t"
                f"{format_int(row[3])}\t"
                f"{format_int(row[4])}"
            )

if __name__ == '__main__':
    main()
