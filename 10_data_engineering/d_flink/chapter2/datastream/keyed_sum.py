from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import KeyedProcessFunction
from pyflink.datastream.state import ValueStateDescriptor
from pyflink.common.typeinfo import Types


# 상태 기반 연산 정의
class KeyedSum(KeyedProcessFunction):

    def __init__(self):
        self.state = None

    def open(self, runtime_context):
        """
        각 key별로 유지할 상태를 정의합니다.

        ValueStateDescriptor(
            "sum",           # 상태 이름
            Types.FLOAT()    # 상태에 저장할 데이터 타입
        )
        """
        descriptor = ValueStateDescriptor("sum", Types.FLOAT())
        self.state = runtime_context.get_state(descriptor)

    def process_element(self, value, ctx):
        """
        value 예시:
        ("A", 100.0)
        ("A", 50.0)
        ("B", 200.0)

        value[0] -> key
        value[1] -> 금액
        """

        # 현재 key의 기존 누적값 조회
        current_sum = self.state.value()

        # 상태가 아직 없으면 0.0으로 초기화
        if current_sum is None:
            current_sum = 0.0

        # 현재 입력값을 더해 새로운 누적합 계산
        new_sum = current_sum + value[1]

        # 상태 업데이트
        self.state.update(new_sum)

        # 확인용 출력
        print(f"[{value[0]}] 누적 금액: {new_sum}")

        # 다음 연산자로 결과 전달
        yield value[0], new_sum


def main():
    # 실행 환경 생성
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    # 예제 데이터 생성
    data = [
        ("A", 100.0),
        ("B", 200.0),
        ("A", 50.0),
        ("B", 30.0),
        ("A", 20.0),
    ]

    # DataStream 생성
    data_stream = env.from_collection(
        collection=data,
        type_info=Types.TUPLE([Types.STRING(), Types.FLOAT()])
    )

    # key 기준으로 분리한 뒤, key별 상태 기반 누적합 계산
    result_stream = data_stream \
        .key_by(lambda x: x[0], key_type=Types.STRING()) \
        .process(
            KeyedSum(),
            output_type=Types.TUPLE([Types.STRING(), Types.FLOAT()])
        )

    # 결과 출력
    result_stream.print()

    # Flink Job 실행
    env.execute("Keyed State Sum Example")


if __name__ == "__main__":
    main()
