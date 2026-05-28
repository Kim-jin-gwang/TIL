from airflow import DAG
from airflow.decorators import task
import pendulum

# 데이터를 반환하는 @task 데코레이터를 사용한 함수
@task
def get_data():
    return "some_value"

# 반환된 데이터를 처리하는 @task 데코레이터를 사용한 함수
@task
def consume(data):
    print(f"Received data: {data}")

default_args = {
    'owner': 'airflow',
    'start_date': pendulum.datetime(2026, 5, 19, tz="Asia/Seoul"),
}

with DAG('xcom_task_decorator_example', default_args=default_args, schedule_interval=None) as dag:
    # @task 데코레이터를 사용한 함수 호출
    data = get_data()  # 'some_value'가 자동으로 XCom에 저장됨
    consume_task = consume(data)  # XCom에서 'some_value'를 가져와 처리

    # 데이터 흐름을 정의 (Task 객체로 연결)
    data >> consume_task
