# Docker 기반 Hadoop 컨테이너 상태 확인 실습

## 실행 위치
`docker ps`는 호스트 터미널에서 실행합니다. `docker exec -it namenode bash` 이후 명령은 `namenode` 컨테이너 내부에서 실행합니다.


## 1. Hadoop 컨테이너 실행 상태 확인
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

## 2. NameNode 컨테이너 접속
```bash
docker exec -it namenode bash
```

## 3. 컨테이너 내부 SSH 서비스 상태 확인
```bash
service ssh status
```

## 4. Hadoop 환경 변수 확인
```bash
echo $HADOOP_HOME
echo $JAVA_HOME
echo $PATH | grep hadoop
```

## 5. 컨테이너 간 통신 확인
```bash
ping -c 2 datanode1
ping -c 2 datanode2
```

## 제출 캡처
아래 핵심 결과 화면 4개를 캡처해 제출합니다.
- image1: `docker ps` 컨테이너 실행 상태 화면
- image2: `echo $HADOOP_HOME` 환경 변수 확인 화면
- image3: `ping -c 2 datanode1` 통신 확인 화면
- image4: `ping -c 2 datanode2` 통신 확인 화면
