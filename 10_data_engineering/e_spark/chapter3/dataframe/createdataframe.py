from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("create_order_dataframe_example") \
    .getOrCreate()

schema = """
    order_id STRING,
    customer_id STRING,
    order_date STRING,
    order_amount DOUBLE,
    payment_method STRING,
    category STRING
"""

data = [
    ("O00001", "C0001", "2026-01-05", 32000.0, "CARD", "book"),
    ("O00002", "C0002", "2026-01-06", 18000.0, "CASH", "food"),
    ("O00003", "C0001", "2026-01-07", 54000.0, "CARD", "electronics")
]

order_df = spark.createDataFrame(
    data=data,
    schema=schema
)

order_df.show()
order_df.printSchema()

