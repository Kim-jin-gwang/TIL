# 사용자 정의 WordCount 실행 실습

## 실행 위치
호스트에서 `docker exec -it namenode bash`로 `namenode` 컨테이너에 접속한 뒤, skeleton 디렉터리에서 실행합니다. 입력 CSV는 `shopping_transactions.csv` 경로를 사용합니다.

```bash
cd /workspace
```


## 1. 입력 파일 업로드
```bash
hadoop fs -put shopping_transactions.csv /user/hadoop/input/
hadoop fs -ls /user/hadoop/input/
hadoop fs -cat /user/hadoop/input/shopping_transactions.csv | head -10
```

## 2. 사용자 정의 WordCount 실행 (Product 기준)

### mapper_answer.py
- CSV의 3번째 필드(Product)를 기준으로 `<product, 1>` 출력

### reducer_answer.py
- 동일한 key별로 개수 합산

```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /user/hadoop/input/shopping_transactions.csv \
  -output /user/hadoop/output/wordcount_custom \
  -mapper "python3 mapper_skeleton.py" \
  -reducer "python3 reducer_skeleton.py" \
  -file mapper_skeleton.py \
  -file reducer_skeleton.py
```

## 3. 결과 확인
```bash
hadoop fs -cat /user/hadoop/output/wordcount_custom/part-* | sort -k2 -nr | head -10
```

## 제출 캡처
아래 핵심 결과 화면 2개를 캡처해 제출합니다.
- image1: `shopping_transactions.csv` HDFS 업로드 확인 화면
- image2: 사용자 정의 Streaming 빈도 상위 결과 화면
