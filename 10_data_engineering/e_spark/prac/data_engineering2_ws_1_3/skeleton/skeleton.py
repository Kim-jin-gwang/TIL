# 실습 힌트
# - 목표: sc.textFile로 외부 파일을 읽고 collect/count/map으로 내용을 탐색합니다.
# - print TODO에는 RDD 액션 결과가 들어가야 합니다. 예: collect(), count().
# - 대소문자 변환은 문자열 메서드 upper(), lower(), 길이는 len(line)을 사용합니다.
# - 실행 위치: skeleton 디렉터리에서 실행해야 ../data/test.txt 경로가 맞습니다.

# TODO 안내
# - SparkSession과 SparkContext 생성 코드를 완성합니다.
# - 전체 데이터 확인은 collect, 줄 수 확인은 count를 사용합니다.
# - 대소문자 변환과 길이 계산은 map 안에서 문자열 메서드와 len을 사용합니다.


from pyspark.sql import SparkSession

# SparkSession 생성
spark = SparkSession.builder.appName("LoadExternalFileApp").getOrCreate()
sc = spark.sparkContext

# 1. 텍스트 파일 로드
text_data = sc.textFile("../data/test.txt")

# 2. 전체 데이터 확인
print("전체 데이터:",text_data.collect())

# 3. 전체 줄 개수 확인
print("전체 줄 수:",text_data.count())

# 4. 모든 문장을 대문자로 변환 후 출력
upper_case_data = text_data.map(lambda line: line.upper())
print(upper_case_data.collect())

# 5. 모든 문장을 소문자로 변환 후 출력
lower_case_data = text_data.map(lambda line: line.lower())
print(lower_case_data.collect())

# 6. 각 문장의 길이 출력
line_lengths = text_data.map(lambda line: len(line))
print(line_lengths.collect())