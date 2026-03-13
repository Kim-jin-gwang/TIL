import re


# 1. 패턴 범위 지정
file_list = [
    "report.pdf",
    "data.csv",
    "config.json",
    "image.png"
]

pattern = re.compile(r'\.(pdf|csv|json)$')

for file in file_list:
    if pattern.search(file):
        print(f'Match: {file}')
        # Match: report.pdf
        # Match: data.csv
        # Match: config.json

print("-" * 30)

# 2. 데이터 추출

# 샘플 로그 (실제로는 수만 줄의 데이터)
log_data = "2026-02-23 14:30:05 [INFO] latency=156ms"

# 2-1. 인덱스 기반 그룹 추출
basic_pattern = re.compile(r"(\d{4}-\d{2}-\d{2}).*latency=(\d+)")
match = basic_pattern.search(log_data)

if match:
    print(f"전체 매치: {match.group(0)}")   # 2026-02-23 14:30:05 [INFO] latency=156
    print(f"추출된 날짜: {match.group(1)}") # 2026-02-23
    print(f"추출된 지연시간: {match.group(2)}") # 156

print("-" * 30)

# 2-2. 이름 붙인 그룹 추출 (Named Group) - 권장 방식
# (?P<이름>...) 형식을 사용
named_pattern = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2}).*latency=(?P<latency>\d+)")
match_named = named_pattern.search(log_data)

if match_named:
    print(f"전체 매치: {match_named.group(0)}") # 2026-02-23 14:30:05 [INFO] latency=156
    print(f"추출된 날짜: {match_named.group('date')}") # 2026-02-23
    print(f"추출된 지연시간: {match_named.group('latency')}") # 156
    
    # 딕셔너리 형태로 한 번에 변환도 가능(Pandas 데이터프레임 생성 시 유용)
    print(f"딕셔너리 변환: {match_named.groupdict()}")  # {'date': '2026-02-23', 'latency': '156'}

print("-" * 30)

# 2-2. 이름 붙인 그룹 추출 (Named Group) - 여러 데이터 매치
log_text = '''
2026-02-20 ERROR user_id=12345 msg="Login failed" latency=203ms
2026-02-21 INFO user_id=67890 latency=87ms
2026-02-22 WARN user_id=11111 msg="Long latency" latency=543ms
2026-02-23 ERROR user_id=22222 msg="Login failed" latency=1203ms
'''
named_pattern = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2}).*latency=(?P<latency>\d+)")
match_list = named_pattern.finditer(log_text)

for match_data in match_list:
    print(match_data.groupdict())

# {'date': '2026-02-20', 'latency': '203'}
# {'date': '2026-02-21', 'latency': '87'}
# {'date': '2026-02-22', 'latency': '543'}
# {'date': '2026-02-23', 'latency': '1203'}

print("-" * 30)

# 3. 그룹 재사용 (Backreference)
html_text = """
<div>
    <p>Hello World</p>
    <span>Regex Study</span>
    <div>Nested Test</div>
</div>
"""

# pattern = re.compile(r"<(\w+)>(.*?)</\1>")  # Positional 예시
pattern = re.compile(r"<(?P<tag>\w+)>(.*?)</(?P=tag)>") # Named 예시

for match in pattern.finditer(html_text):
    print("Matched Text:", match.group(0)) # <p>Hello World</p>
    # print("Tag Name:", match.group(1))  # Positional 일 때
    print("Tag Name:", match.group("tag")) # Named 일 때
# Matched Text: <p>Hello World</p>
# Tag Name: p
# Matched Text: <span>Regex Study</span>
# Tag Name: span
# Matched Text: <div>Nested Test</div>
# Tag Name: div

