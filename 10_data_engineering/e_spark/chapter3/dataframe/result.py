from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession \
    .builder \
    .appName("order_history_write_example") \
    .getOrCreate()

order_schema = """
    order_id STRING,
    customer_id STRING,
    order_date STRING,
    order_amount DOUBLE,
    payment_method STRING,
    category STRING
"""

order_df = spark.read \
    .option("header", True) \
    .schema(order_schema) \
    .csv("data/input/order_history.csv")

card_order_df = order_df.filter(col("payment_method") == "CARD")

card_order_df.write \
    .mode("overwrite") \
    .format("csv") \
    .save("data/output")

