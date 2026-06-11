import pandas as pd
from elasticsearch import Elasticsearch

# 1. CSV 파일 불러오기
df = pd.read_csv("/workspace/transactions.csv")  # ← 파일 경로 입력 ("transactions.csv")

# 2. JSON 형식으로 변환
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_dict.html
records = df.to_dict(orient='records')  # ← 'records' 지정

# 3. Elasticsearch 연결
es = Elasticsearch("http://es01:9200")

# 4. 데이터 업로드
for record in records:
    es.index(index='finance', document=record)  # ← 인덱스 이름 입력 (finance")


# Kibana에서 데이터를 확인합니다.

# 확인한 데이터에서 

