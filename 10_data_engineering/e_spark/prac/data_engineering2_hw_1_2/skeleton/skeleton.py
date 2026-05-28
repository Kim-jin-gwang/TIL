# 실습 힌트
# - 목표: SparkSession/SparkContext를 만들고 map, filter, count 같은 기본 변환/액션을 연습합니다.
# - SparkSession.builder.appName(...).getOrCreate() 순서와 spark.sparkContext를 먼저 완성하세요.
# - RDD 생성은 sc.parallelize(...), 결과 확인은 collect() 또는 count()를 사용합니다.
# - 실행 위치는 이 파일이 있는 skeleton 디렉터리를 권장합니다.

# TODO 안내
# - SparkSession.builder.appName(...).getOrCreate() 순서로 SparkSession을 생성합니다.
# - spark.sparkContext로 RDD 작업에 사용할 SparkContext를 가져옵니다.
# - sc.parallelize로 1부터 20까지의 숫자 RDD를 생성합니다.


from pyspark.sql import SparkSession

# SparkSession 생성
spark = SparkSession.builder.appName("Transformations").getOrCreate()
sc = spark.sparkContext

# 1. 버전 확인
print("Spark version:", sc.version)

# 2. 숫자 데이터 생성 및 변환 연산
# 1~20까지 숫자 데이터 생성
numbers = sc.parallelize(range(1, 21))

# 생성된 데이터 확인
print(numbers.collect())

# 각 숫자를 2배 변환
doubled = numbers.map(lambda x: x * 2)
print(doubled.collect())

# 10보다 큰 숫자만 출력
greater_than_10 = numbers.filter(lambda x: x > 10)
print(greater_than_10.collect())

# 1~20까지 생성된 숫자의 총 개수 확인
print(numbers.count())

# 10보다 큰 숫자의 총 개수 확인
print(greater_than_10.count())

# 3. 알파벳 문자열 데이터 변환 연산
alphabets = sc.parallelize(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"])

# 생성된 알파벳 데이터 확인
print(alphabets.collect())

# 각 문자를 두 번 반복
repeated = alphabets.map(lambda x: x * 2)
print(repeated.collect())

# "E"보다 뒤에 있는 문자만 출력
after_E = alphabets.filter(lambda x: x > "E")
print(after_E.collect())

# "E"보다 뒤에 있는 문자의 총 개수 확인
print(after_E.count())

# 알파벳 데이터를 소문자로 변환
lower_alphabets = alphabets.map(lambda x: x.lower())
print(lower_alphabets.collect())

# 4. 랜덤 숫자 리스트 변환
random_numbers = sc.parallelize([3, 10, 5, 7, 1])

# 모든 숫자를 제곱
squared = random_numbers.map(lambda x: x * x)
print(squared.collect())

# 제곱한 숫자의 값 중 10보다 큰 값만 출력
greater_than_10_sq = squared.filter(lambda x: x > 10)
print(greater_than_10_sq.collect())

# 10보다 큰 값의 총 개수 확인
print(greater_than_10_sq.count())
