from airflow import DAG
from airflow.operators.python import PythonOperator 
from datetime import datetime, timedelta
import pendulum
import pandas as pd

# CSV 파일 경로 설정 (DAG 파일과 동일한 경로에 존재한다고 가정 - 변경 자유롭게)
CSV_FILE_PATH = "./data/input_data.csv"
OUTPUT_FILE_PATH = "./data/output_data.csv"

# 데이터 변환을 수행하는 Python 함수 정의
def transform_csv():
    """
    CSV 파일을 읽어와서 데이터를 변환한 후, 새로운 CSV 파일로 저장하는 함수
    """
    # CSV 파일 읽기
    df = pd.read_csv(CSV_FILE_PATH)  # 파일 경로 
    
    # 데이터 변환 수행
    # 예제: 특정 컬럼명을 변경하고 새로운 컬럼 추가
    df.rename(columns={"old_column": "new_column"}, inplace=True)  # 변경할 컬럼명 
    df["processed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    
    # 변환된 데이터를 새로운 CSV 파일로 저장
    df.to_csv(OUTPUT_FILE_PATH, index=False)  # 저장할 파일 경로 
    print("Data transformation complete. Saved to", OUTPUT_FILE_PATH) 

# DAG의 기본 설정 지정
default_args = {
    "start_date": pendulum.datetime(2026, 5, 19, tz="Asia/Seoul"),   # DAG의 시작 날짜 설
    # 추가적인 설정 (예: retries, retry_delay 등)은 필요에 따라 추가할 수 있음
}

# DAG 생성 (Workflow 정의)
dag = DAG(
    dag_id="csv_transform_dag",  # DAG의 ID (이름) 
    default_args=default_args,  # 기본 인자 전달
    description="A simple CSV transformation DAG",  # DAG 설명을 통해 UI에 표시 확인 가능
    schedule=None,
)

# PythonOperator를 사용하여 transform_csv 함수를 Task로 등록
transform_task = PythonOperator(
    task_id="transform_task",  # Task ID 지정 
    python_callable=transform_csv,  # 실행할 Python 함수 
    dag=dag,  # 해당 Task가 속할 DAG 지정 
)

# DAG 내 Task 실행 순서 정의 (현재는 단일 Task이므로 순서 지정 불필요)
transform_task