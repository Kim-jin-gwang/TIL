from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")


print("\n[1] nested 검색 - feature_name = Camera")
print("검색 조건: features 배열 안에서 feature_name이 Camera인 문서")
print("nested 필드 내부에 Camera 기능이 존재하는 상품을 검색")
print()

query = {
    "query": {
        "nested": {
            "path": "features",
            "query": {
                "term": {
                    "features.feature_name": "Camera"
                }
            }
        }
    }
}

response = es.search(index="products", body=query)

print("[검색 결과]")
for hit in response["hits"]["hits"]:
    source = hit["_source"]
    print(f"score: {hit['_score']}")
    print(f"- {source['name']} ({source['brand']})")
print(" ")


print("\n[2] nested 검색 - RAM = 16GB")
print("검색 조건: 같은 features 객체 안에서 feature_name은 RAM, feature_value는 16GB")
print("RAM이라는 기능의 값이 16GB인 상품만 정확히 검색")
print()

query = {
    "query": {
        "nested": {
            "path": "features",
            "query": {
                "bool": {
                    "must": [
                        { "term": { "features.feature_name": "RAM" }},
                        { "term": { "features.feature_value": "16GB" }}
                    ]
                }
            }
        }
    }
}

response = es.search(index="products", body=query)

print("[검색 결과] RAM = 16GB")
for hit in response["hits"]["hits"]:
    doc = hit["_source"]
    print(f"score: {hit['_score']}")
    print(f"- {doc['name']} ({doc['brand']})")
print(" ")


print("\n[3] 일반 bool 검색 - nested 사용 안 함")
print("검색 조건: 문서 전체에서 features.feature_name에 RAM이 있고, features.feature_value에 16GB가 존재")
print("nested를 쓰지 않았을 때 배열 내부 객체의 관계가 정확히 유지되지 않을 수 있음을 확인")
print()

query = {
    "query": {
        "bool": {
            "must": [
                { "term": { "features.feature_name": "RAM" }},
                { "term": { "features.feature_value": "16GB" }}
            ]
        }
    }
}

response = es.search(index="products", body=query)

print("[검색 결과] RAM이라는 이름과 16GB라는 값이 존재하는 문서 (nested 아님)")
for hit in response["hits"]["hits"]:
    doc = hit["_source"]
    print(f"score: {hit['_score']}")
    print(f"- {doc['name']} ({doc['brand']})")