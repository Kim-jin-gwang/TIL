import os

from pyflink.table import EnvironmentSettings, TableEnvironment


# 1. 환경 설정
env_settings = EnvironmentSettings.in_batch_mode()
t_env = TableEnvironment.create(environment_settings=env_settings)


# 2. 경로 설정
input_path = "input/online_sales_clean.csv"
output_path = "output/sales_summary.csv"

os.makedirs(os.path.dirname(output_path), exist_ok=True)


# 기존 테이블 제거
# 같은 이름의 테이블이 이미 있을 경우 재실행 오류를 방지하기 위한 처리
t_env.execute_sql("DROP TABLE IF EXISTS sales")
t_env.execute_sql("DROP TABLE IF EXISTS sales_summary")


# 3. 소스 테이블 생성
# 전처리된 CSV 파일을 Flink Table API에서 읽을 수 있도록 테이블로 등록
t_env.execute_sql(
    f"""
    CREATE TABLE sales (
        InvoiceNo STRING,
        StockCode STRING,
        Description STRING,
        Quantity DOUBLE,
        InvoiceDate STRING,
        UnitPrice DOUBLE,
        CustomerID DOUBLE,
        Country STRING,
        Discount DOUBLE,
        PaymentMethod STRING,
        ShippingCost DOUBLE,
        Category STRING,
        SalesChannel STRING,
        ReturnStatus STRING,
        ShipmentProvider STRING,
        WarehouseLocation STRING,
        OrderPriority STRING
    ) WITH (
        'connector' = 'filesystem',
        'path' = '{input_path}',
        'format' = 'csv',
        'csv.ignore-parse-errors' = 'true'
    )
    """
)


# 4. 집계 쿼리 실행
# Category별 매출 합계를 계산
result = t_env.sql_query(
    """
    SELECT
        Category,
        ROUND(COALESCE(SUM(Quantity * UnitPrice), 0.0), 2) AS TotalSales
    FROM sales
    GROUP BY Category
    """
)


# 5. 결과 테이블 생성
# 집계 결과를 CSV 파일로 저장하기 위한 Sink 테이블
t_env.execute_sql(
    f"""
    CREATE TABLE sales_summary (
        Category STRING,
        TotalSales DOUBLE
    ) WITH (
        'connector' = 'filesystem',
        'path' = '{output_path}',
        'format' = 'csv',
        'sink.parallelism' = '1'
    )
    """
)


# 6. 결과 저장
# execute_insert()는 Flink Job을 실행하여 결과를 Sink 테이블에 기록
result.execute_insert("sales_summary").wait()

print("매출 요약 CSV 저장 완료:", output_path)
