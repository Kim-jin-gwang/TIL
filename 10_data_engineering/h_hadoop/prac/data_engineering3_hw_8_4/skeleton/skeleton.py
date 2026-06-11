import pandas as pd
from elasticsearch import Elasticsearch

# 과제 Lv2에서 만들었던 데이터를 해당 위치로 이동 시켜 진행해야 합니다.

df = pd.read_csv('/tmp/hadoop_data/transactions.csv')
records = df.to_dict(orient='records')

es = Elasticsearch('http://es01:9200')
for record in records:
    es.index(index='finance-index', document=record)

# 인덱싱 후, 아래의 내용과 같은 형태를 Kibana Dev tools를 활용해서 데이터를 확인하고 캡쳐하여 같이 업로드합니다.
# 3. 문서 인덱싱
for record in records:
    doc_id = record.get('transaction_id') or f"{record.get('transaction_date')}-{record.get('amount')}"
    es.index(index='finance-index', id=doc_id, document=record)

es.indices.refresh(index='finance-index')

# 4. category가 "food"인 문서 검색
query = {
    "query": {
        "match": {
        "category": "food"
        }
    }
}

response = es.search(index='finance-index', body=query)

# 5. 검색 결과 출력
for hit in response['hits']['hits']:
    print(hit['_source'])


"""
POST finance-index/_search
{
  "query": {
    "match": {
      "category": "food"
    }
  }
}
"""
