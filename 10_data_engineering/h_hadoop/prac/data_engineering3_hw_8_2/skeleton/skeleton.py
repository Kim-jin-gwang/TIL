import time
import os
import shutil
from pyspark.sql import SparkSession

# Hdfs에 user/local/hadoop_data/transactions.csv 경로에 파일이 적재가 된 상태여야 합니다.

# SparkSession 생성
spark = SparkSession.builder \
    .appName("Read HDFS CSV") \
    .master("local[*]") \
    .getOrCreate()

# HDFS의 CSV 파일 읽기
df = spark.read.option("header", "true").csv("hdfs://namenode:9000/user/local/hadoop_data/transactions.csv")

# 데이터 출력 (검증용)
df.show()

# 필요한 컬럼만 선택
df_selected = df.select("transaction_date", "amount")

# 로컬 디스크에 CSV로 저장 (Spark는 디렉토리 + part 파일 형태로 저장)
output_dir = "/tmp/hadoop_data/transactions"
final_file = "/tmp/hadoop_data/transactions.csv"

df_selected.write.mode("overwrite").option("header", "true").csv(f"file://{output_dir}")

# 저장 완료될 때까지 대기
time.sleep(2)

# part 파일을 찾아 단일 파일로 rename
files = os.listdir(output_dir)
for f in files:
    if f.startswith("part-") and f.endswith(".csv"):
        shutil.move(os.path.join(output_dir, f), final_file)

# 디렉토리 정리 (선택 사항)
for f in os.listdir(output_dir):
    path = os.path.join(output_dir, f)
    if os.path.isfile(path):
        os.remove(path)
os.rmdir(output_dir)

print(f"저장 완료: {final_file}")
