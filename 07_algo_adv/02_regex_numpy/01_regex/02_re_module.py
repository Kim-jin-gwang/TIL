import re

text = "2026-02-20 ERROR user_id=12345 latency=203ms"

# 2-1. match / search
# match() : 문자열 시작부터 매칭, Match 객체 반환 (없으면 None)
print(re.match(r'\d{4}-\d{2}-\d{2}', text))         # <re.Match object; span=(0, 10), match='2026-02-20'>
print(re.match(r'ERROR', text))                     # None (시작이 ERROR가 아님)


# search() : 문자열 전체에서 매칭되는 첫 번째, Match 객체 반환 (없으면 None)
print(re.search(r'\d{4}-\d{2}-\d{2}', text))        # <re.Match object; span=(0, 10), match='2026-02-20'>
print(re.search(r'ERROR', text))                    # <re.Match object; span=(11, 16), match='ERROR'>


# 2-2. findall / finditer
# findall() : 모든 매칭 결과를 리스트로 반환
print(re.findall(r'\d+', text))                      # ['2026', '02', '20', '12345', '203']


# finditer() : 모든 매칭 결과를 Match 객체 이터레이터로 반환
for m in re.finditer(r'\d+', text):
    print(m.group(), m.span())
# 2026 (0, 4)
# 02   (5, 7)
# 20   (8, 10)
# 12345 (22, 27)
# 203  (36, 39)


# 2-3. group / start / end / span
# .group() : 매칭된 문자열 반환
result = re.search(r'user_id=(\w+)', text)
print(result.group())                                # 'user_id=12345' (전체)
print(result.group(1))                               # '12345' (첫 번째 그룹 - 소괄호로 묶인 (\w+)를 의미)

# extra. 소괄호 사용법
# extra_text = "2026-02-20 ERROR user_id=12345 latency=203ms"
# extra_result = re.search(r'(\w+)=(\d+)', extra_text)
# print(extra_result.group(0))                         # 'user_id=12345' (전체)
# print(extra_result.group(1))                         # 'user_id' (첫 번째 그룹)
# print(extra_result.group(2))                         # '12345' (두 번째 그룹)


# .start() / .end() : 매칭된 위치의 시작/끝 인덱스
result = re.search(r'ERROR', text)
print(result.start())                                # 11
print(result.end())                                  # 16


# .span() : (시작 인덱스, 끝 인덱스) 튜플 반환
print(result.span())                                 # (11, 16)


# 2-4. compile
# compile() : 패턴을 미리 컴파일하여 재사용
date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

logs = ["2026-02-20 INFO start", "no date here", "2026-02-21 ERROR timeout"]
for log in logs:
    m = date_pattern.search(log)
    if m:
        print(m.group())
        # '2026-02-20'
        # '2026-02-21'