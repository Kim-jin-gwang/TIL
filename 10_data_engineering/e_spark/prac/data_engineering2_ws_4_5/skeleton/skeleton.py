# Structured Streaming의 rate source로 계속 들어오는 데이터를 만들고 event-time window 집계를 수행하는 실습입니다.
# TODO에는 스트리밍 입력/출력 객체, source 이름, watermark, 집계 메서드, output mode를 채워 넣습니다.
from pyspark.sql import SparkSession
from pyspark.sql.functions import window

spark = (
    SparkSession.builder
    .appName("PracticeRateSourceWindow")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

stream_df = (
    spark
    .readStream
    .format("rate")
    .option("rowsPerSecond", 5)
    .load()
)
# 위 TODO 순서: 스트리밍 입력을 만드는 속성, 초당 행을 생성하는 내장 source 이름

result_df = (
    stream_df
    .withWatermark("timestamp", "1 minute")
    .groupBy(window("timestamp", "10 seconds"))
    .count()
)
# 위 TODO 순서: 이벤트 시간 지연 허용 기준을 설정하는 메서드, 10초 window 기준으로 묶는 메서드, window별 행 개수를 세는 메서드

query = (
    result_df
    .writeStream
    .outputMode("complete")
    .format("console")
    .option("truncate", "false")
    .start()
)
# 위 TODO 순서: 스트리밍 출력을 시작하는 속성, 집계 결과 전체를 매번 출력하는 output mode

query.awaitTermination()
