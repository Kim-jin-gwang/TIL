import time
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.window import SlidingProcessingTimeWindows
from pyflink.common.time import Time
from pyflink.common.typeinfo import Types


def delayed_map(record):
    """Processing time window의 겹치는 집계를 눈으로 보기 위한 입력 간격"""
    if record[1] == 0:
        time.sleep(3)
    elif record[1] == 1:
        time.sleep(0.1)
    elif record[1] == 3:
        time.sleep(0.4)
    elif record[1] == 4:
        time.sleep(1.1)
    elif record[1] == 5:
        time.sleep(0.4)
    return record


env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

data = [
    ("user1", 1),
    ("user1", 3),
    ("user1", 4),
    ("user1", 5),
    ("user1", 0),  # 마지막 윈도우가 닫힐 시간을 벌기 위한 요소
]
data_stream = env.from_collection(
    collection=data,
    type_info=Types.TUPLE([Types.STRING(), Types.INT()])
)

delayed_stream = data_stream.map(
    delayed_map,
    output_type=Types.TUPLE([Types.STRING(), Types.INT()])
)

# 2초 크기의 윈도우가 1초마다 생성되므로 같은 이벤트가 둘 이상의 윈도우에 포함될 수 있다.
windowed_stream = (
    delayed_stream
        .key_by(lambda x: x[0])
        .window(SlidingProcessingTimeWindows.of(Time.seconds(2), Time.seconds(1)))
        .reduce(lambda a, b: (a[0], a[1] + b[1]))
)

windowed_stream.print()
env.execute("Sliding Processing Time Window Example")
