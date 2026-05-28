from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime
import pendulum

with DAG(
    dag_id='spark_submit_example',
    start_date=pendulum.datetime(2026, 5, 19, tz="Asia/Seoul"),
    schedule_interval=None,
    catchup=False,
    tags=['spark'],
) as dag:

    submit_job = SparkSubmitOperator(
        task_id='spark_submit_task',
        application='/opt/airflow/dags/scripts/spark_wordcount.py',
        conn_id='spark_default',
        conf={
            "spark.master": "spark://spark-master:7077",
            "spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version": "2",
            "spark.driver.extraJavaOptions": "-Duser.dir=/opt/bitnami/spark"

        },
        verbose=True,
    )
