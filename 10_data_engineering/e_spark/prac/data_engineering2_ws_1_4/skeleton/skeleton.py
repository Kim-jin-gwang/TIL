# 실습 힌트
# - 목표: 텍스트 RDD에서 특정 문자열 포함, 시작 문자열, 끝 문자열 조건으로 필터링합니다.
# - lower()로 소문자 변환 후 "data", "ai" 포함 여부를 확인하세요.
# - 시작/끝 조건은 startswith(...), endswith(...) 문자열 메서드를 사용합니다.
# - 실행 위치: skeleton 디렉터리에서 실행해야 ../data/test.txt 경로가 맞습니다.

# TODO 안내
# - SparkSession과 SparkContext 생성 코드를 완성합니다.
# - data와 ai 포함 조건은 lower() 결과에 해당 문자열이 들어있는지 검사합니다.
# - 시작/끝 조건은 startswith와 endswith 문자열 메서드를 사용합니다.


from pyspark.sql import SparkSession

# SparkSession 생성
spark = SparkSession.builder.appName("DataFilterApp").getOrCreate()
sc = spark.sparkContext

# 1. 텍스트 파일 로드 및 데이터 확인
text_data = sc.textFile("../data/test.txt")
print(text_data.collect())

# 2. "data"가 포함된 문장만 출력
contains_data = text_data.filter(lambda line: "data" in line.lower())
print(contains_data.collect())

# 3. "ai"가 포함된 문장만 출력
contains_ai = text_data.filter(lambda line: "ai" in line.lower())
print(contains_ai.collect())

# 4. "data"가 포함된 문장의 개수
print("data 포함 문장 수:", contains_data.count())

# 5. "ai"가 포함된 문장의 개수
print("ai 포함 문장 수:", contains_ai.count())

# 6. "Big"으로 시작하는 문장
starts_with_big = text_data.filter(lambda line: line.startswith("Big"))
print(starts_with_big.collect())

# 7. "future"로 끝나는 문장
ends_with_future = text_data.filter(lambda line: line.endswith("future"))
print(ends_with_future.collect())