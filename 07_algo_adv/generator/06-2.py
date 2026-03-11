def read_large_file_with_generator(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()
# 예제 파일 경로
file_path = 'large_data_file.txt'

# 제너레이터 사용하여 파일 읽기 및 처리
for line in read_large_file_with_generator(file_path):
    # print(line)
    pass
