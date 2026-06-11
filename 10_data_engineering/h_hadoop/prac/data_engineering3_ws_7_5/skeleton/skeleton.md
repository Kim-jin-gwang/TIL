# YARN 스케줄러 확인 및 Pi 계산 프로그램 실행 실습

## 실행 위치
모든 명령은 호스트 터미널에서 `docker exec ...` 형태로 실행합니다.


Docker 실습 환경은 `CapacityScheduler`를 기본값으로 사용합니다.  
FIFO/Fair 스케줄러 전환은 추가 설정 파일과 큐 구성이 필요해 환경별 오류가 생길 수 있으므로, 이 실습에서는 현재 스케줄러 확인과 YARN 작업 실행 흐름을 검증합니다.

## 1. 현재 스케줄러 설정 확인
```bash
docker exec namenode bash -lc "grep -A1 yarn.resourcemanager.scheduler.class /usr/local/hadoop/etc/hadoop/yarn-site.xml"
```

## 2. ResourceManager 재시작
```bash
docker exec namenode bash -lc "yarn --daemon stop resourcemanager; yarn --daemon start resourcemanager; sleep 5"
```

## 3. NodeManager 상태 확인
```bash
docker exec namenode yarn node -list
```

## 4. Pi 프로그램 실행 및 시간 측정
```bash
docker exec namenode bash -lc "time hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.5.jar pi 10 100"
```

## 5. YARN 애플리케이션 목록 확인
```bash
docker exec namenode yarn application -list -appStates ALL
```

## 제출 캡처
아래 핵심 결과 화면 4개를 캡처해 제출합니다.
- image1: 현재 YARN 스케줄러 설정 확인 화면
- image2: ResourceManager 재시작 후 `yarn node -list` 화면
- image3: Pi 프로그램 실행 완료 화면
- image4: YARN 애플리케이션 목록 화면
