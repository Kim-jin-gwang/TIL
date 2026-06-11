# HDFS 파일 업로드, 조회, 삭제, 목록 확인 실습

## 실행 위치
호스트에서 `docker exec -it namenode bash`로 `namenode` 컨테이너에 접속한 뒤, problem_2 디렉터리에서 실행합니다. problem_1에서 `transactions.csv`를 먼저 HDFS에 업로드한 상태여야 합니다.

```bash
cd /workspace
```


## 1. HDFS에 transactions.csv 내용 확인
```bash
hdfs dfs -cat /user/local/hadoop_data/transactions.csv
```

## 2. HDFS에 note.txt 업로드
```bash
hdfs dfs -put note.txt /user/local/hadoop_data/
```

## 3. 업로드된 note.txt 내용 확인
```bash
hdfs dfs -cat /user/local/hadoop_data/note.txt
```

## 4. note.txt 파일 삭제
```bash
hdfs dfs -rm /user/local/hadoop_data/note.txt
```

## 5. /user/local/hadoop_data 디렉토리 내 파일 목록 확인
```bash
hdfs dfs -ls /user/local/hadoop_data/
```

### 출력 예시:
```
Found 1 items
-rw-r--r--   1 futura supergroup        453 2025-08-12 23:53 /user/local/hadoop_data/transactions.csv
```

## 제출 캡처
아래 핵심 결과 화면 2개를 캡처해 제출합니다.
- image1: 업로드된 `note.txt` 내용 확인 화면
- image2: `note.txt` 삭제 후 HDFS 목록 화면
