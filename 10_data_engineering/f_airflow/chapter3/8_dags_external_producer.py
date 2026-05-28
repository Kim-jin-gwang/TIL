from airflow import DAG
from airflow.operators.empty import EmptyOperator
import pendulum

dag_a = DAG(
    dag_id="dag_a",
    start_date=pendulum.datetime(2026, 5, 19, tz="Asia/Seoul"),
)

task_a = EmptyOperator(
    task_id="task_a",
    dag=dag_a
)

