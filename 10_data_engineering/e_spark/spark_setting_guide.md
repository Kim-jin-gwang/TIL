# PySpark 설치 및 실습 가이드

## 1. Spark 다운로드 및 설치

```bash
cd /home/ssafy

# Spark 3.5.4 다운로드
wget https://archive.apache.org/dist/spark/spark-3.5.4/spark-3.5.4-bin-hadoop3.tgz

# 압축 해제
tar -xvzf spark-3.5.4-bin-hadoop3.tgz

# /home/ssafy/spark 로 이동
sudo mv spark-3.5.4-bin-hadoop3 /home/ssafy/spark
```

---

## 2. Spark 환경변수 등록

```bash
echo 'export SPARK_HOME=/home/ssafy/spark' >> ~/.bashrc
echo 'export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-*.zip:$PYTHONPATH' >> ~/.bashrc
echo 'export PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

환경변수 설정 확인:
```bash
echo $SPARK_HOME
# 출력: /home/ssafy/spark
```

---

## 3. Spark 실행 확인

```bash
spark-shell
```

정상 실행되면 `Ctrl + C`로 종료.

---

## 4. PySpark 설치

```bash
pip install pyspark==3.5.4
```

---

## 5. PySpark 기본 예제

```bash
pyspark
```

```python
from pyspark.sql import SparkSession

# Spark 세션 생성
spark = SparkSession.builder.appName("App").getOrCreate()

# Spark 버전 출력
print("Spark Version:", spark.version)

# 간단한 연산
a = 5
b = 10
print("a + b =", a + b)
print("a * b =", a * b)

# Spark 세션 종료
spark.stop()
```

---

## 6. sc.textFile() 활용 예제 (Python 버전)

### 6.1 테스트 파일 생성
```bash
echo "Hello Spark Apache Spark is powerful Big Data Processing" > test.txt
```

---

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("TextFileExample").getOrCreate()
sc = spark.sparkContext

# 파일 읽기
rdd = sc.textFile("test.txt")
```

---

```python
print("파티션 개수:", rdd.getNumPartitions())

rdd_single = rdd.repartition(1)
print("변경된 파티션 개수:", rdd_single.getNumPartitions())
```

---

## 7. RDD 액션 & 트랜스포메이션 

```python
# collect() — 전체 데이터 조회
print(rdd.collect())
```
> 모든 데이터를 배열 형태로 반환 (Action 연산)  
> **주의:** 대규모 데이터에서는 사용 지양.

```python
print("줄 개수:", rdd.count())
```

```python
filtered = rdd.filter(lambda line: "Spark" in line)
print(filtered.collect())
```
> 조건을 만족하는 요소만 포함하는 새로운 RDD 생성 (Transformation 연산).

```python
lower = rdd.map(lambda line: line.lower())
print(lower.collect())
```
> RDD의 각 요소를 변환하여 새로운 RDD 생성 (Transformation 연산).

```python
spark.stop()
```

---



## 8. Docker를 활용한 Spark 실행 환경 구성

### 8.1 프로젝트 구조

```bash
spark_docker/
├── Dockerfile.spark
├── docker-compose.yml
├── jobs/
│   └── example.py
├── data/
└── output/
```

### 8.2 Dockerfile 작성 (Python + Pandas 포함)

```Dockerfile
FROM apache/spark:3.5.4-java17-python3

USER root

# python alias 설정 (중요)
RUN ln -sf $(which python3) /usr/bin/python

# pandas 설치
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pandas==2.2.3

USER spark
```

### 8.3 docker-compose.yml 작성

```yml
services:
  spark-master:
    build:
      context: .
      dockerfile: Dockerfile.spark
    container_name: spark-master
    environment:
      - SPARK_MODE=master
      - SPARK_MASTER_HOST=spark-master
    ports:
      - "8083:8080"
      - "7077:7077"
    networks:
      - de_net
    command: /bin/bash -c "/opt/spark/sbin/start-master.sh && tail -f /dev/null"
    volumes:
      - ./jobs:/opt/spark/jobs
      - ./data:/opt/spark/data
      - ./output:/opt/spark/output

  spark-worker:
    build:
      context: .
      dockerfile: Dockerfile.spark
    container_name: spark-worker
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
    depends_on:
      - spark-master
    ports:
      - "8084:8081"
    networks:
      - de_net
    command: /bin/bash -c "sleep 5; /opt/spark/sbin/start-worker.sh $${SPARK_MASTER_URL} && tail -f /dev/null"
    volumes:
      - ./jobs:/opt/spark/jobs
      - ./data:/opt/spark/data
      - ./output:/opt/spark/output

networks:
  de_net:
    driver: bridge
```

### 8.4 컨테이너 접속 및 Python 확인

```bash
docker exec -it spark-master bash

python --version
```

### 8.5 Example 파일 실행

```python
from pyspark.sql import SparkSession

# SparkSession 생성
spark = SparkSession.builder \
    .appName("Example") \
    .getOrCreate()

# 간단한 데이터 생성
data = [
    ("Alice", 20),
    ("Bob", 30),
    ("Cathy", 40)
]
columns = ["name", "age"]

# DataFrame 생성
df = spark.createDataFrame(data, columns)

# 결과 출력
df.show()

# Spark 종료
spark.stop()
```

```bash
# 도커 외부
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/jobs/example.py

# 도커 내부
/opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/jobs/example.py

# 결과화면
+-----+---+
| name|age|
+-----+---+
|Alice| 20|
|  Bob| 30|
|Cathy| 40|
+-----+---+
```