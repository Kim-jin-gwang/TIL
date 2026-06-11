# 내장 WordCount 실행 실습

## 실행 위치
호스트에서 `docker exec -it namenode bash`로 `namenode` 컨테이너에 접속한 뒤, 과제 데이터 디렉터리로 이동해서 실행합니다.

```bash
cd /workspace
```


## 1. 입력 파일 업로드
```bash
hadoop fs -put shopping_transactions.csv /user/hadoop/input/
hadoop fs -ls /user/hadoop/input/
hadoop fs -cat /user/hadoop/input/shopping_transactions.csv | head -10
```

## 2. 내장 WordCount 실행
```bash
hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
  wordcount /user/hadoop/input/shopping_transactions.csv /user/hadoop/output/wordcount_builtin
```

## 3. 결과 확인
```bash
hadoop fs -cat /user/hadoop/output/wordcount_builtin/part-* | sort -k2 -nr | head -10
```

## 제출 캡처
아래 핵심 결과 화면 2개를 캡처해 제출합니다.
- image1: `shopping_transactions.csv` HDFS 업로드 확인 화면
- image2: 내장 WordCount 빈도 상위 결과 화면
