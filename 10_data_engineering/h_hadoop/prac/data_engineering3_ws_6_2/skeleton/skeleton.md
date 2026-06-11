# Hadoop Docker 클러스터 실행 실습

## 실행 위치
호스트의 `/home/ssafy/ssafy_hadoop/lecture_code/files` 디렉터리가 `namenode` 컨테이너 내부의 `/workspace`로 마운트됩니다. Docker Compose는 호스트 터미널에서 실행하고, Hadoop 명령은 `namenode` 컨테이너 내부에서 실행합니다.


## 1. Docker Compose 위치로 이동

## 2. Hadoop 클러스터 실행
```bash
docker compose up -d --build
```

## 3. 실행 컨테이너 확인
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

## 4. NameNode 컨테이너에서 Hadoop 설정 확인
```bash
docker exec -it namenode bash
hdfs getconf -confKey fs.defaultFS
hdfs getconf -confKey dfs.replication
echo $HADOOP_HOME
```

## 5. 웹 UI 확인
- NameNode UI: http://localhost:9870
- ResourceManager UI: http://localhost:8088
- DataNode UI: http://localhost:9864, http://localhost:9865

## 제출 캡처
아래 핵심 결과 화면 3개를 캡처해 제출합니다.
- image1: `docker ps` Hadoop 컨테이너 목록 화면
- image2: `hdfs getconf -confKey fs.defaultFS` 설정 조회 화면
- image3: NameNode UI 접속 화면
