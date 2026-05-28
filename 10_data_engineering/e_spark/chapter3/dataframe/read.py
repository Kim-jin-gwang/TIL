from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("read_load_example") \
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
    .format("csv") \
    .option("header", True) \
    .option("delimiter", ",") \
    .schema(order_schema) \
    .load("data/input/order_history.csv")

order_df.show(10)

