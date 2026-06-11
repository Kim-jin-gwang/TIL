# HDFS를 활용한 금융 데이터 CSV 업로드 및 다운로드 실습

## 실행 위치
호스트에서 `docker exec -it namenode bash`로 `namenode` 컨테이너에 접속한 뒤, 실습 데이터 디렉터리로 이동해서 실행합니다.

```bash
cd /workspace
```


## 1. HDFS 디렉토리 생성
```bash
hdfs dfs -mkdir -p /user/local/hadoop_data
```

## 2. 로컬 CSV 파일 업로드 (transactions.csv)
```bash
hdfs dfs -put transactions.csv /user/local/hadoop_data/
hdfs dfs -ls /user/local/hadoop_data/transactions.csv
```

## 3. HDFS에서 로컬로 파일 다운로드
```bash
mkdir -p ~/backup
hdfs dfs -get /user/local/hadoop_data/transactions.csv ~/backup/
```

## 4. 다운로드한 파일 내용 확인
```bash
cat ~/backup/transactions.csv
```

## 제출 캡처
아래 핵심 결과 화면 2개를 캡처해 제출합니다.
- image1: HDFS에 업로드된 `transactions.csv` 목록 확인 화면
- image2: 다운로드한 `transactions.csv` 내용 확인 화면
