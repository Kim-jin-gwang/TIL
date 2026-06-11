#!/bin/bash
set -e

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

service ssh start

echo "[$HOSTNAME] Starting Hadoop Services..."

if [[ "$HOSTNAME" == "namenode" ]]; then
    NAME_DIR="/usr/local/hadoop/hdfs/namenode"

    if [[ ! -d "$NAME_DIR/current" ]]; then
        echo "[Namenode] HDFS metadata not found. Formatting once..."
        hdfs namenode -format -force
    else
        echo "[Namenode] Existing HDFS metadata found. Skipping format."
    fi

    echo "[Namenode] Starting NameNode..."
    hdfs namenode &

    echo "[Namenode] Starting ResourceManager..."
    yarn resourcemanager &

    tail -f /dev/null
else
    echo "[$HOSTNAME] Starting DataNode..."
    hdfs datanode &

    echo "[$HOSTNAME] Starting NodeManager..."
    yarn nodemanager &

    tail -f /dev/null
fi
