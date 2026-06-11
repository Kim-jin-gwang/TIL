# Hadoop 데몬 실행 및 상태 확인 실습

## 실행 위치
모든 명령은 호스트 터미널에서 `docker exec ...` 형태로 실행합니다.


## 1. 컨테이너별 Java 프로세스 확인
```bash
docker exec namenode jps
docker exec datanode1 jps
docker exec datanode2 jps
```

## 2. HDFS 상태 확인
```bash
docker exec namenode hdfs dfsadmin -report
```

## 3. YARN NodeManager 상태 확인
```bash
docker exec namenode yarn node -list
```

## 4. ResourceManager 웹 UI 확인
브라우저에서 http://localhost:8088 접속 후 노드 상태를 확인합니다.

## 제출 캡처
아래 핵심 결과 화면 4개를 캡처해 제출합니다.
- image1: `docker exec namenode jps` Java 프로세스 확인 화면
- image2: `docker exec namenode hdfs dfsadmin -report` HDFS 상태 화면
- image3: `docker exec namenode yarn node -list` NodeManager 상태 화면
- image4: ResourceManager 웹 UI 노드 상태 화면
