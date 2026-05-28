from airflow import DAG  # DAG 생성을 위한 기본 클래스
from airflow.operators.empty import EmptyOperator  # 실행할 작업이 없는 빈 태스크
import pendulum  # 시간대 설정을 위한 라이브러리

# DAG 정의 (이 DAG는 Scheduler, Worker가 정상 작동하는지 확인하는 역할을 합니다.)
with DAG(
    dag_id="test_airflow_components",  # DAG의 이름
    start_date=pendulum.datetime(2026, 5, 19, tz="Asia/Seoul"),  # DAG 시작 날짜 (2026년 5월 19일)
    tags=["test", "health_check"],  # DAG 태그 (Airflow UI에서 관리 용이) - 원하는 내용 입력
) as dag:

    # DAG 시작과 끝을 나타내는 빈 태스크 생성
    start = EmptyOperator(task_id="start")  # 시작 태스크
    check_scheduler = EmptyOperator(task_id="check_scheduler")  # 스케줄러 확인 태스크
    check_worker = EmptyOperator(task_id="check_worker")  # 워커 확인 태스크
    end = EmptyOperator(task_id="end")  # 종료 태스크

    # 실행 순서 설정 (start → check_scheduler & check_worker → end)
    start >> [check_scheduler, check_worker] >> end