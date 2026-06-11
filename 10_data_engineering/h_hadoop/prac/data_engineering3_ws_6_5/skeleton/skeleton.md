# HDFS 복제와 블록 위치 분석 실습

## 실행 위치
호스트에서 `docker exec -it namenode bash`로 `namenode` 컨테이너에 접속한 뒤 실행합니다. 실습 파일은 컨테이너 내부에서 직접 생성합니다.

```bash
cd /workspace
```

## 1. HDFS 복제 설정과 블록 크기 확인
강의안의 HDFS 구조에서 NameNode는 파일 메타데이터를 관리하고, DataNode는 실제 블록을 저장합니다. 먼저 현재 클러스터의 복제 수와 블록 크기 설정을 확인합니다.

```bash
hdfs getconf -confKey dfs.replication
hdfs getconf -confKey dfs.blocksize
```

## 2. 분석용 파일 생성 후 HDFS 업로드
컨테이너 내부에 분석용 텍스트 파일을 만들고 HDFS에 업로드합니다.

```bash
mkdir -p /workspace/hdfs_lv5
seq 1 2000 > /workspace/hdfs_lv5/block_source.txt

hadoop fs -mkdir -p /user/hadoop/lv5
hadoop fs -put -f /workspace/hdfs_lv5/block_source.txt /user/hadoop/lv5/block_source.txt
```

## 3. NameNode가 관리하는 파일 메타데이터 확인
파일 목록과 `stat` 결과를 확인하여 HDFS 경로, 복제 수, 블록 크기, 파일 크기를 확인합니다.

```bash
hadoop fs -ls /user/hadoop/lv5
hadoop fs -stat "replication=%r block_size=%o size=%b modified=%y" /user/hadoop/lv5/block_source.txt
```

## 4. 블록 위치와 복제 배치 확인
`fsck` 결과에서 파일이 어떤 블록으로 관리되는지, 각 블록이 어느 DataNode에 저장되는지 확인합니다.

```bash
hdfs fsck /user/hadoop/lv5/block_source.txt -files -blocks -locations
```

## 5. DataNode 상태 확인
`dfsadmin -report`를 통해 Live DataNode 수와 각 DataNode의 저장소 상태를 확인합니다.

```bash
hdfs dfsadmin -report
```

## 정리 질문
아래 내용을 짧게 정리합니다.

1. `dfs.replication` 값과 `fsck`의 블록 위치 개수가 일치하는지 확인합니다.
2. NameNode가 직접 파일 내용을 저장하지 않고 메타데이터를 관리한다는 점을 설명합니다.
3. DataNode가 실제 블록을 저장하고 NameNode에 상태를 보고한다는 점을 설명합니다.

## 제출 캡처
아래 핵심 결과 화면 4개를 캡처해 제출합니다.
- image1: `dfs.replication` 설정 조회 화면
- image2: `hadoop fs -stat` 파일 메타데이터 화면
- image3: `hdfs fsck` 블록 위치 화면
- image4: `hdfs dfsadmin -report` Live DataNode 화면
