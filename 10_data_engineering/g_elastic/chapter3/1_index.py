from elasticsearch import Elasticsearch
from pprint import pprint

es = Elasticsearch("http://localhost:9200")

index_name = "products_chapter3"

if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

index_body = {
    "settings": {
        "analysis": {
            "tokenizer": {
                "nori_custom_tokenizer": {
                    "type": "nori_tokenizer",
                    "decompound_mode": "mixed",
                    "discard_punctuation": False,
                    "user_dictionary": "dictionary/userdict_ko.txt"
                }
            },
            "filter": {
                "my_synonym_filter": {
                    "type": "synonym",
                    "synonyms_path": "dictionary/synonyms.txt",
                    "lenient": True
                }
            },
            "analyzer": {
                "user_dict_analyzer": {
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
            "name": {
                "type": "text",
                "analyzer": "user_dict_analyzer"
            },
            "brand": {
                "type": "keyword"
            },
            "price": {
                "type": "float"
            },
            "category": {
                "type": "text",
                "analyzer": "user_dict_analyzer"
            },
            "rating": {
                "type": "float"
            }
        }
    }
}

es.indices.create(index=index_name, body=index_body)
print(f"{index_name} 생성 완료")


# 1. Mapping 확인
mapping = es.indices.get_mapping(index=index_name)

print("\n [Mapping 확인] ")
pprint(mapping[index_name]["mappings"]["properties"])


# 2. Settings 확인
settings = es.indices.get_settings(index=index_name)

print("\n [Analyzer 설정 확인] ")
pprint(settings[index_name]["settings"]["index"]["analysis"])


# 3. 필드의 analyzer 적용 여부 확인
print("\n [name 필드 analyzer 확인] ")
print(mapping[index_name]["mappings"]["properties"]["name"]["analyzer"])