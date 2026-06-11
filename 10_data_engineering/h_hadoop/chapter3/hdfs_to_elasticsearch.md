# HDFS → Elasticsearch 흐름 (JSON 저장 방식 + 직접 적재 방식)

HDFS에서 PySpark로 데이터를 읽고, Elasticsearch에 적재하는 두 가지 흐름을 설명합니다.

첫 번째 방식은 HDFS 데이터를 Spark로 읽은 뒤 JSON으로 저장하고, 별도의 Python 코드에서 Elasticsearch에 매핑 설정과 함께 bulk 업로드하는 방식입니다.

두 번째 방식은 중간 JSON 파일을 만들지 않고, Spark DataFrame을 Elasticsearch Spark Connector를 통해 Elasticsearch에 직접 적재하는 방식입니다.

---

## 디렉토리 구성 예시

```bash
/files
  ├── test_read_hdfs.py        # HDFS CSV → JSON 저장
  ├── upload_to_es.py          # JSON → Elasticsearch 업로드 및 인덱스 매핑
  ├── hdfs_to_es.py            # HDFS CSV → Elasticsearch 직접 적재
  └── transactions.csv
```

Spark Docker Compose에서 `jobs` 디렉터리를 `/opt/spark/jobs`로 마운트했다면, `hdfs_to_es.py`는 다음 위치에 있어야 합니다.

```bash
/opt/spark/jobs/hdfs_to_es.py
```

예시:

```bash
lecture_code/
  ├── jobs/
  │   └── hdfs_to_es.py
  ├── data/
  │   └── transactions.csv
  └── ...
```

---

## 1. 사전 조건

- Hadoop(HDFS) 정상 실행 중 (`hdfs dfs -ls` 또는 `hadoop fs -ls` 등으로 확인)
- Spark Master / Worker 정상 실행 중
- Elasticsearch 8.17 실행 중 (`http://es01:9200`)
- Hadoop, Spark, Elasticsearch가 같은 Docker 네트워크에 연결되어 있어야 함
- Python 패키지 설치 완료

예시 네트워크 설정:

```yaml
networks:
  shared-net:
    external: true
```

같은 Docker 네트워크에 연결되어 있으면 Spark 컨테이너에서 다음 주소를 사용할 수 있습니다.

```text
HDFS NameNode: hdfs://namenode:9000
Spark Master: spark://spark-master:7077
Elasticsearch: http://es01:9200
```


HDFS에 원본 CSV 파일을 업로드합니다.

```bash
hadoop fs -mkdir -p /user/local/hadoop_data
hadoop fs -put -f transactions.csv /user/local/hadoop_data/transactions.csv
hadoop fs -ls /user/local/hadoop_data
```

파일이 정상적으로 업로드되었는지 확인합니다.

```bash
hadoop fs -cat /user/local/hadoop_data/transactions.csv | head
```

---

## 2. test_read_hdfs.py (Spark로 JSON 저장)

이 방식은 HDFS에 있는 CSV 파일을 Spark로 읽은 뒤, 로컬 디스크에 JSON 파일로 저장합니다.

```python
from pyspark.sql import SparkSession

# SparkSession 생성
spark = SparkSession.builder \
    .appName("Read HDFS CSV") \
    .master("local[*]") \
    .getOrCreate()

# HDFS의 CSV 파일 읽기
df = spark.read.option("header", "true").csv("hdfs://namenode:9000/user/local/hadoop_data/transactions.csv")

# 데이터 출력 (검증용)
df.show()

# JSON 파일로 로컬 디스크에 저장
df.write.mode("overwrite").json("file:///tmp/hadoop_data/transactions")
```

실행:

```bash
python test_read_hdfs.py
```

### 참고

- Spark로 JSON 저장 시 기본적으로 `part-*.json` 파일들이 생성됩니다.
- 해당 데이터를 읽어 Elasticsearch에 문서 형태로 저장할 수 있습니다.
- 이 방식은 Spark 처리 결과를 중간 파일로 남긴 뒤, 별도의 적재 코드에서 Elasticsearch로 업로드하는 구조입니다.

---

## 3. upload_to_es.py (인덱스 매핑 + bulk 업로드)

이 방식은 앞 단계에서 생성된 JSON 파일을 읽고, Elasticsearch에 인덱스 매핑을 생성한 뒤 bulk 방식으로 업로드합니다.

### 코드 흐름

```python
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import RequestError
import os, json

# 1. Elasticsearch 연결
es = Elasticsearch("http://es01:9200")

# 2. JSON 파일 경로 및 인덱스 이름
data_dir = "/tmp/hadoop_data/transactions"
index_name = "finance-transactions"

# 3. 매핑 정의
index_mapping = {
    "mappings": {
        "properties": {
            "transaction_id":   { "type": "keyword" },
            "transaction_date": { "type": "date", "format": "yyyy-MM-dd||strict_date_optional_time" },
            "amount":           { "type": "float" },
            "category":         { "type": "keyword" }
        }
    }
}

# 4. 인덱스 생성 시도
try:
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=index_mapping)
        print(f"[INFO] 새 인덱스 [{index_name}] 생성 완료")
except RequestError as e:
    print(f"[ERROR] 인덱스 생성 오류: {e.info}")
```

---

### bulk 데이터 업로드

```python
# 5. JSON 파일 수집
json_files = [
    os.path.join(data_dir, f)
    for f in os.listdir(data_dir)
    if f.startswith("part-") and f.endswith(".json")
]

# 6. bulk action 구성
actions = []
for file_path in json_files:
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            actions.append({
                "_index": index_name,
                "_id": doc.get("transaction_id"),
                "_source": doc
            })

# 7. Elasticsearch로 업로드
if actions:
    response = helpers.bulk(es, actions)
    es.indices.refresh(index=index_name)
    print(f"[SUCCESS] {len(actions)} documents indexed to [{index_name}]")
else:
    print("[WARN] No documents found to index.")
```

실행:

```bash
python upload_to_es.py
```

---

## 4. hdfs_to_es.py (HDFS → Elasticsearch 직접 적재)

앞의 2번, 3번 방식은 다음과 같은 흐름입니다.

```text
HDFS CSV
  → Spark로 읽기
  → 로컬 JSON 파일 저장
  → Python Elasticsearch Client로 bulk 업로드
  → Elasticsearch
```

이번 방식은 중간 JSON 파일을 만들지 않고, Spark에서 Elasticsearch로 바로 저장합니다.

```text
HDFS CSV
  → Spark DataFrame
  → Elasticsearch Spark Connector
  → Elasticsearch
```

### 코드 흐름

#### 1) SparkSession 생성

```python
spark = (
    SparkSession.builder
    .appName("HDFS to Elasticsearch")
    .master("spark://spark-master:7077")
    .config(
        "spark.jars.packages",
        "org.elasticsearch:elasticsearch-spark-30_2.12:8.17.0"
    )
    .getOrCreate()
)
```

`master("spark://spark-master:7077")`는 Spark 작업을 Spark 클러스터에 제출하겠다는 의미입니다.

`org.elasticsearch:elasticsearch-spark-30_2.12:8.17.0` 패키지는 Spark DataFrame을 Elasticsearch에 저장하기 위한 Elasticsearch Spark Connector입니다.

이 Connector가 없으면 다음과 같은 오류가 발생할 수 있습니다.

```text
DATA_SOURCE_NOT_FOUND
Failed to find the data source: org.elasticsearch.spark.sql
```

또는 다음과 같은 오류가 발생할 수 있습니다.

```text
ClassNotFoundException: org.elasticsearch.spark.sql.DefaultSource
```

#### 2) Elasticsearch 인덱스 매핑 생성

```python
es_host = "http://es01:9200"
index_name = "finance-transactions"
```

Spark 컨테이너와 Elasticsearch 컨테이너가 같은 Docker 네트워크에 연결되어 있으므로, Elasticsearch 컨테이너 이름인 `es01`로 접근할 수 있습니다.

```python
index_mapping = {
    "mappings": {
        "properties": {
            "transaction_id": {
                "type": "keyword"
            },
            "transaction_date": {
                "type": "date",
                "format": "yyyy-MM-dd||strict_date_optional_time"
            },
            "amount": {
                "type": "float"
            },
            "category": {
                "type": "keyword"
            }
        }
    }
}
```

각 필드는 다음과 같은 의미를 가집니다.

| 필드명 | 타입 | 설명 |
|---|---|---|
| `transaction_id` | `keyword` | 거래 ID. 검색 및 문서 ID로 사용 |
| `transaction_date` | `date` | 거래 일자 |
| `amount` | `float` | 거래 금액 |
| `category` | `keyword` | 거래 카테고리 |

`transaction_id`, `category`는 정확히 일치하는 값으로 조회하거나 집계하기 좋은 필드이므로 `keyword` 타입을 사용합니다.

`transaction_date`는 날짜 기반 필터링과 Kibana 시각화를 위해 `date` 타입으로 지정합니다.

`amount`는 금액 비교와 집계를 위해 `float` 타입으로 지정합니다.

#### 3) HDFS CSV 읽기

```python
df = (
    spark.read
    .option("header", "true")
    .csv("hdfs://namenode:9000/user/local/hadoop_data/transactions.csv")
)
```

Spark가 HDFS에 저장된 CSV 파일을 읽습니다.

여기서 경로는 컨테이너 내부 로컬 경로가 아니라 HDFS 경로입니다.

```text
hdfs://namenode:9000/user/local/hadoop_data/transactions.csv
```

따라서 HDFS에도 동일한 위치에 `transactions.csv` 파일이 있어야 합니다.

#### 4) 컬럼 타입 변환

```python
df = (
    df
    .select(
        col("transaction_id").cast("string").alias("transaction_id"),
        col("transaction_date").cast("string").alias("transaction_date"),
        col("amount").cast("float").alias("amount"),
        col("category").cast("string").alias("category")
    )
)
```

CSV는 기본적으로 문자열 중심으로 읽히기 때문에, Elasticsearch 매핑에 맞게 타입을 정리합니다.

특히 `amount`는 숫자 비교와 집계를 위해 `float`으로 변환합니다.

검증을 위해 일부 데이터를 출력합니다.

```python
df.show(10, truncate=False)
df.printSchema()
```

예상 출력 예시는 다음과 같습니다.

```text
+--------------+----------------+-------+--------------+
|transaction_id|transaction_date|amount |category      |
+--------------+----------------+-------+--------------+
|TX1166        |2024-01-08      |273.11 |food          |
|TX1273        |2024-01-05      |391.69 |transportation|
|TX1042        |2024-02-11      |4892.9 |utilities     |
+--------------+----------------+-------+--------------+
```

스키마는 다음과 같이 확인됩니다.

```text
root
 |-- transaction_id: string (nullable = true)
 |-- transaction_date: string (nullable = true)
 |-- amount: float (nullable = true)
 |-- category: string (nullable = true)
```

#### 5) Spark DataFrame을 Elasticsearch에 저장

```python
(
    df.write
    .format("org.elasticsearch.spark.sql")
    .option("es.nodes", "es01")
    .option("es.port", "9200")
    .option("es.resource", index_name)
    .option("es.mapping.id", "transaction_id")
    .mode("append")
    .save()
)
```

`df.write.format("org.elasticsearch.spark.sql")`는 Spark DataFrame을 Elasticsearch에 저장하겠다는 의미입니다.

각 옵션의 의미는 다음과 같습니다.

| 옵션 | 의미 |
|---|---|
| `es.nodes` | Elasticsearch 노드 주소 |
| `es.port` | Elasticsearch 포트 |
| `es.resource` | 저장할 Elasticsearch 인덱스 이름 |
| `es.mapping.id` | Elasticsearch 문서 ID로 사용할 컬럼 |
| `mode("append")` | 기존 인덱스에 데이터를 추가 저장 |

특히 다음 설정이 중요합니다.

```python
.option("es.mapping.id", "transaction_id")
```

이 설정은 `transaction_id` 값을 Elasticsearch 문서의 `_id`로 사용합니다.

따라서 같은 `transaction_id`를 가진 데이터가 다시 적재될 경우, 매번 완전히 새로운 문서가 계속 쌓이는 것이 아니라 동일한 문서 ID 기준으로 저장됩니다.

---

### 실행

코드 안에 Spark Master와 Elasticsearch Spark Connector 설정이 들어 있으므로, 우선 아래 명령어로 실행합니다.

```bash
docker exec -it spark-master bash -c "/opt/spark/bin/spark-submit /opt/spark/jobs/hdfs_to_es.py"
```

다음 에러가 발생할 수 있습니다.

```text
ClassNotFoundException: org.elasticsearch.spark.sql.DefaultSource
```

이 경우 실행 명령어에서 직접 `--packages` 옵션을 지정합니다.

```bash
docker exec -it spark-master bash -c "/opt/spark/bin/spark-submit --master spark://spark-master:7077 --packages org.elasticsearch:elasticsearch-spark-30_2.12:8.17.0 /opt/spark/jobs/hdfs_to_es.py"
```

---

### 참고

Python 패키지 `elasticsearch`와 Elasticsearch Spark Connector는 역할이 다릅니다.

| 구분 | 역할 |
|---|---|
| `elasticsearch` Python 패키지 | Python 코드에서 Elasticsearch API 호출 |
| `elasticsearch-spark-30_2.12` Connector | Spark DataFrame을 Elasticsearch에 저장 |

따라서 Python 패키지를 설치했다고 해서 다음 코드가 자동으로 동작하는 것은 아닙니다.

```python
df.write.format("org.elasticsearch.spark.sql")
```

이 코드를 사용하려면 반드시 Elasticsearch Spark Connector가 필요합니다.

---

## 5. 결과 확인

### Elasticsearch API

Elasticsearch 컨테이너 또는 같은 네트워크에 연결된 컨테이너에서 다음 명령어로 확인합니다.

```bash
curl -XGET 'http://es01:9200/finance-transactions/_search?pretty'
```

또는 호스트에서 9200 포트를 열어두었다면 다음 명령어로도 확인할 수 있습니다.

```bash
curl -XGET 'http://localhost:9200/finance-transactions/_search?pretty'
```

문서 개수만 확인하려면 다음 명령어를 사용합니다.

```bash
curl -XGET 'http://localhost:9200/finance-transactions/_count?pretty'
```

또는 Kibana 접속 후 아래 경로에서 확인합니다.

- **Stack Management > Index Management** 에서 `finance-transactions` 존재 확인
- **Discover** 메뉴에서 데이터 탐색 가능
- **Data View** 생성 시: `finance-transactions`, `finance-transactions-*`, `transaction_date`로 지정

---

## 6. Kibana 시각화 예시

- 시간 흐름에 따른 거래 수 변화
- 카테고리별 거래 비율 파악
- 금액이 300 초과인 거래 필터링 (예: `amount > 300`)
- 날짜별 거래 건수 분석
- 카테고리별 평균 거래 금액 분석

---

## 7. 확장 가능 요소

- Airflow DAG 구성하여 ETL 자동화
- Spark DataFrame or SQL 기반 데이터 전처리 적용
- Kafka 연계 실시간 적재 구조
- Spark Structured Streaming 기반 실시간 Elasticsearch 적재
- Kibana Dashboard를 통한 거래 데이터 시각화

---

## 8. 전체 흐름 요약

### 방식 1. JSON 저장 후 bulk 업로드

```text
HDFS
  └── /user/local/hadoop_data/transactions.csv
        ↓
Spark
  └── test_read_hdfs.py
        ↓
Local JSON
  └── /tmp/hadoop_data/transactions/part-*.json
        ↓
Python Elasticsearch Client
  └── upload_to_es.py
        ↓
Elasticsearch
  └── finance-transactions
```

### 방식 2. Spark에서 Elasticsearch 직접 적재

```text
HDFS
  └── /user/local/hadoop_data/transactions.csv
        ↓
Spark
  └── hdfs_to_es.py
        ↓
Elasticsearch Spark Connector
        ↓
Elasticsearch
  └── finance-transactions
```
