# Hadoop HDFS 기본 명령어 실습

## 실행 위치
호스트에서 `docker exec -it namenode bash`로 `namenode` 컨테이너에 접속한 뒤, 실습 데이터가 있는 디렉터리로 이동해서 실행합니다.

```bash
cd /workspace
```


## 1. HDFS 디렉터리 생성
```bash
hadoop fs -mkdir -p /user/hadoop/input/
```

## 2. 로컬 파일(test.txt)을 HDFS 경로로 업로드
```bash
hadoop fs -put test.txt /user/hadoop/input/
```

## 3. 업로드된 HDFS 파일(test.txt)의 내용 확인
```bash
hadoop fs -cat /user/hadoop/input/test.txt
```

## 4. HDFS 파일을 로컬 /tmp/downloads 경로로 다운로드
```bash
# 컨테이너 내부 /tmp 경로에 downloads 폴더 생성
mkdir -p /tmp/downloads

# 파일 다운로드
hadoop fs -get /user/hadoop/input/test.txt /tmp/downloads
```

## 5. 로컬에 다운로드 된 (“test.txt”) 파일이 있는지 목록 확인
```bash
ls /tmp/downloads
```

## 6. HDFS 경로 내 파일 및 디렉터리 목록 확인
```bash
hadoop fs -ls /user/hadoop/input
```

## 7. HDFS에서 test.txt 파일 삭제
```bash
hadoop fs -rm /user/hadoop/input/test.txt
```

## 8. HDFS 경로 내 test.txt 파일이 삭제됐는지 디렉터리 목록 확인
```bash
hadoop fs -ls /user/hadoop/input
```

## 제출 캡처
아래 핵심 결과 화면 3개를 캡처해 제출합니다.
- image1: `hadoop fs -cat /user/hadoop/input/test.txt` 업로드 파일 내용 화면
- image2: `ls /tmp/downloads` 다운로드 파일 확인 화면
- image3: `hadoop fs -ls /user/hadoop/input` 삭제 후 목록 화면
