from pathlib import Path

import pandas as pd
from pyflink.common.typeinfo import Types
from pyflink.datastream import KeyedProcessFunction, StreamExecutionEnvironment
from pyflink.datastream.state import ValueStateDescriptor


DATA_PATH = Path(__file__).with_name("data.csv")


class KeyedCustomerSpend(KeyedProcessFunction):
    """customer_id별 누적 거래 금액을 ValueState에 저장하는 예제."""

    def open(self, runtime_context):
        descriptor = ValueStateDescriptor("customer_spend_sum", Types.FLOAT())
        self.state = runtime_context.get_state(descriptor)

    def process_element(self, value, ctx):
        customer_id, amount = value
        current_sum = self.state.value() or 0.0
        new_sum = current_sum + amount
        self.state.update(new_sum)
        yield (customer_id, round(new_sum, 2))


def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    env.enable_checkpointing(10000)

    df = pd.read_csv(DATA_PATH)
    transactions = df[["customer_id", "amount"]].dropna().head(20).values.tolist()

    customer_stream = env.from_collection(
        transactions,
        type_info=Types.TUPLE([Types.STRING(), Types.FLOAT()])
    )

    result_stream = (
        customer_stream
        .key_by(lambda x: x[0])
        .process(
            KeyedCustomerSpend(),
            output_type=Types.TUPLE([Types.STRING(), Types.FLOAT()])
        )
    )

    result_stream.print("customer-spend")
    env.execute("Keyed State Customer Spend Example")


if __name__ == "__main__":
    main()
