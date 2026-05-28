# 실습 힌트
# - 목표: 직접 만든 RDD에 map/filter/count/collect를 적용해 기본 변환을 익힙니다.
# - SparkSession 생성, sc.parallelize, len, map, filter, collect를 순서대로 채우세요.
# - filter는 조건을 만족하는 원소만 남기고, count는 원소 개수만 반환합니다.
# - "is" 필터는 부분 문자열이 아니라 독립 단어인지 확인하도록 split()을 사용합니다.
# - 실행 위치는 이 파일이 있는 skeleton 디렉터리를 권장합니다.

# TODO 안내
# - SparkSession과 SparkContext 생성 코드를 완성합니다.
# - RDD 생성은 SparkContext의 리스트 병렬화 메서드를 사용합니다.
# - 단어 길이는 len, 변환은 map, 개수 확인은 count, 결과 확인은 collect를 사용합니다.
# - is 필터는 filter와 split을 조합해 독립 단어만 검사합니다.


from pyspark.sql import SparkSession

# SparkSession 생성
spark = SparkSession.builder.appName("WordLengthApp").getOrCreate()
sc = spark.sparkContext

# 1. 단어 길이 변환 및 필터링
# 문자열 데이터 생성("Spark", "Parallel", "Machine", "Learning", "Hadoop", "Kafka", "Big Data")
words = sc.parallelize(["Spark", "Parallel", "Machine", "Learning", "Hadoop", "Kafka", "Big Data"])

# 생성한 문자열 데이터 확인
print(words.collect())

# 각 단어의 길이 계산
word_lengths = words.map(lambda word: len(word))
print(word_lengths.collect())

# 6글자 이상 단어만 필터링
long_words = words.filter(lambda word: len(word) >= 6)
print(long_words.collect())

# 6글자 이상 단어 개수
long_words_count = long_words.count()
print(f"6글자 이상 단어 개수: {long_words_count}")

# 2. 짝수/홀수 필터링 및 합산 연산
# 1~20까지 숫자 데이터를 생성
numbers = sc.parallelize(range(1, 21))

# 짝수 필터링 후 데이터 확인
even = numbers.filter(lambda x: x % 2 == 0)
print("짝수:", even.collect())

# 홀수 필터링 후 데이터 확인
odd = numbers.filter(lambda x: x % 2 != 0)
print("홀수:", odd.collect())

# 3.소문자 변환 및 "is" 포함 문장 필터링
# 문자열 데이터 생성
sentences = sc.parallelize([
    "Spark is a powerful analytics engine",
    "Big Data is transforming industries",
    "Data Science is revolutionizing decision making",
    "Machine Learning and AI are the future"
])

# 모든 문장을 소문자로 변환하여 데이터 확인
lower = sentences.map(lambda line: line.lower())
print("소문자 변환:", lower.collect())

# "is"라는 독립 단어가 포함된 문장만 필터링 후 데이터 확인
contains_is = sentences.filter(lambda line: "is" in line.lower().split())  # TODO: filter 연산과 단어 단위 분리를 위한 문자열 메서드
print('"is" 포함 문장:', contains_is.collect())
