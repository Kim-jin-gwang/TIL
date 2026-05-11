# 실습 힌트
# - 목표: 뉴스 문장을 단어로 분해하고 금융 키워드만 필터링한 뒤 단어별 빈도를 집계합니다.
# - 실행 환경 생성 후 병렬성은 set_parallelism(2)로 지정합니다.
# - flat_map은 문장을 [(word, 1), ...] 형태로 펼치고, filter는 finance_keywords 포함 여부를 확인합니다.
# - 실행 위치: skeleton 디렉터리에서 실행해야 ../data/data.csv 경로가 맞습니다.

# TODO 안내
# - Flink 실행 환경을 만들고 병렬성은 2로 설정합니다.
# - 뉴스 텍스트 리스트는 from_collection으로 문자열 DataStream으로 변환합니다.
# - 문장을 단어 튜플로 펼칠 때 flat_map을 사용하고 금융 키워드만 filter로 남깁니다.
# - 키워드별 집계는 key_by(lambda x: x[0]).sum(1)로 수행합니다.
# - 마지막에는 env.execute로 잡을 실행합니다.

import pandas as pd
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.typeinfo import Types

def main():
    # Flink 실행 환경 설정
    env = StreamExecutionEnvironment.get_execution_environment()  # TODO: 실행 환경 생성 메서드 호출
    # 병렬성 2로 설정
    env.set_parallelism(2)  

    # CSV 데이터 불러오기
    df = pd.read_csv("../data/data.csv")
    news_texts = df["news_text"].dropna().tolist()  # 결측값 제거 후 리스트 변환

    # TODO: 리스트 데이터를 DataStream으로 변환
    text_stream = env.from_collection(news_texts, type_info=Types.STRING())  # TODO: 리스트 데이터를 DataStream으로 변환

    # FlatMap 및 Filter 연산 적용
    finance_keywords = {"stock", "market", "investment", "economy"}
    processed_stream = (text_stream
                        .flat_map(lambda text: [(word.lower(), 1) for word in text.split()], 
                              output_type=Types.TUPLE([Types.STRING(), Types.INT()]))  # FlatMap 연산 적용
                        .filter(lambda x: x[0] in finance_keywords))  # 특정 금융 키워드만 필터링하는 함수

    # 키워드 별로 갯수 집계
    aggregated_stream = processed_stream.key_by(lambda x: x[0]).sum(1)
    # 결과 출력
    aggregated_stream.print()

    # 실행
    env.execute("FlatMap and Filter Example")  # TODO: Flink 잡 실행 메서드 호출

if __name__ == "__main__":
    main()
