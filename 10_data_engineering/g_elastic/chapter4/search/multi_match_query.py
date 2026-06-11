from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")


print("\n[0] multi_match 기본 검색")
print("검색어: Samsung")
print("대상 필드: name, description")
print("여러 필드에서 Samsung을 검색")
print("type을 지정하지 않으면 기본적으로 best_fields 방식으로 동작")
print()

query = {
    "_source": ["product_id", "name", "brand", "description"],
    "query": {
        "multi_match": {
            "query": "Samsung",
            "fields": ["name", "description"],
            "operator": "or"
        }
    }
}

res = es.search(index="products", body=query)
for hit in res["hits"]["hits"]:
    print(f"score: {hit['_score']}")
    print(hit["_source"])
print(" ")


print("\n[1] best_fields 검색")
print("검색어: Samsung")
print("대상 필드: name, description")
print("여러 필드 중 Samsung과 가장 잘 맞는 필드를 기준으로 검색")
print()

query = {
    "_source": ["product_id", "name", "brand", "description"],
    "query": {
        "multi_match": {
            "query": "Samsung",
            "fields": ["name", "description"],
            "type": "best_fields",
            "operator": "or"
        }
    }
}

res = es.search(index="products", body=query)
for hit in res["hits"]["hits"]:
    print(f"score: {hit['_score']}")
    print(hit["_source"])
print(" ")


print("\n[2] most_fields 검색")
print("검색어: Samsung")
print("대상 필드: name, description")
print("name과 description 여러 필드에서 Samsung이 많이 매칭되는 문서를 검색")
print()

query = {
    "_source": ["product_id", "name", "brand", "description"],
    "query": {
        "multi_match": {
            "query": "Samsung",
            "fields": ["name", "description"],
            "type": "most_fields",
            "operator": "or"
        }
    }
}

res = es.search(index="products", body=query)
for hit in res["hits"]["hits"]:
    print(f"score: {hit['_score']}")
    print(hit["_source"])
print(" ")


print("\n[3] cross_fields 검색")
print("검색어: Samsung Ultra")
print("대상 필드: name, description")
print("name과 description을 하나의 필드처럼 보고 Samsung과 Ultra가 모두 포함된 문서를 검색")
print()

query = {
    "_source": ["product_id", "name", "brand", "description"],
    "query": {
        "multi_match": {
            "query": "Samsung Ultra",
            "fields": ["name", "description"],
            "type": "cross_fields",
            "operator": "and"
        }
    }
}

res = es.search(index="products", body=query)
for hit in res["hits"]["hits"]:
    print(f"score: {hit['_score']}")
    print(hit["_source"])