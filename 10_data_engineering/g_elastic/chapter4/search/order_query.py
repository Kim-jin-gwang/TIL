from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")


print("\n[1] 가격 기준 정렬 검색")
print("대상 인덱스: products")
print("정렬 기준: price")
print("정렬 방식: 내림차순(desc)")
print("상품을 가격이 높은 순서대로 조회")
print()

response = es.search(
    index="products",
    body={
        "sort": [
            {
                "price": {
                    "order": "desc"
                }
            }
        ]
    }
)

print("[products 인덱스 - price 내림차순 정렬 결과]")
for hit in response["hits"]["hits"]:
    source = hit["_source"]
    print(f"sort value: {hit['sort']}, name: {source['name']}")