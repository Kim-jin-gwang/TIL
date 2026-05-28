from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pendulum

# 기본 DAG 설정 (default_args 딕셔너리 설정)
default_args = {
    "start_date": pendulum.datetime(2026, 5, 19, tz="Asia/Seoul"),  # DAG의 시작 날짜 설정(최신으로 지정)
}

# DAG 객체 생성
dag = DAG(
    "bash_process_dag",  # DAG의 이름
    default_args=default_args,  # 위에서 설정한 기본 인자값 사용
    description="DAG to process using Bash script",  # DAG에 대한 간략한 설명
)

# BashOperator Task 정의
process_csv_task = BashOperator(
    task_id="process_csv_shell_task",  # 태스크의 고유 ID
    bash_command="/opt/airflow/plugins/shell/process_csv.sh ",  # 실행할 Bash 스크립트 'process_csv.sh' 경로
    dag=dag,  # DAG에 태스크 추가
)

# DAG 실행 순서 정의 (현재는 단일 태스크이므로 추가 연결 불필요)
process_csv_task # Airflow에서 실행될 태스크

