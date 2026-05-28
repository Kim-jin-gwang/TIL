from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
from datetime import datetime
import pendulum

# Task 1: CSV 데이터 읽기
def download_data():
    df = pd.read_csv("dags/input_data.csv")
    print("데이터 로드 완료")
    return df.to_dict()

# Task 2: 데이터 처리 (old_column 삭제, age_group 추가)
def process_data(**kwargs):
    ti = kwargs['ti']
    data_dict = ti.xcom_pull(task_ids="download_data")        # TODO: 바로 이전 데이터 로드 태스크의 ID 문자열
    df = pd.DataFrame(ti)                          # TODO: 위에서 가져온 dict 객체 변수

    df = df.drop(columns=["old_column"])                   # TODO: CSV에서 제거할 실제 컬럼명
    df["age_group"] = df["age"].apply(             # TODO: 나이 값이 들어있는 실제 컬럼명
        lambda x: "Young" if x < 30 else "Adult"
    )
    print("데이터 처리 완료")

    ti.xcom_push(key="processed_data_key", value=df.to_dict())     # TODO: 다음 단계에서 사용할 XCom key 문자열

# Task 3: 데이터 저장 (파일 저장)
def store_data(**kwargs):
    ti = kwargs['ti']
    records = ti.xcom_pull(task_ids="process_data", key="processed_data_key")  # TODO: 전처리 태스크 ID / 위에서 정한 XCom key
    df = pd.DataFrame(records)

    output_path = "dags/output_data.csv"              # TODO: 필요 시 저장 경로 조정
    df.to_csv(output_path, index=False)
    print(f"파일 저장 완료: {output_path}")

# DAG 정의
dag = DAG(
    "csv_complex_process_dag",                     # TODO: DAG ID (문자열)
    schedule_interval="@daily",   # TODO: 스케줄 문자열 (예: 크론/프리셋 형식)
    start_date=pendulum.datetime(2026, 5, 19, tz="Asia/Seoul"),  # TODO: pendulum 형태의 시작일
    catchup=False                # TODO: 소급 실행 여부 (True/False)
)

# Task 정의
task_1 = PythonOperator(task_id="download_data", python_callable=download_data, dag=dag)
task_2 = PythonOperator(task_id="process_data",  python_callable=process_data,  dag=dag)
task_3 = PythonOperator(task_id="store_data",    python_callable=store_data,    dag=dag)

# 실행 순서
task_1 >> task_2 >> task_3          # TODO: 위에서 만든 task_1 → task_2 → task_3 순으로 연결


#  로그 경로 참고:
# CLI 환경 또는 서버에서 로그 파일은 일반적으로 다음 경로에 저장됨:
# logs/<dag_id>/<run_id>/<task_id>/<execution_date>/ 폴더 구조로 저장되며,
# 이 구조 덕분에 DAG 이름과 Task 이름으로 로그를 쉽게 확인 가능함.
