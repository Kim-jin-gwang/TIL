# 실습 힌트
# - 목표: 외부 텍스트 파일을 RDD로 읽고 collect/count/filter/map/repartition을 연습합니다.
# - SparkSession 생성 후 sc = spark.sparkContext를 완성하세요.
# - contains_data는 line.lower()에 "data"가 포함되는지 확인하면 됩니다.
# - 실행 위치: skeleton 디렉터리에서 실행해야 ../data/test_1.txt 경로가 맞습니다.

# TODO 안내
# - SparkSession.builder.appName(...).getOrCreate()로 SparkSession을 생성합니다.
# - spark.sparkContext로 SparkContext를 가져옵니다.
# - data 포함 여부는 문자열 리터럴과 lower() 결과를 사용해 검사합니다.
# - 대문자/소문자 변환은 문자열 메서드를 사용합니다.
# - 파티션 개수 확인은 RDD의 파티션 수 조회 메서드를 사용하고, repartition에는 목표 파티션 수를 넣습니다.


from pyspark.sql import SparkSession

# SparkSession 생성
spark = SparkSession.builder.appName("TextDataAnalysis").getOrCreate()
sc = spark.sparkContext

# 텍스트 파일 로드
text_data = sc.textFile("../data/test_1.txt")

# 전체 텍스트 출력
print(text_data.collect())

# 줄 수 출력
print("전체 줄 개수:", text_data.count())

# 'data'가 포함된 문장 필터링
contains_data = text_data.filter(lambda line: 'data' in line.lower())
print(contains_data.collect())

# 포함된 줄 수 출력
print("전체 줄 개수:", contains_data.count())

# 대문자로 변환
upper_case_data = text_data.map(lambda line: line.upper())
print(upper_case_data.collect())

# 소문자로 변환
lower_case_data = text_data.map(lambda line: line.lower())
print(lower_case_data.collect())

# 기본 파티션 개수 확인
print("기본 파티션 개수:", text_data.getNumPartitions())

# 파티션 4개로 재설정 후 확인
repartitioned_data = text_data.repartition(4)
print("변경된 파티션 개수:", repartitioned_data.getNumPartitions())
