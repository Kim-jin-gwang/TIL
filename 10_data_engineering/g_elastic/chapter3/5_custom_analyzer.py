from elasticsearch import Elasticsearch, helpers
from pprint import pprint

# Elasticsearch 클라이언트 연결
es = Elasticsearch("http://localhost:9200")

# 실습에서 사용할 인덱스 이름
index_name = "products_chapter3"

# 같은 이름의 인덱스가 이미 있으면 삭제
# analyzer, mapping 설정은 인덱스 생성 시점에 적용되므로 실습에서는 삭제 후 다시 생성
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# 인덱스 생성 설정
# settings에는 analyzer, tokenizer, filter 같은 텍스트 분석 설정을 정의
# mappings에는 각 필드의 타입과 어떤 analyzer를 사용할지 정의
index_body = {
    "settings": {
        "analysis": {
            "tokenizer": {
                # Nori tokenizer는 한국어 형태소 분석을 위한 tokenizer
                # user_dictionary를 사용하면 사용자 정의 단어를 하나의 토큰처럼 인식하도록 보완 가능
                "nori_custom_tokenizer": {
                    "type": "nori_tokenizer",
                    "decompound_mode": "mixed",
                    "discard_punctuation": False,
                    "user_dictionary": "dictionary/userdict_ko.txt"
                }
            },
            "filter": {
                # stop filter는 검색에 큰 의미가 없는 단어를 제거할 때 사용
                # 예: the, and, is, a 같은 단어를 stopwords.txt에 정의해두면 제거 가능
                "search_stop_filter": {
                    "type": "stop",
                    "stopwords_path": "dictionary/stopwords.txt"
                },
                # synonym filter는 서로 같은 의미로 취급할 단어를 확장할 때 사용
                # 예: 갤럭시, galaxy를 동의어로 등록하면 두 검색어가 비슷하게 처리됨
                "my_synonym_filter": {
                    "type": "synonym",
                    "synonyms_path": "dictionary/synonyms.txt",
                    "lenient": True
                }
            },
            "analyzer": {
                # 영어 설명 문장에 적용할 analyzer
                # whitespace로 공백 기준 분리 후 lowercase, stop filter를 적용
                "search_stop_analyzer": {
                    "type": "custom",
                    "tokenizer": "whitespace",
                    "filter": [
                        "lowercase",
                        "search_stop_filter"
                    ]
                },
                # 한국어 상품명, 카테고리에 적용할 analyzer
                # Nori 사용자 사전과 동의어 필터를 함께 적용
                "user_dic_synonym_analyzer": {
                    "type": "custom",
                    "tokenizer": "nori_custom_tokenizer",
                    "filter": [
                        "lowercase",
                        "my_synonym_filter"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            # 상품명은 검색 대상이므로 text 타입으로 설정
            # 한국어 사용자 사전과 동의어가 적용된 analyzer 사용
            "name": {
                "type": "text",
                "analyzer": "user_dic_synonym_analyzer"
            },
            # 상품 설명은 영어 불용어 제거를 확인하기 위한 필드
            "description": {
                "type": "text",
                "analyzer": "search_stop_analyzer"
            },
            # brand는 정확히 일치하는 값으로 필터링/집계할 수 있도록 keyword 타입 사용
            "brand": {
                "type": "keyword"
            },
            # 가격과 평점은 범위 검색이나 정렬에 사용할 수 있도록 숫자 타입 사용
            "price": {
                "type": "float"
            },
            # category도 검색 대상이 될 수 있으므로 text 타입과 analyzer 적용
            "category": {
                "type": "text",
                "analyzer": "user_dic_synonym_analyzer"
            },
            "rating": {
                "type": "float"
            }
        }
    }
}

es.indices.create(index=index_name, body=index_body)
print(f"{index_name} 인덱스 생성 완료")

# Mapping 확인
# 각 필드가 어떤 타입과 analyzer로 생성되었는지 확인
mapping = es.indices.get_mapping(index=index_name)

print("\n [Mapping 확인] ")
pprint(mapping[index_name]["mappings"]["properties"])

# Analysis Settings 확인
# tokenizer, filter, analyzer 설정이 의도대로 들어갔는지 확인
settings = es.indices.get_settings(index=index_name)

print("\n [Analysis Settings 확인] ")
pprint(settings[index_name]["settings"]["index"]["analysis"])

# 불용어 제거 Analyzer 확인
# the, and, is, a 등이 stopwords.txt에 있으면 결과 토큰에서 제거됨
stop_analyze_result = es.indices.analyze(
    index=index_name,
    body={
        "analyzer": "search_stop_analyzer",
        "text": "the galaxy and iphone is a smartphone"
    }
)

print("\n [불용어 제거 analyzer 결과] ")
for token in stop_analyze_result["tokens"]:
    print(token["token"])

# Nori 사용자 사전 + 동의어 Analyzer 확인
# userdict_ko.txt에 등록된 단어가 있다면 토큰 분리 결과가 달라질 수 있음
userdict_analyze_result = es.indices.analyze(
    index=index_name,
    body={
        "analyzer": "user_dic_synonym_analyzer",
        "text": "삼성갤럭시 울트라 출시"
    }
)

print("\n [Nori 사용자 사전 + 동의어 analyzer 결과] ")
for token in userdict_analyze_result["tokens"]:
    print(token["token"])

# 동의어 Analyzer 확인
# synonyms.txt에 등록된 동의어가 함께 토큰으로 확장되는지 확인
synonym_analyze_result = es.indices.analyze(
    index=index_name,
    body={
        "analyzer": "user_dic_synonym_analyzer",
        "text": "갤럭시"
    }
)

print("\n [동의어 analyzer 결과: 갤럭시] ")
for token in synonym_analyze_result["tokens"]:
    print(token["token"])

# Bulk로 넣을 테스트 데이터 정의
# _id를 직접 지정하면 같은 코드를 여러 번 실행해도 같은 ID 문서는 덮어쓰기됨
documents = [
    {
        "_id": 1,
        "name": "삼성 갤럭시 울트라",
        "description": "the galaxy is a premium smartphone",
        "brand": "Samsung",
        "price": 1499.99,
        "category": "smartphone",
        "rating": 4.9
    },
    {
        "_id": 2,
        "name": "Galaxy Ultra",
        "description": "galaxy and ultra phone",
        "brand": "Samsung",
        "price": 1489.99,
        "category": "smartphone",
        "rating": 4.7
    },
    {
        "_id": 3,
        "name": "삼성갤럭시 울트라 출시",
        "description": "new galaxy was released",
        "brand": "Samsung",
        "price": 1479.99,
        "category": "smartphone",
        "rating": 4.6
    },
    {
        "_id": 4,
        "name": "아이폰 15 프로",
        "description": "the iphone is a smartphone",
        "brand": "Apple",
        "price": 1299.99,
        "category": "smartphone",
        "rating": 4.3
    }
]

# Bulk API 요청용 구조로 변환
# _source에는 실제 저장할 문서 내용을 넣고, _id는 Elasticsearch 문서 ID로 사용
actions = [
    {
        "_index": index_name,
        "_id": doc["_id"],
        "_source": {k: v for k, v in doc.items() if k != "_id"}
    }
    for doc in documents
]

# Bulk 삽입 실행
success_count, errors = helpers.bulk(es, actions)
print(f"\nBulk insert completed. 성공 문서 수: {success_count}")

# Bulk 삽입 직후 검색 결과에서 바로 확인할 수 있도록 refresh 실행
es.indices.refresh(index=index_name)

# 전체 문서 개수 확인
count_result = es.count(index=index_name)

print("\n [전체 문서 개수 확인] ")
print(f"저장된 문서 수: {count_result['count']}")

# 한국어 검색어로 검색
# name 필드에 설정된 user_dic_synonym_analyzer가 검색어에도 적용됨
resp = es.search(
    index=index_name,
    query={
        "match": {
            "name": "갤럭시"
        }
    }
)

print("\n [검색 결과: 갤럭시] ")
for hit in resp["hits"]["hits"]:
    print(f"score={hit['_score']:.4f}, name={hit['_source']['name']}")

# 영어 동의어 검색어로 검색
# synonyms.txt 설정에 따라 galaxy가 갤럭시와 연결되어 검색될 수 있음
resp = es.search(
    index=index_name,
    query={
        "match": {
            "name": "galaxy"
        }
    }
)

print("\n [검색 결과: galaxy] ")
for hit in resp["hits"]["hits"]:
    print(f"score={hit['_score']:.4f}, name={hit['_source']['name']}")

# 불용어가 포함된 문장 검색
# description 필드에는 search_stop_analyzer가 적용되어 불용어가 제거된 상태로 검색됨
resp = es.search(
    index=index_name,
    query={
        "match": {
            "description": "the galaxy and smartphone"
        }
    }
)

print("\n [검색 결과: the galaxy and smartphone] ")
for hit in resp["hits"]["hits"]:
    print(f"score={hit['_score']:.4f}, description={hit['_source']['description']}")