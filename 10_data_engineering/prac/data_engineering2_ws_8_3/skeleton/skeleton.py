from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
from datetime import datetime
import pendulum

def download_data():
    df = pd.read_csv("dags/input_data.csv")
    print("데이터 로드 완료")
    return df.to_dict(orient="records")   # XCom으로 자동 전달

def process_data(**kwargs):
    records = kwargs["ti"].xcom_pull(task_ids="download_data")   # TODO: 이전 태스크 ID
    df = pd.DataFrame(records)
    df = df.drop(columns=["old_column"])
    df["age_group"] = df["age"].apply(lambda x: "Young" if x < 30 else "Adult")
    print("데이터 처리 완료")
    return df.to_dict(orient="records")

def store_data(**kwargs):
    records = kwargs["ti"].xcom_pull(task_ids="process_data", key="return_value")  # TODO: 이전 태스크 ID
    df = pd.DataFrame(records)
    output_path = "dags/output_data.csv"
    df.to_csv(output_path, index=False)
    print(f"파일 저장 완료: {output_path}")

# DAG 객체 생성
dag = DAG(
    dag_id="python_xcom_etl_dag",                        # TODO: DAG ID
    schedule_interval="@daily",             # TODO: 실행 주기 (예: @daily)
    start_date=pendulum.datetime(2026, 5, 19, tz="Asia/Seoul"),  # TODO: 시작 날짜 (예: 2026, 5, 19)
    catchup=False                          # TODO: True/False
)

# 태스크 정의
task_1 = PythonOperator(
    task_id="download_data",
    python_callable=download_data,
    dag=dag
)

task_2 = PythonOperator(
    task_id="process_data",
    python_callable=process_data,
    dag=dag
)

task_3 = PythonOperator(
    task_id="store_data",
    python_callable=store_data,
    dag=dag
)

# 태스크 실행 순서
task_1 >> task_2 >> task_3                