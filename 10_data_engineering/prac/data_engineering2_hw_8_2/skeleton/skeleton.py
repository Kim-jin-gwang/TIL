from airflow import DAG
from airflow.decorators import task
import pendulum
import pandas as pd
import os
from datetime import datetime

INPUT_DIR = "./data/input"
OUTPUT_DIR = "./data/output"

with DAG(
    dag_id="csv_folder_aggregate_dag_simple",  
    start_date=pendulum.datetime(2026, 5, 19, tz="Asia/Seoul"),  
    schedule="@daily",  
    # 조건: 매일 실행되는 스케줄을 지정하세요.
    catchup=False,  
    # 조건: 과거 실행 건 무시
) as dag:

    @task
    def collect_files():
        files = sorted([
            os.path.join(INPUT_DIR, f)
            for f in os.listdir(INPUT_DIR)
            if f.endswith(".csv")
        ])
        if not files:
            # 파일이 없어도 실패하지 않고 빈 리스트 반환
            return []
        return files

    @task
    def aggregate(files):
        if not files:
            # 입력이 없을 때는 컬럼만 있는 빈 CSV를 저장
            out_path = os.path.join(OUTPUT_DIR, "aggregated_empty.csv")
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            pd.DataFrame(columns=["date","product_id","total_qty","total_sales"]).to_csv(out_path, index=False)
            return out_path

        # 조건: 전달받은 모든 CSV 파일을 읽어와 하나의 DataFrame으로 합치세요.
        frames = [pd.read_csv(p) for p in files]
        df = pd.concat(frames, ignore_index=True)

        # 조건: qty * price 로 총액(total) 컬럼을 계산
        df["total"] = df["qty"] * df["price"]

        # 조건: date, product_id 기준으로 묶어 수량과 총액을 합계(sum)로 집계
        agg = (
            df.groupby(["date", "product_id"], as_index=False)
              .agg(total_qty=("qty", "sum"), total_sales=("total", "sum"))
              .sort_values(["date", "product_id"])
        )

        # 조건: 집계 결과를 aggregated.csv 파일로 저장
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        out_path = os.path.join(OUTPUT_DIR, f"aggregated.csv")
        agg.to_csv(out_path, index=False)
        return out_path

    aggregate(collect_files())
