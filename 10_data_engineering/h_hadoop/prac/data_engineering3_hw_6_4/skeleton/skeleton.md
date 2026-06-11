# 설정 파일 적용 확인 및 환경 점검 실습

## 실행 위치
호스트에서 `docker exec -it namenode bash`로 `namenode` 컨테이너에 접속한 뒤 실행합니다.


## 1. core-site.xml, hdfs-site.xml 에 설정한 값 확인
```bash
# core-site.xml에서 설정한 fs.defaultFS 값 확인
hdfs getconf -confKey fs.defaultFS

# hdfs-site.xml에서 설정한 NameNode 저장 경로 확인
hdfs getconf -confKey dfs.namenode.name.dir

# hdfs-site.xml에서 설정한 DataNode 저장 경로 확인
hdfs getconf -confKey dfs.datanode.data.dir
```

## 2. 환경 변수 확인
```bash
# HADOOP_HOME 환경 변수 확인
echo $HADOOP_HOME

# HADOOP_CONF_DIR 환경 변수 확인
echo $HADOOP_CONF_DIR

# PATH 환경 변수 중 hadoop 관련 경로 확인
echo $PATH | grep hadoop
```

## 3. JAVA_HOME이 hadoop-env.sh에 반영되었는지 확인
```bash
# JAVA_HOME 설정이 포함되어 있는지 확인
grep JAVA_HOME $HADOOP_HOME/etc/hadoop/hadoop-env.sh  
```

## 4. Hadoop 구성 점검 (hdfs 명령어 정상 동작 여부)
```bash
# HDFS 루트 디렉토리 리스트 확인
hdfs dfs -ls /
```

## 제출 캡처
아래 핵심 결과 화면 4개를 캡처해 제출합니다.
- image1: `fs.defaultFS` 설정 조회 화면
- image2: `HADOOP_HOME` 환경 변수 확인 화면
- image3: `hadoop-env.sh`의 `JAVA_HOME` 설정 확인 화면
- image4: `hdfs dfs -ls /` 명령 실행 화면
