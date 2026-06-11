from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")


print("\n[1] match 검색")
print("검색어: AI")
print("대상 필드: description")
print("description 필드에 AI라는 단어가 포함된 문서를 검색")
print()

query = {
    "_source": ["product_id", "name", "description"],
    "query": {
        "match": {
            "description": "AI"
        }
    }
}

res = es.search(index="products", body=query)

print("[검색 결과]")
for hit in res["hits"]["hits"]:
    print(f"score: {hit['_score']}")
    print(hit["_source"])
print(" ")


print("\n[2] match 검색 - operator AND")
print("검색어: Samsung Neo")
print("대상 필드: name")
print("name 필드에 Samsung과 Neo가 모두 포함된 문서를 검색")
print()

query = {
    "_source": ["product_id", "name", "brand"],
    "query": {
        "match": {
            "name": {
                "query": "Samsung Neo",
                "operator": "AND"
            }
        }
    }
}

res = es.search(index="products", body=query)

print("[검색 결과]")
for hit in res["hits"]["hits"]:
    print(f"score: {hit['_score']}")
    print(hit["_source"])
print(" ")


print("\n[3] match_phrase 검색")
print("검색어: Samsung Neo")
print("대상 필드: name")
print("name 필드에서 Samsung Neo가 연속된 구문으로 등장하는 문서를 검색")
print()

query = {
    "_source": ["product_id", "name", "brand"],
    "query": {
        "match_phrase": {
            "name": "Samsung Neo"
        }
    }
}

res = es.search(index="products", body=query)

print("[검색 결과]")
for hit in res["hits"]["hits"]:
    print(f"score: {hit['_score']}")
    print(hit["_source"])
print(" ")


print("\n[4] match_phrase_prefix 검색")
print("검색어: Samsung N")
print("대상 필드: name")
print("name 필드에서 Samsung 다음에 N으로 시작하는 단어가 이어지는 문서를 검색")
print()

query = {
    "_source": ["product_id", "name", "brand"],
    "query": {
        "match_phrase_prefix": {
            "name": "Samsung N"
        }
    }
}

res = es.search(index="products", body=query)

print("[검색 결과]")
for hit in res["hits"]["hits"]:
    print(f"score: {hit['_score']}")
    print(hit["_source"])