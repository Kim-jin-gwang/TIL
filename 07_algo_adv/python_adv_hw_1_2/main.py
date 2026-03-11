def read_data(data_list):
    for line in data_list:
        yield line.strip()

def filter_errors(iterator):
    for line in iterator:
        if "ERROR" in line:
            yield line


def to_uppercase(iterator):
    for line in iterator:
        yield line.upper()

# 사용 예시:
raw_data = [
    "INFO: This is an info message.",
    "ERROR: This is an error message.",
    "WARNING: This is a warning message.",
    "ERROR: Another error message."
]

pipeline = to_uppercase(filter_errors(read_data(raw_data)))
for line in pipeline:
    print(line) 