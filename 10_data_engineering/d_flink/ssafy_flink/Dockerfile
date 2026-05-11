FROM flink:1.19-scala_2.12-java17

# Python3, pip, PyFlink 및 실습에 필요한 Python 라이브러리 설치
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip install --no-cache-dir apache-flink==1.19.3 && \
    pip install --no-cache-dir pandas

# Kafka 연동을 위한 Flink SQL Kafka Connector JAR 파일 복사
# Dockerfile과 같은 위치에 flink-sql-connector-kafka-3.3.0-1.19.jar 파일이 있어야 함
COPY flink-sql-connector-kafka-3.3.0-1.19.jar /opt/flink/

# PyFlink 실행에 필요한 flink-python JAR 파일을 Flink 경로로 복사
RUN cp /opt/flink/opt/flink-python-*.jar /opt/flink/

# python 명령어로 Python3가 실행되도록 심볼릭 링크 생성
RUN ln -s /usr/bin/python3 /usr/bin/python

# Flink 기본 작업 디렉토리 설정
WORKDIR /opt/flink