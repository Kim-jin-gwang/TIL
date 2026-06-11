# HDFS 파일 정보 확인 실습

## 실행 위치
호스트에서 `docker exec -it namenode bash`로 `namenode` 컨테이너에 접속한 뒤, 실습 데이터 디렉터리로 이동해서 실행합니다. 먼저 `finance.csv`를 HDFS에 업로드합니다.

```bash
cd /workspace
hdfs dfs -mkdir -p /user/local/hadoop_data
hdfs dfs -put -f finance.csv /user/local/hadoop_data/finance.csv
```


## 1. finance.csv 파일 내용 확인
```bash
hdfs dfs -cat /user/local/hadoop_data/finance.csv
```

## 2. finance.csv 파일 메타 정보 확인

### (1) 블록 수, 파일 수, 용량 확인
```bash
hdfs dfs -count /user/local/hadoop_data/finance.csv
```

### 출력 예시
```
0          1           453 /user/local/hadoop_data/finance.csv
```

### (2) 파일 용량 확인 (요약)
```bash
hdfs dfs -du -s /user/local/hadoop_data/finance.csv
```

### 출력 예시
```
453  453  /user/local/hadoop_data/finance.csv
```

### (3) 파일 상태 확인 (최종 수정 시간 등)
```bash
hdfs dfs -stat /user/local/hadoop_data/finance.csv
```

### 출력 예시
```
2025-05-12 14:53:32
```

## 제출 캡처
아래 핵심 결과 화면 4개를 캡처해 제출합니다.
- image1: `finance.csv` 내용 확인 화면
- image2: `hdfs dfs -count` 메타 정보 화면
- image3: `hdfs dfs -du -s` 파일 용량 화면
- image4: `hdfs dfs -stat` 파일 상태 화면
