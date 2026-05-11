# 실습 힌트
# - 목표: 거래 유형별 금액 합계를 PyFlink DataStream으로 계산합니다.
# - 실행 환경은 StreamExecutionEnvironment.get_execution_environment()로 생성합니다.
# - 데이터 타입은 Types.TUPLE([Types.STRING(), Types.FLOAT()]) 형태로 지정하세요.
# - key_by는 transaction_type 위치인 x[0], sum은 amount 위치인 1번 인덱스를 사용합니다.

# TODO 안내
# - Flink 실행 환경은 StreamExecutionEnvironment의 실행 환경 생성 메서드로 만듭니다.
# - 리스트는 env.from_collection으로 DataStream으로 변환하고 tuple 타입을 지정합니다.
# - 거래 유형 기준 그룹화는 key_by(lambda x: x[0])를 사용합니다.
# - 금액 합계는 amount 위치인 인덱스 1을 sum에 전달합니다.
# - 마지막에는 env.execute로 잡을 실행합니다.

import pandas as pd
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.typeinfo import Types

def main():
    # Flink 스트리밍 실행 환경 설정
    env = StreamExecutionEnvironment.get_execution_environment()  # TODO: Flink 실행 환경을 생성하는 메서드 호출

    # CSV 데이터 불러오기
    df = pd.read_csv("../data/data.csv")
    transactions = df[["transaction_type", "amount"]].dropna().values.tolist()  

    # 스트리밍 TODO: 리스트 데이터를 DataStream으로 변환
    transaction_stream = env.from_collection(transactions, type_info=Types.TUPLE([Types.STRING(), Types.FLOAT()]))  # TODO: 리스트를 DataStream으로 변환하고 (문자열, 실수) 튜플 타입 지정

    # 거래 유형별 금액 합산 파이프라인 구성
    total_amount_per_type = transaction_stream.key_by(lambda x:x[0]).sum(1)

    # 결과 실시간 출력
    total_amount_per_type.print()

    # 실행
    env.execute("Streaming Transaction Processing")  # TODO: Flink 잡 실행 메서드 호출을 시작하는 메서드 호출

if __name__ == "__main__":
    main()
