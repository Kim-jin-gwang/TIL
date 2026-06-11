# YARN 작업 상태 확인 및 장애 상황 분석 실습 - Answer

## 실행 위치
장애 유도 실습입니다. `docker exec -it datanode1 bash`로 `datanode1`에 접속해 NodeManager PID를 확인하고 종료합니다. 작업 실행과 YARN 확인은 `namenode` 컨테이너에서 진행합니다.


## 1. NodeManager 장애 유도 및 로그 분석

### jps로 NodeManager PID 확인 후 종료
```bash
docker exec -it datanode1 bash
jps
kill -9 <NodeManager PID>
jps
```

### 장애 유도를 위한 작업 실행
```bash
docker exec -it namenode bash
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar pi 20 10000
```

## 2. NodeManager 재시작 후 상태 확인
```bash
exit
docker exec datanode1 bash -lc "yarn --daemon start nodemanager"
docker exec datanode1 jps
```

### 실패 또는 대기 상태에서 로그 확인
```bash
yarn application -list -appStates RUNNING,ACCEPTED,FAILED
yarn logs -applicationId <application_id> # application_1756269082638_0001
```

## 3. 동일한 작업 재실행
```bash
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar pi 20 10000
```

### YARN 애플리케이션 상태 확인
```bash
yarn application -list -appStates ALL
```

## 제출 캡처
아래 핵심 결과 화면 5개를 캡처해 제출합니다.
- image1: NodeManager 종료 후 `jps` 확인 화면
- image2: 장애 상태의 YARN 애플리케이션 목록 화면
- image3: 장애 애플리케이션 로그 확인 화면
- image4: NodeManager 재시작 후 `jps` 확인 화면
- image5: Pi 작업 재실행 성공 화면
