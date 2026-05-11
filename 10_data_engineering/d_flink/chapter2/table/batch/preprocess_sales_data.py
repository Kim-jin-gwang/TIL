import os

import pandas as pd


# 1. CSV 읽기
input_path = "input/online_sales_dataset.csv"
output_path = "input/online_sales_clean.csv"

df = pd.read_csv(input_path)


# 2. 수치형 컬럼 강제 변환 및 결측치 채우기
numeric_cols = [
    "Quantity",
    "UnitPrice",
    "ShippingCost",
    "CustomerID",
    "Discount",
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)


# 3. 필터링
# - Quantity, UnitPrice는 양수인 데이터만 사용
# - ShippingCost, CustomerID, Discount, Category는 결측이 아닌 데이터만 사용
df = df[
    (df["Quantity"] > 0)
    & (df["UnitPrice"] > 0)
    & df["ShippingCost"].notna()
    & df["CustomerID"].notna()
    & df["Discount"].notna()
    & df["Category"].notna()
]


# 4. 문자열 정리 및 타입 정리
df["Category"] = df["Category"].astype(str).str.strip()
df[numeric_cols] = df[numeric_cols].astype(float)


# 5. 컬럼 순서 고정
# Flink에서 읽을 스키마와 CSV 컬럼 순서를 맞추기 위한 처리
final_cols = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
    "Discount",
    "PaymentMethod",
    "ShippingCost",
    "Category",
    "SalesChannel",
    "ReturnStatus",
    "ShipmentProvider",
    "WarehouseLocation",
    "OrderPriority",
]

df = df[final_cols]


# 6. 저장
os.makedirs(os.path.dirname(output_path), exist_ok=True)

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8",
    float_format="%.2f",
)

print("정제된 CSV 저장 완료:", output_path)
