# 실습 힌트
# - 목표: 거래 금액 기준으로 스트림을 나누고, 낮은 금액은 10%씩 증가시킨 뒤 다시 합칩니다.
# - process_transactions 안의 TODO은 낮은 금액 스트림의 금액을 10% 증가시키는 map 연산입니다.
# - high_value_stream은 5000 이상, low_value_stream은 5000 미만 조건으로 분리합니다.
# - 실행 위치: skeleton 디렉터리에서 실행해야 ../data/data.csv 경로가 맞습니다.

# TODO 안내
# - 낮은 금액 스트림은 map으로 10% 증가시킵니다.
# - 고액/저액 분리는 filter와 금액 기준 5000으로 작성합니다.
# - 반복 처리 대상은 low_value_stream입니다.
# - 최종 union은 high_value_stream과 processed_stream을 병합합니다.

import pandas as pd
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.typeinfo import Types

def process_transactions(input_stream):
    """
    거래 데이터를 반복 처리하는 함수
    - 최대 10회 반복 후 종료
    - 낮은 거래 금액을 10%씩 증가시키되, 데이터가 중간에 사라지지 않도록 필터링하지 않음
    """
    max_iterations = 10  # 최대 반복 횟수
    iteration = 0

    while iteration < max_iterations:
        input_stream = input_stream.map(
            lambda x: (x[0],x[1] * 1.1),  # TODO: 각 레코드의 금액을 10% 증가시키는 변환 연산
            output_type=Types.TUPLE([Types.STRING(), Types.FLOAT()])
        )
        iteration += 1  

    return input_stream  # 최종 처리된 스트림 반환

def main():
    # Flink 실행 환경 설정
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    # CSV 데이터 불러오기
    df = pd.read_csv("../data/data.csv")
    transactions = df[['stock_ticker', 'amount']].dropna().values.tolist()  

    # TODO: 리스트 데이터를 DataStream으로 변환
    transaction_stream = env.from_collection(
        transactions, 
        type_info=Types.TUPLE([Types.STRING(), Types.FLOAT()])
    )

    # 거래 금액 기준 데이터 분할
    high_value_stream = transaction_stream.filter(lambda x: x[1] >= 5000)  # TODO: 5000 이상인 거래만 선택하는 필터 연산
    low_value_stream = transaction_stream.filter(lambda x: x[1] < 5000 )  # TODO: 5000 미만 거래만 선택하는 필터 조건 작성

    # 반복 연산 적용
    processed_stream = process_transactions(low_value_stream)  # TODO: 10% 증가 반복을 적용할 낮은 금액 스트림

    # 최종 결과 스트림 병합
    final_stream = high_value_stream.union(processed_stream)  # TODO: 원래 높은 금액 스트림과 처리된 낮은 금액 스트림을 병합

    # 결과 출력
    final_stream.print()

    # 실행
    env.execute("Transaction Processing with Split & Iteration")

if __name__ == "__main__":
    main()
