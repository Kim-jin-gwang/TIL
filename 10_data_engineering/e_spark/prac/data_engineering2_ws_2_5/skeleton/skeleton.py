# 실습 힌트
# - 목표: 고객 이탈 CSV를 RDD로 읽고 조건별 평균 이탈률을 계산합니다.
# - raw_rdd는 sc.textFile로 만들고, 첫 줄 header를 제거한 뒤 분석합니다.
# - CSV 컬럼 인덱스를 확인하면서 parse_credit, parse_age, parse_card 함수의 반환값을 맞추세요.
# - 실행 위치: skeleton 디렉터리에서 실행해야 ../data/Customer-Churn-Records.csv 경로가 맞습니다.

# TODO 안내
# - CSV 로드는 sc.textFile을 사용합니다.
# - 각 parse 함수 적용은 map, None 제거는 filter로 연결합니다.
# - 그룹별 평균 계산 전 같은 키끼리 모으려면 groupByKey를 사용합니다.
# - 최종 출력은 collect로 드라이버에 가져와 반복 출력합니다.
# - 카드 유형 평균도 groupByKey 뒤 mapValues로 계산합니다.

# 고객 이탈 데이터 분석 실습 Skeleton 파일
# TODO 표시된 부분을 채운 후 PySpark 환경에서 실행하세요.

from pyspark import SparkContext
sc = SparkContext("local", "PartitionPerformanceApp")

# 1. CSV 파일 로드 및 데이터 확인
# CSV 파일을 RDD로 변환
raw_rdd = sc.textFile("../data/Customer-Churn-Records.csv")

# 헤더 
header = raw_rdd.first()
data_rdd = raw_rdd.filter(lambda line: line != header)

# 헤더 제거 후 상위 5개 데이터
print("\n[헤더 제거 후 상위 5개 데이터]")
for row in data_rdd.take(5):
    print(row)

# 3. 신용 점수(CreditScore)별 고객 이탈률 분석
def parse_credit(line):
    cols = line.split(",")
    if cols[3].strip() == "" or cols[13].strip() == "":
        return None
    credit_score = (int(cols[3]) // 100) * 100
    exited = int(cols[13])
    return (f"{credit_score}점대", exited)

credit_rdd = data_rdd.map(parse_credit).filter(lambda x: x is not None)
credit_avg_rdd = credit_rdd.groupByKey().mapValues(lambda vals: sum(vals)/len(vals)*100)

print("\n[신용 점수대별 평균 이탈률]")
for item in credit_avg_rdd.collect():
    print(item)

# 4. 연령(Age)대별 고객 이탈률 분석
def parse_age(line):
    cols = line.split(",")
    if cols[6].strip() == "" or cols[13].strip() == "":
        return None
    age_group = (int(cols[6]) // 10) * 10
    exited = int(cols[13])
    return (f"{age_group}대", exited)

age_rdd = data_rdd.map(parse_age).filter(lambda x: x is not None)
age_avg_rdd = age_rdd.groupByKey().mapValues(lambda vals: sum(vals)/len(vals)*100)

print("\n[연령대별 평균 이탈률]")
for item in age_avg_rdd.collect():
    print(item)

# 5. 카드 유형(Card Type)별 고객 이탈률 분석
def parse_card(line):
    cols = line.split(",")
    if cols[16].strip() == "" or cols[13].strip() == "":
        return None
    card_type = cols[16].strip()
    exited = int(cols[13])
    return (card_type, exited)

card_rdd = data_rdd.map(parse_card).filter(lambda x: x is not None)
card_avg_rdd = card_rdd.groupByKey().mapValues(lambda vals: sum(vals)/len(vals)*100)

print("\n[카드 유형별 평균 이탈률]")
for item in card_avg_rdd.collect():
    print(item)
