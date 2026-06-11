
# Hadoop 클러스터 및 YARN 스케줄링 가이드

Hadoop의 분산 클러스터 구조 및 YARN 기반 리소스 스케줄링 구조를 이해하고, 실습을 통해 스케줄러를 변경하고 확인하는 과정을 정리합니다.

---

## 1. 클러스터 개요 및 구성

### 클러스터란?

- 여러 대의 서버(노드)가 하나의 시스템처럼 동작
- 대용량 데이터를 병렬 처리하기 위한 필수 구조
- Hadoop에서는 HDFS + YARN + MapReduce/Spark 등의 형태로 구성

---

## 2. Hadoop 클러스터 구성 요소

| 계층 | 구성요소 | 역할 |
|---|---|---|
| 스토리지 | NameNode | HDFS 메타데이터 관리 |
| 스토리지 | DataNode | 실제 데이터 블록 저장 |
| 컴퓨팅 | ResourceManager | 클러스터 전체 자원 관리 및 스케줄링 |
| 컴퓨팅 | NodeManager | 각 노드의 컨테이너 실행 및 자원 상태 보고 |
| 클라이언트 | 사용자 또는 프로그램 | 작업 제출 및 결과 확인 |

- NameNode는 파일 이름, 디렉토리 구조, 블록 위치 등의 메타데이터를 관리
- DataNode는 실제 데이터 블록을 저장 
- ResourceManager는 클러스터 전체의 CPU, 메모리 등의 자원을 관리
- NodeManager는 각 워커 노드에서 컨테이너를 실행하고 상태를 보고

---

## 3. HDFS의 핵심 특징

- 블록 단위 저장: 파일을 일정한 크기의 블록으로 나누어 저장
- 복제 저장: 장애에 대비하기 위해 각 블록을 여러 개의 복제본으로 저장
- 데이터 무결성: 수정 불가, 병렬 처리에 적합
- 배치 최적화: 대용량 데이터를 순차적으로 처리

---

## 4. Hadoop V1 vs V2 비교

| 항목 | Hadoop V1 | Hadoop V2 (YARN) |
|------|-----------|------------------|
| 자원/작업 관리 | JobTracker 단일 처리 | ResourceManager + AppMaster 분산 처리 |
| 확장성 | 낮음 | 높음 |
| 장애 대응 | JobTracker에 부하 집중 | 역할 분리로 장애 영향 완화, HA 구성 가능 |
| 지원 엔진 | MapReduce | MR, Spark, Flink, Hive 등 |

---

## 5. YARN 구조 및 역할

| 용어 | 설명 |
|------|------|
| ResourceManager (RM) | 클러스터 전체 자원을 관리. 모든 ApplicationMaster를 통제 |
| NodeManager (NM) | 각 노드에 존재하며, 컨테이너 실행과 노드 자원 상태 보고를 담당 |
| Container | NM이 실행하는 작업 공간 (CPU, 메모리 포함). 하나의 Mapper, Reducer, Spark Executor 등이 실행됨 |
| ApplicationMaster (AM) | 각 Job의 전용 관리자. 작업 흐름 관리 및 컨테이너 요청 수행 |
| Client | Job을 제출하는 사용자 또는 프로그램 |

Note  
- Container ≠ Node  
- 컨테이너는 노드 위에 동적으로 생성되는 작업 실행 단위이며, 하나의 물리 노드에는 여러 컨테이너가 생성될 수 있음

---

## 6. MapReduce on YARN 실행 구조 예시

Hadoop V2부터 MapReduce는 YARN 위에서 실행되며, 아래와 같은 실행 구조

```
[사용자]
   ↓ (hadoop jar ...)
[ResourceManager] ← ApplicationMaster 실행 요청
   ↓
[NodeManager] → ApplicationMaster 실행 (Container 1)
   ↓
[ApplicationMaster] → ResourceManager에 Mapper/Reducer 실행 요청
   ↓
[여러 NodeManager들] → Mapper/Reducer 실행 (Container 2, 3, ...)
```

- ApplicationMaster는 MapReduce Job마다 하나씩 생성되며, 전체 작업 흐름(Mapper/Reducer 스케줄링)을 관리
- Mapper와 Reducer는 각각 별도의 컨테이너에서 실행
- 입력 데이터는 HDFS에서 읽고, 출력 역시 HDFS에 저장
- Shuffle 단계에서 Mapper의 출력이 네트워크를 통해 Reducer에게 전달되며, 이 과정에서 병목이 발생할 수 있음

### 특징

| 항목 | 설명 |
|------|------|
| 작업 조정 역할 | MapReduce ApplicationMaster가 수행 |
| 실행 단위 | Mapper, Reducer 각각 YARN Container로 실행 |
| 병렬성 | Mapper 개수 = 입력 스플릿 수, Reducer 개수는 사용자가 지정 가능 |
| 입출력 | 모두 HDFS 기반 |
| 통신 | Shuffle 시 네트워크 전송 발생 (Mapper → Reducer) |


## 7. 작업 간 통신 및 데이터 흐름

### Container 간 통신

- Mapper → Reducer 간 Shuffle 단계에서 네트워크 통신 발생
- 이때 Container 간 데이터가 전송되며, 디스크 I/O와 네트워크 병목의 주요 지점

### DataNode 간 통신

- 읽기 작업에서는 Client가 필요한 블록을 가진 DataNode로부터 직접 데이터를 읽음
- 쓰기 작업에서는 복제본 생성을 위해 DataNode 간 파이프라인 방식의 데이터 전달이 발생할 수 있음
- NameNode는 데이터 자체를 전달하지 않고, 블록 위치와 메타데이터를 관리함

---

## 8. YARN 작업 실행 흐름

1. 클라이언트 → ResourceManager에 Job 제출
2. NM이 ApplicationMaster 실행
3. RM이 AM에게 Container 위치 지정
4. AM이 NM에게 작업 실행 요청
5. 실행 후 상태 업데이트 및 결과 수신

---

## 9. YARN 스케줄링 필요성

- 여러 Job을 동시에 처리하려면 자원 충돌 최소화 필요
- 자원 효율성 및 응답속도 최적화를 위해 필요
- 스케줄링 없으면 자원 독점, 작업 지연, 성능 저하

---

## 10. YARN 설정

### 10.1 yarn-site.xml

```xml
<configuration>
  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>namenode</value>
  </property>
  
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
```

### 10.2 yarn 기반 실행 테스트

1. HDFS에 디렉토리 생성 및 업로드
```bash
# 입력 파일 생성
echo "Hello World Hello SSAFY" > test.txt

# HDFS에 디렉토리 생성 및 파일 업로드
hdfs dfs -mkdir -p /user/hadoop/input
hdfs dfs -put -f test.txt /user/hadoop/input/

# 업로드 확인
hdfs dfs -ls /user/hadoop/input
```

2. YARN 위에서 MapReduce 실행
```bash
hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.5.jar \
  wordcount /user/hadoop/input/test.txt /user/hadoop/output/map_output
```

### Application 목록 확인

```bash
yarn application -list -appStates ALL
```

### 개별 Job 로그 확인

```bash
yarn logs -applicationId <application_id>
```

로그 위치: $HADOOP_HOME/logs/

---

## 11. YARN 스케줄러 종류 및 설정

### (1) FIFO 스케줄러 (기본값) - yarn-site.xml

```xml
<property>
  <name>yarn.resourcemanager.scheduler.class</name>
  <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.fifo.FifoScheduler</value>
</property>
```

- 장점: 단순함
- 단점: 긴 작업이 자원 독점 가능

---

### (2) Capacity 스케줄러

```xml
<property>
  <name>yarn.resourcemanager.scheduler.class</name>
  <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.capacity.CapacityScheduler</value>
</property>
```

- 큐(Queue)별 자원을 비율로 분할

> capacity-scheduler.xml 예시

```xml
<!-- 기본 설정 (Configured Capacity): 큐에 할당된 자원 비율 -->
<property>
  <name>yarn.scheduler.capacity.root.default.capacity</name>
  <value>100</value>  <!-- 기본 자원 100% -->
</property>

<!-- 최대 설정 (Maximum Capacity): 큐가 점유할 수 있는 최대치 -->
<property>
  <name>yarn.scheduler.capacity.root.default.maximum-capacity</name>
  <value>100</value>  <!-- 최대 100%까지 확장 가능 -->
</property>
```

---

### (3) Fair 스케줄러

```xml
<property>
  <name>yarn.resourcemanager.scheduler.class</name>
  <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.fair.FairScheduler</value>
</property>
```

- 자원을 사용자 간 공정하게 나눔
- 작업 독점 방지에 유리

---

## 12. 스케줄러 변경 적용 방법

### Docker 환경에서 변경하는 예시 (Capacity)

docker exec namenode bash

```bash
cat > $HADOOP_HOME/etc/hadoop/yarn-site.xml <<'EOF'
<configuration>
  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>namenode</value>
  </property>

  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>

  <property>
    <name>yarn.resourcemanager.scheduler.class</name>
    <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.capacity.CapacityScheduler</value>
  </property>
</configuration>
EOF
```

```bash
docker exec namenode bash -lc "yarn --daemon stop resourcemanager; sleep 2; yarn --daemon start resourcemanager; jps"
docker exec datanode1 bash -lc "yarn --daemon stop nodemanager; sleep 2; yarn --daemon start nodemanager; jps"
docker exec datanode2 bash -lc "yarn --daemon stop nodemanager; sleep 2; yarn --daemon start nodemanager; jps"
```

변경 확인

```bash
cat $HADOOP_HOME/etc/hadoop/yarn-site.xml | grep scheduler.class -A1
```

---
