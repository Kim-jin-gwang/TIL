# 실습 힌트
# - 목표: 문자열 스트림을 만들고 FileSink로 파일에 저장합니다.
# - 실행 환경 생성, from_collection, Encoder.simple_string_encoder, FileSink.build, sink_to, execute 순서로 채우세요.
# - 출력 경로는 ./output/result이며, 기존 결과가 남아 있으면 새 파일이 추가될 수 있습니다.
# - 실행 위치는 이 파일이 있는 skeleton 디렉터리를 권장합니다.

# TODO 안내
# - Flink 실행 환경을 생성합니다.
# - Python 리스트를 DataStream으로 변환합니다.
# - Encoder.simple_string_encoder()를 사용해 문자열 인코더를 생성합니다.
# - FileSink는 for_row_format(...).build()로 완성합니다.
# - DataStream은 sink_to로 FileSink에 연결하고 env.execute로 실행합니다.

import os

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FileSink
from pyflink.common.serialization import Encoder
from pyflink.common.typeinfo import Types


def main():
    # 실행 환경 생성
    env = StreamExecutionEnvironment.get_execution_environment()  
    # TODO: Flink 실행 환경을 생성하는 메서드를 호출하세요.

    # 데이터 소스 생성
    data = ["Hello", "Flink", "World"]

    data_stream = env.from_collection(
        data,
        type_info=Types.STRING()
    )
    # TODO: Python 리스트를 DataStream으로 변환하는 메서드를 호출하세요.

    # PyFlink 문자열 인코더 생성
    encoder = Encoder.simple_string_encoder()
    # TODO: 문자열 데이터를 파일에 저장하기 위한 simple string encoder를 생성하세요.

    # 출력 디렉터리 설정
    output_dir = "./output/result"
    os.makedirs(output_dir, exist_ok=True)

    # FileSink 설정
    file_sink = FileSink.for_row_format(
        output_dir,
        encoder
    ).build()
    # TODO: FileSink를 완성하는 build 메서드를 호출하세요.

    # Sink에 데이터 연결
    data_stream.sink_to(file_sink)
    # TODO: DataStream을 FileSink에 연결하세요.

    # Flink 작업 실행
    env.execute("File Sink Example")
    # TODO: Flink 작업을 실행하세요.


if __name__ == "__main__":
    main()