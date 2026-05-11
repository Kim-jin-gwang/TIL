import pandas as pd
from pyflink.datastream import StreamExecutionEnvironment  # Flink 스트리밍 실행 환경을 가져오는 모듈
from pyflink.common.typeinfo import Types  # 데이터 타입을 정의하는 모듈

'''
Exception in thread read_grpc_client_inputs 오류는 Apache Beam Runner가 내부적으로 사용하면서 생기는 gRPC 관련 예외
Exception in thread read_grpc_client_inputs는 Apache Beam + gRPC 스레드 관련 경고로 Flink 파이프라인이 정상 종료되었는지만 확인하면 됩니다.
PyFlink는 내부적으로 Apache Beam Runner 또는 MiniCluster를 사용하는데, 그 과정에서 gRPC 기반의 내부 스레드 처리 중 오류가 발생하는 경우가 있습니다. 

Flink 작업이 정상적으로 완료되었더라도, PyFlink 실행 시 내부적으로 read_grpc_client_inputs나 Multiplexer hanging up 같은 gRPC 관련 오류 메시지가 출력될 수 있습니다.
이건 Flink와 Python 사이의 통신이 작업 종료와 함께 빠르게 끊기면서 생기는 정상적인 현상이며, 결과나 실행에는 전혀 영향을 주지 않습니다.
실제로 결과가 잘 출력되었다면 안심하셔도 됩니다.
'''

def main():
    # Flink 스트리밍 실행 환경 설정
    env = StreamExecutionEnvironment.get_execution_environment()  # Flink 실행 환경 생성

    # 병렬성 2로 설정
    env.set_parallelism(2)

    # CSV 데이터 불러오기
    df = pd.read_csv("../data/data.csv")
    #df = pd.read_csv("/opt/flink/workspace/data_engineering1_ws_7_3/data/data.csv")  # docker 환경에서의 경로로 변경
    news_texts = df["news_text"].dropna().tolist()  # 리스트 변환을 위한 메서드 호출

    # 스트리밍 데이터 스트림 생성
    text_stream = env.from_collection(news_texts, type_info=Types.STRING())  # 데이터 스트림을 생성하는 메서드

    # WordCount 파이프라인 구성
    word_count = (text_stream
                  .flat_map(lambda text: [(word.lower(), 1) for word in text.split()], 
                            output_type=Types.TUPLE([Types.STRING(), Types.INT()]))
                  .key_by(lambda x: x[0])
                  .sum(1))  # 실시간 합산을 위한 덧셈 함수

    # 결과 실시간 출력
    word_count.print()  # 스트림을 출력하는 메서드 호출

    # 실행
    env.execute("Streaming Finance News WordCount")  # Flink 실행을 시작하는 메서드 호출

if __name__ == "__main__":
    main()
