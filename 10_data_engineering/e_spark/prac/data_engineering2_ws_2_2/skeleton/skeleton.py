# 실습 힌트
# - 목표: 텍스트를 단어로 분해하고 stopwords 제거 후 단어별 개수를 계산합니다.
# - 줄 단위 RDD를 단어 단위로 펼칠 때는 flatMap을 사용합니다.
# - 단어 개수 계산은 (word, 1) 쌍을 만든 뒤 reduceByKey로 합산합니다.
# - 실행 위치: skeleton 디렉터리에서 실행해야 ../data/wordCount.txt 경로가 맞습니다.

# TODO 안내
# - 줄 단위 RDD를 단어 단위로 펼칠 때 flatMap을 사용합니다.
# - 중간 결과 확인은 collect를 사용합니다.
# - 소문자 변환과 길이 필터는 map/filter로 처리합니다.
# - stopwords 집합을 기준으로 제거하고, (word, 1) 쌍을 만든 뒤 reduceByKey로 합산합니다.

# WordCount 실습 Skeleton 파일
# TODO 표시된 부분을 채운 후 PySpark 환경에서 실행하세요.

from pyspark import SparkContext
import re
sc = SparkContext("local", "WordCountApp")

# 1. 텍스트 파일 RDD 변환
word_count_rdd = sc.textFile("../data/wordCount.txt")

# 2. 불필요한 단어 목록 정의 (Stopwords)
stopwords = {"and", "is", "the", "on", "of", "to", "a", "has", "for", "from",
             "that", "this", "it", "an", "be", "are", "by", "in", "with", "as"}

# 3. 줄을 단어 단위로 분리
words = word_count_rdd.flatMap(lambda line: re.findall(r'\b\w+\b', line))
print(words.collect())

# 4. 모든 단어를 소문자로 변환
lower_words = words.map(lambda word: word.lower())
print(lower_words.collect())

# 5. 최소 길이 3글자 이상만 필터링
filtered_length = lower_words.filter(lambda word: len(word) > 2)
print(filtered_length.collect())

# 6. Stopwords 제거
filtered_words = filtered_length.filter(lambda word: word not in stopwords)
print(filtered_words.collect())

# 7. (단어, 1) 형태로 매핑
word_pairs = filtered_words.map(lambda word: (word, 1))

# 8. 단어별 빈도 계산
word_counts = word_pairs.reduceByKey(lambda a, b: a + b)
print(word_counts.collect())
