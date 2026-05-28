from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum

def extract_data():
    print("Extracting data...")
    return "raw_data"

def transform_data(data):
    print(f"Transforming data: {data}")
    return f"transformed_{data}"

def load_data(data):
    print(f"Loading data: {data}")
    # 데이터 로딩 예시
    return f"loaded_{data}"

# DAG 정의
with DAG(dag_id="example_dag", schedule_interval="@daily", start_date=pendulum.datetime(2026, 5, 19, tz="Asia/Seoul")) as dag:
    
    # PythonOperator를 사용하여 각 태스크를 명시적으로 정의
    extract_task = PythonOperator(task_id="extract_data", python_callable=extract_data)
    transform_task = PythonOperator(task_id="transform_data", python_callable=transform_data, op_args=["{{ task_instance.xcom_pull(task_ids='extract_data') }}"])
    load_task = PythonOperator(task_id="load_data", python_callable=load_data, op_args=["{{ task_instance.xcom_pull(task_ids='transform_data') }}"])

    # 태스크 간 의존성 설정
    extract_task >> transform_task >> load_task
