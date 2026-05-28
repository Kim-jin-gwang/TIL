from pyflink.common import Duration
from pyflink.common.typeinfo import Types
from pyflink.common.watermark_strategy import TimestampAssigner, WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import ProcessFunction


class EventTimeAssigner(TimestampAssigner):
    def extract_timestamp(self, element, record_timestamp):
        return element[2]


class ExplainWatermarkProcessFunction(ProcessFunction):
    def open(self, runtime_context):
        self.max_event_time = -1

        self.window_counts = {}

    def process_element(self, value, ctx):
        label, sensor_id, event_time, count = value

        self.max_event_time = max(self.max_event_time, event_time)
        watermark = self.max_event_time - 1000

        # 2초 이벤트 시간 윈도우입니다.
        # 0~1999ms는 [0s,2s), 4000~5999ms는 [4s,6s)에 들어갑니다.
        window_start = (event_time // 2000) * 2000
        window_end = window_start + 2000

        # allowed lateness 2초를 적용한 정리 기준입니다.
        # [0s,2s) window는 watermark가 4s를 지나면 더 이상 늦은 데이터를 받지 않습니다.
        cleanup_time = window_end + 2000

        if watermark > cleanup_time:
            yield (
                f"TOO LATE     event={label:24s} "
                f"event_time={event_time // 1000}s watermark={watermark // 1000}s "
                f"window=[{window_start // 1000}s,{window_end // 1000}s)"
            )
            return

        self.window_counts[window_end] = self.window_counts.get(window_end, 0) + count

        if watermark >= window_end and event_time < watermark:
            status = "LATE ALLOWED"
        elif watermark >= window_end:
            status = "WINDOW READY"
        else:
            status = "COLLECTED"

        yield (
            f"{status:12s} event={label:24s} "
            f"event_time={event_time // 1000}s watermark={watermark // 1000}s "
            f"window=[{window_start // 1000}s,{window_end // 1000}s) "
            f"count={self.window_counts[window_end]}"
        )


# 실행 환경 생성
env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

data = [
    # [0s,2s) window에 정상적으로 들어가는 이벤트입니다.
    ("on-time-0s", "sensor-1", 0, 1),
    ("on-time-1s", "sensor-1", 1000, 1),

    # event_time=4s가 도착하면 watermark는 3s가 됩니다.
    # 이때 [0s,2s) window는 결과를 낼 수 있는 상태가 됩니다.
    ("advance-watermark-4s", "sensor-1", 4000, 1),

    # event_time=1s이므로 [0s,2s) window에 속합니다.
    # watermark=3s라 늦었지만, cleanup 기준 4s 전이므로 allowed lateness 안쪽입니다.
    ("late-but-allowed-1s", "sensor-1", 1000, 1),

    # event_time=10s가 도착하면 watermark는 9s가 됩니다.
    # 이제 [0s,2s) window의 cleanup 기준 4s를 훨씬 지났습니다.
    ("advance-watermark-10s", "sensor-1", 10000, 1),

    # 같은 event_time=1s이지만 이제는 너무 늦었습니다.
    # 실제 Window API에서는 side_output_late_data(...) 대상입니다.
    ("too-late-1s", "sensor-1", 1000, 1),
]


# 데이터 소스 정의
source = env.from_collection(
    data,
    type_info=Types.TUPLE([Types.STRING(), Types.STRING(), Types.LONG(), Types.INT()])
)


# 워터마크 전략 설정: 최대 1초까지 순서가 뒤바뀐 이벤트를 기다립니다.
# 예를 들어 event_time=4s를 보면 watermark는 대략 3s까지 진행됩니다.
watermark_strategy = (
    WatermarkStrategy
        .for_bounded_out_of_orderness(Duration.of_seconds(1))
        .with_timestamp_assigner(EventTimeAssigner())
)


# 타임스탬프와 워터마크를 스트림에 적용합니다.
watermarked_stream = source.assign_timestamps_and_watermarks(watermark_strategy)


# watermark가 적용된 스트림을 설명용 ProcessFunction에 통과시켜 결과를 출력합니다.
processed_stream = watermarked_stream.process(
    ExplainWatermarkProcessFunction(),
    output_type=Types.STRING()
)
processed_stream.print()


# 실행
env.execute("Watermark Late Elements Concept")
