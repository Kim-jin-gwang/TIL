import re

text = "2026-02-20 ERROR user_id=12345 latency=203ms"
# text = "2026-02-20 ERROR user_id=12345 latency=203m"

# + : 1회 이상 반복
print(re.findall(r'\d+', text))             # ['2026', '02', '20', '12345', '203']

# * : 0회 이상 반복
print(re.findall(r'-\d*', text))            # ['-02', '-20']

# ? : 0 또는 1회
print(re.findall(r'latency=\d+ms?', text))  # ['latency=203ms'] - s가 있어도 없어도 매칭

# {n} : 정확히 n회
print(re.findall(r'\d{4}', text))           # ['2026']

# {n,m} : n~m회
print(re.findall(r'\d{2,4}', text))         # ['2026', '02', '20', '1234', '203']

# [] : 문자 집합 - 대괄호 안의 문자 중 하나
print(re.findall(r'[A-Z]+', text))          # ['ERROR']
print(re.findall(r'[0-9a-z]+', text))       # ['2026', '02', '20', 'ser', 'id', '12345', 'latency', '203']

# ^ : 문자열 시작
print(re.match(r'^\d{4}', text))            # <re.Match object; span=(0, 4), match='2026'> - 2026으로 시작
print(re.match(r'^\d{4}', text).group())    # 2026

# $ : 문자열 끝
print(re.search(r'ms$', text))              # <re.Match object; span=(42, 44), match='ms'> - ms로 끝
print(re.search(r'ms$', text).group())      # ms
