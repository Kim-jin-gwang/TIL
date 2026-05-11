# Apache Flink 1.19 설치 및 설정 

## 1. Flink 설치 및 권한 설정

```bash

# Flink 1.19 다운로드 및 압축 해제
cd /home/ssafy
wget https://archive.apache.org/dist/flink/flink-1.19.3/flink-1.19.3-bin-scala_2.12.tgz
tar -xvzf flink-1.19.3-bin-scala_2.12.tgz
mv flink-1.19.3 flink

echo 'export FLINK_HOME=/home/ssafy/flink' >> ~/.bashrc
echo 'export PATH=$FLINK_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

## 2. Flink 설정 변경

```bash
cd /home/ssafy/flink
cd conf
vi config.yaml
```

다음 항목들을 추가 또는 수정(파일 제공된거 복사 붙여넣기 권장)

```yaml
jobmanager.bind-host: 0.0.0.0
rest.bind-address: 0.0.0.0
```

## 3. 클러스터 시작 및 UI 접속

```bash
cd /home/ssafy/flink/bin
./start-cluster.sh
```

- 웹 UI 접속: [http://localhost:8081](http://localhost:8081)

> 실행 시 `localhost`가 아닌 `Desktop-xxxx`와 같은 이름으로 뜰 수 있음  
> 이는 **WSL의 네트워크 구조** 때문입니다.
> 이를 통한 이슈를 없애고자 binding 설정을 사용합니다.

---

## WSL2 네트워크 구조 이해

### localhost란?

- `127.0.0.1`: 내 컴퓨터 내부에서만 접근 가능한 주소
- **“이 컴퓨터에서만 들어올 수 있는 문”**

### 0.0.0.0이란?

- “이 컴퓨터가 가진 **모든 네트워크 인터페이스에 대해 열어줌**”
- 즉, `localhost`, 내부 IP, 외부 IP 모두 포함

### WSL1 vs WSL2

| 항목 | WSL1 | WSL2 |
|------|------|------|
| 네트워크 공유 | Windows와 IP 공유 | 가상 네트워크 (IP 분리) |
| localhost 공유 | 가능 | 기본 불가능 (포트포워딩 필요) |
| 해결 방법 | 기본 공유됨 | `0.0.0.0` 바인딩 필수 |

### WSL2에서 0.0.0.0을 써도 괜찮은가?

- 대부분 NAT(Network Address Translation)로 외부에서 접근 불가
- Windows에서 보안 관리하므로, WSL 내에서 포트 개방은 상대적으로 안전
- Windows 브라우저에서 WSL 서버에 접속하려면 `0.0.0.0` 필수

---


## Socket 예제 실행

```bash
# 포트 확인
nc -l 9000  # 또는 9000 등 비어 있는 포트 확인

# 예제 실행
cd /home/ssafy/flink/
./bin/flink run examples/streaming/SocketWindowWordCount.jar --hostname localhost --port 9000
```

---

## Flink 로그 실시간 확인

```bash
cd /home/ssafy/flink/
tail -f log/flink-*.out
```

### tail 옵션 설명

- `tail`: 파일 마지막 부분 출력
- `-f`: 파일 변경사항을 실시간으로 추적하며 출력
- `log/flink-*.out`: Flink 로그 파일 전체 지정 (`standalonesession`, `taskexecutor` 등 포함)

---

## Flink 클러스터 종료

```bash
./stop-cluster.sh
```

---

## Docker를 통한 Flink 띄우기

### 1. 프로젝트 구조

```
ssafy_flink/
├── Dockerfile
├── docker-compose.yml
├── pyflink_job.py  ← 실행할 PyFlink 코드
```

---

### 2. Dockerfile – PyFlink 실행 환경 이미지 만들기

```dockerfile
FROM flink:1.19-scala_2.12-java17

# 2. Python & pip 설치 + PyFlink 설치
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip install --no-cache-dir apache-flink==1.19.3 && \
    pip install pandas

# 3. 기본 Python3 링크 설정
RUN ln -s /usr/bin/python3 /usr/bin/python

# 4. 작업 디렉토리 설정
WORKDIR /opt/flink

```

---

### 3. docker-compose.yml – Flink 클러스터 구성 기본구조

```yaml
services:
  jobmanager:
    build: .
    image: pyflink
    container_name: flink_jobmanager
    hostname: jobmanager
    ports:
      - "8081:8081"
    command: jobmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager
    volumes:
      - ./workspace:/opt/flink/workspace

  taskmanager:
    build: .
    image: pyflink
    container_name: flink_taskmanager
    depends_on:
      - jobmanager
    command: taskmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager
    volumes:
      - ./workspace:/opt/flink/workspace
      
```

---

### 3-1. docker-compose.yml – Flink 클러스터 구성 2 TaskManager

```yaml
services:
  jobmanager:
    build:
      context: .
      dockerfile: Dockerfile
    image: pyflink
    container_name: flink_jobmanager
    hostname: jobmanager
    ports:
      - "8081:8081"
    command: jobmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager
    volumes:
      - ./workspace:/opt/flink/workspace

  taskmanager1:
    build:
      context: .
      dockerfile: Dockerfile
    image: pyflink
    container_name: flink_taskmanager1
    depends_on:
      - jobmanager
    command: taskmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager
    volumes:
      - ./workspace:/opt/flink/workspace

  taskmanager2:
    build:
      context: .
      dockerfile: Dockerfile
    image: pyflink
    container_name: flink_taskmanager2
    depends_on:
      - jobmanager
    command: taskmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager
    volumes:
      - ./workspace:/opt/flink/workspace

```

---
### 4. PyFlink Job 예제 (pyflink_job.py)

```python
from pyflink.datastream import StreamExecutionEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

data = env.from_collection([("apple", 1), ("banana", 1), ("apple", 1)])
data.print()

env.execute("PyFlink Docker Job")
```

---

### 5. 실행 순서

#### 1. Docker 이미지 빌드
```bash
docker build -t pyflink .
```

#### 2. 클러스터 실행
```bash
docker-compose up
```

#### 3. JobManager 컨테이너에서 실행
```bash
docker exec -it flink_jobmanager python /opt/flink/workspace/pyflink_job.py
```

```bash
docker exec -it flink_jobmanager bash
python /opt/flink/workspace/pyflink_job.py
```

---

### 6. PyFlink Job 실행 방식 (flink run 기준)

PyFlink 코드는 Python으로 직접 실행할 수도 있지만, 실제 Flink 클러스터에 Job을 제출하는 방식은 `flink run -py` 형태
 
#### 6.1 Docker 내부에서 flink run 실행 (권장)

```bash
docker compose up -d
docker exec -it flink_jobmanager /opt/flink/bin/flink run -py /opt/flink/workspace/pyflink_job.py
```

또는

```bash
docker exec -it flink_jobmanager bash
/opt/flink/bin/flink run -py /opt/flink/workspace/pyflink_job.py
```

결과 확인:

```bash
docker logs -f flink_taskmanager
docker logs -f flink_taskmanager1
docker logs -f flink_taskmanager2
```

#### 6.2 로컬에서 Docker Flink 클러스터로 Job 제출

```bash
cd /home/ssafy/ssafy_flink/workspace
flink run -m localhost:8081 -py ./pyflink_job.py
```

- Flink CLI 설치 필요
- docker-compose에서 8081 포트 열려 있어야 함

동작 구조:

```
로컬 Flink CLI → localhost:8081(JobManager)로 Job 제출 → Docker TaskManager에서 실행
```

#### 6.3 파일 경로 주의

Docker 내부 실행 시:

```python
pd.read_csv("/opt/flink/workspace/data/data.csv")
```

로컬 실행 시:

```python
pd.read_csv("./data/data.csv")
```

안전한 방식:

```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "data" / "data.csv")
```

#### 6.4 병렬성(Parallelism)과 Slot 주의

```python
env.set_parallelism(2)
```

- 병렬성만큼 Slot 필요
- 부족 시 에러: `NoResourceAvailableException: Could not acquire the minimum required resources.`

해결 방법:

1. 병렬성 낮추기

```python
env.set_parallelism(1)
```

2. TaskManager slot 늘리기

```yaml
taskmanager:
  environment:
    - |
      FLINK_PROPERTIES=
      taskmanager.numberOfTaskSlots: 2
```

3. TaskManager 추가

```bash
docker compose up -d --scale taskmanager=2
```

#### 6.5 실행 방식 비교

| 방식 | 실행 명령 | 특징 |
|------|--------|------|
| Python 직접 실행 | python pyflink_job.py | 단순 테스트 |
| Docker 내부 실행 | flink run -py | 안정적, 권장 |
| 로컬 → Docker 제출 | flink run -m localhost:8081 | 실제 운영 구조와 유사 |

#### 6.6 핵심 정리

- PyFlink는 Python으로 작성하지만 실제 클러스터 실행은 `flink run -py`로 수행
- Docker 내부 실행 → 컨테이너 경로 기준, 로컬 제출 → 로컬 경로 기준
- Flink는 병렬성만큼 Slot 필요
