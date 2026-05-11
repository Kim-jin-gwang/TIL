# 실습 힌트
# - 목표: 주식 티커별 총 거래 금액과 거래 횟수를 reduce로 누적하고 평균 금액을 계산합니다.
# - key_by는 stock_ticker 위치인 x[0]을 사용합니다.
# - reduce 결과는 (ticker, total_amount, count) 형태를 유지하고, map에서 평균을 계산하세요.
# - 실행 위치: skeleton 디렉터리에서 실행해야 ../data/data.csv 경로가 맞습니다.

# TODO 안내
# - Flink 실행 환경은 StreamExecutionEnvironment.get_execution_environment()로 만듭니다.
# - 티커별 그룹화는 key_by(lambda x: x[0])를 사용합니다.
# - 거래 금액과 거래 횟수는 reduce로 누적합니다.
# - 평균 계산은 map으로 처리하고 결과는 print로 출력합니다.
# - 마지막에는 env.execute로 잡을 실행합니다.

import pandas as pd
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.typeinfo import Types

def main():
    # Flink 실행 환경 설정
    env = StreamExecutionEnvironment.get_execution_environment()  # Flink TODO: 실행 환경 생성 메서드 호출
    
    # 병렬성 1로 설정
    env.set_parallelism(1)  

    # CSV 파일 로드
    df = pd.read_csv("../data/data.csv")  
    transactions = df[['stock_ticker', 'amount']].dropna().values.tolist()  # 주식 티커(상품)와 거래 금액 선택

    # TODO: 리스트 데이터를 DataStream으로 변환 (상품 ID, 거래 금액, 초기 거래 횟수(1) 추가)
    transaction_stream = env.from_collection(
        [(t[0], t[1], 1) for t in transactions],  # 거래 횟수(1) 추가
        type_info=Types.TUPLE([Types.STRING(), Types.FLOAT(), Types.INT()])
    )

    # Keyby Reduce 연산: 상품별 총 거래 금액 및 거래 횟수 누적
    total_amount_stream = (transaction_stream
                           .key_by(lambda x: x[0])  # TODO: stock_ticker 기준으로 그룹화하는 메서드
                           .reduce(lambda a, b: (a[0], a[1] + b[1], a[2] + b[2])))  # TODO: 같은 stock_ticker의 금액과 건수를 누적하는 연산

    # 평균 거래 금액 계산 (map 연산)
    average_transaction_stream = total_amount_stream.map(
        lambda x: (x[0], x[1], x[1] / x[2] if x[2] > 0 else 0),  # 평균 계산을 위한 map 연산 적용
        output_type=Types.TUPLE([Types.STRING(), Types.FLOAT(), Types.FLOAT()])
    )

    # 결과 출력 (상품별 총 거래 금액 및 평균 거래 금액)
    average_transaction_stream.print()  # TODO: 결과 스트림 출력 메서드 호출

    # TODO: Flink 잡 실행 메서드 호출
    env.execute("Stock Ticker Total and Average Transaction Amount")  # TODO: Flink 잡 실행 메서드 호출

if __name__ == "__main__":
    main()
