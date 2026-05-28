from airflow.decorators import task, dag
import pendulum

# DAG 정의
@dag(schedule_interval="@daily", start_date=pendulum.datetime(2026, 5, 19, tz="Asia/Seoul"))
def example_dag():
    
    # @task 데코레이터로 Airflow 태스크로 변환
    @task
    def extract_data():
        print("Extracting data...")
        return "raw_data"
    
    @task
    def transform_data(data):
        print(f"Transforming data: {data}")
        return f"transformed_{data}"
    
    @task
    def load_data(data):
        print(f"Loading data: {data}")
        return f"loaded_{data}"

    # 태스크 간 의존성 설정
    data = extract_data()  # 첫 번째 태스크
    transformed_data = transform_data(data)  # 두 번째 태스크
    load_data(transformed_data)  # 세 번째 태스크

# DAG 실행
example_dag()
