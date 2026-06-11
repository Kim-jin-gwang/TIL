from elasticsearch import Elasticsearch, helpers
import json
import time
import os

# --------------------------------------------------------
# TODO: 1. Elasticsearch 클라이언트 생성
# --------------------------------------------------------
es = Elasticsearch("http://localhost:9200")
index_name = "products"

# --------------------------------------------------------
# 공통 실행 함수
# --------------------------------------------------------
def show_aggs(label, body):
    print(f"\n{label}")
    # TODO: 2. 집계 쿼리 실행
    res = es.search(index=index_name, body=body)
    print(json.dumps(res.get("aggregations", {}), indent=2, ensure_ascii=False))

# --------------------------------------------------------
# [1] 기존 인덱스 삭제
# --------------------------------------------------------
print("[1] 기존 인덱스 삭제")
# TODO: 인덱스 존재 여부 확인
if es.indices.exists(index=index_name):
    # TODO: 인덱스 삭제
    es.indices.delete(index=index_name)
    print(" → 기존 인덱스 삭제 완료")
else:
    print(" → 기존 인덱스 없음, 새로 생성 진행")
time.sleep(1)

# --------------------------------------------------------
# [2] 인덱스 생성 (name, brand(keyword), price)
# --------------------------------------------------------
print("[2] 인덱스 생성 및 매핑 적용")

# TODO: 인덱스 생성
es.indices.create(
    index=index_name,
    body={
        "mappings": {
            "properties": {
                "name":  { "type": "text" },
                "brand": { "type": "keyword" },   # 집계를 위해 반드시 keyword
                "price": { "type": "double" }
            }
        }
    }
)
time.sleep(1)

# --------------------------------------------------------
# [3] Bulk 데이터 삽입
# --------------------------------------------------------
print("[3] Bulk 데이터 삽입 (sample_products.json 사용)")

json_path = "../data/product_list.json"
if not os.path.exists(json_path):
    print(f"파일 없음: {json_path}")
    raise SystemExit(1)

with open(json_path, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

actions = []
for i in range(0, len(lines), 2):  # Bulk 포맷: action + doc
    action_meta = json.loads(lines[i])
    doc = json.loads(lines[i + 1])
    meta = list(action_meta.values())[0]

    actions.append({
        "_index": index_name,
        "_id": meta.get("_id"),
        "_source": doc
    })

# TODO: Bulk 삽입 실행
helpers.bulk(es, actions)

# TODO: 인덱스 refresh
es.indices.refresh(index=index_name)
print(" → 데이터 삽입 및 refresh 완료")
time.sleep(1)

# --------------------------------------------------------
# [4] 전체 문서 가격 통계(stats)
# --------------------------------------------------------
show_aggs("[4] 전체 가격 통계(stats)", {
    "size": 0,
    "aggs": {
        "price_stats": {
            "stats": {
                "field": "price"
            }
        }
    }
})

# --------------------------------------------------------
# [5] 브랜드별 상품 개수 (terms)
# --------------------------------------------------------
show_aggs("[5] 브랜드별 상품 개수(terms)", {
    "size": 0,
    "aggs": {
        "brand_buckets": {
            "terms": {
                "field": "brand",
                "size": 10
            }
        }
    }
})

# --------------------------------------------------------
# [6] Samsung 브랜드만 필터링 후 가격 통계(stats)
# --------------------------------------------------------
show_aggs("[6] Samsung 브랜드 대상 가격 통계(stats)", {
    "size": 0,
    "query": {
        "term": {
            "brand": "Samsung"
        }
    },
    "aggs": {
        "samsung_price_stats": {
            "stats": {
                "field": "price"
            }
        }
    }
})

print("\nElasticsearch Metric & Bucket Aggregation 실습 완료!")
