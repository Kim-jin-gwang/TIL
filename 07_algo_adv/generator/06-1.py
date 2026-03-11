def read_large_file_without_generator(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]
    
file_path = 'large_data_file.txt'
# 전체 파일을 메모리에 로드하여 처리
lines = read_large_file_without_generator(file_path)
for line in lines:
    # print(line)
    pass
