# Hadoop MapReduce (Split → Map → Shuffle & Sort → Reduce → 최종 출력) 실습

## 실행 위치
호스트에서 `docker exec -it namenode bash`로 `namenode` 컨테이너에 접속한 뒤, 실습 데이터 디렉터리로 이동해서 실행합니다.

```bash
cd /workspace
```


## 1. 로컬 파일을 HDFS에 업로드
```bash
hadoop fs -put input.txt /user/hadoop/input/
```

### 파일 목록 및 크기 확인
```bash
hadoop fs -ls /user/hadoop/input/
```

## 2. Split 정보 확인
```bash
hdfs fsck /user/hadoop/input/input.txt -files -blocks
```

## 3. WordCount 실행 (Mapper + Reducer)
```bash
hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.5.jar \
    wordcount /user/hadoop/input/input.txt /user/hadoop/output/map_output
```

## 4. 결과 확인 (최종 출력)
```bash
hadoop fs -cat /user/hadoop/output/map_output/part-r-00000
```

## 제출 캡처
아래 핵심 결과 화면 3개를 캡처해 제출합니다.
- image1: `hadoop fs -ls /user/hadoop/input/` 입력 파일 업로드 확인 화면
- image2: `hdfs fsck` Split 정보 확인 화면
- image3: WordCount 최종 출력 파일 내용 화면
