import re

text = "user_id=12345 latency=203ms"


# Lookahead (?=패턴) : 뒤에 패턴이 오는 경우에 앞의 내용이 매칭됨, 작성된 패턴은 결과에 포함 안 됨
# \w+ 뒤에 = 이 오는 단어만 추출 → = 는 결과에 미포함
print(re.findall(r'\w+(?==)', text))         # ['user_id', 'latency']


# Negative Lookahead (?!...) : 패턴 뒤에 ...이 오지 않는 경우만 매칭
# \d+ 뒤에 ms 가 오지 않는 숫자만 추출
# 주의: 203ms 에서 3ms 를 제외한 20 이 반환됨 (203 전체 추출 불가)
print(re.findall(r'\d+(?!ms)', text))        # ['12345', '20']

# ms 바로 앞의 숫자를 추출하려면 Lookahead 사용
print(re.findall(r'\d+(?=ms)', text))        # ['203']


# Lookbehind (?<=...) : 패턴 앞에 ...이 있는 경우만 매칭, ...은 결과에 포함 안 됨
# = 뒤에 오는 값만 추출 → = 는 결과에 미포함
print(re.findall(r'(?<==)\w+', text))        # ['12345', '203ms']


# Negative Lookbehind (?<!...) : 패턴 앞에 ...이 없는 경우만 매칭
# user_id= 뒤가 아닌 숫자만 추출 → latency 의 203 만 반환
print(re.findall(r'(?<!user_id=)\d+', text)) # ['203']


# 소비 비교 : Lookahead 는 조건만 검사하고 결과에 포함하지 않음
text2 = "100ms 200ms"

print(re.findall(r'\d+ms', text2))      # ['100ms', '200ms'] - ms 포함 (소비)
print(re.findall(r'\d+(?=ms)', text2))  # ['100', '200']     - ms 제외 (소비 안 함)


# 탐욕적 매칭과 게으른 매칭
html = "<div>hello</div>"
print(re.findall(r"<.*>", html))  # ['<div>hello</div>'] - Greedy
print(re.findall(r"<.*?>", html)) # ['<div>', '</div>'] - Lazy

text3 = "aaaa"
print(re.findall(r"a+", text3))    # ['aaaa'] - Greedy
print(re.findall(r"a+?", text3))   # ['a', 'a', 'a', 'a'] - Lazy


# 비캡쳐 그룹 예제 1
text = "office: 02-123-4567"

# 일반 그룹 () 사용 : 괄호 안의 내용(02)만 쏙 뽑아서 리스트에 담음
pattern1 = re.findall(r"(\d{2,3})-\d{3}-\d{4}", text)
print(f"일반 그룹: {pattern1}") # ['02'] 

# 비캡처 그룹 (?:) 사용 : 괄호는 '묶기'용으로만 쓰고, 리스트에는 전체를 담음
pattern2 = re.findall(r"(?:\d{2,3})-\d{3}-\d{4}", text)
print(f"비캡처 그룹: {pattern2}")  # ['02-123-4567']


# 비캡처 그룹 예제 2
text = """
file.pdf
data.csv
image.png
report.json
"""

# re.MULTILINE : 문자열 전체가 아니라, 줄 단위로 시작(^)과 끝($)을 판단하도록 만드는 옵션
# 일반 그룹
pattern1 = re.compile(r'.+\.(pdf|csv|json)$', re.MULTILINE)

# 비캡처 그룹
pattern2 = re.compile(r'.+\.(?:pdf|csv|json)$', re.MULTILINE)

print("=== 일반 그룹 ===")
print(re.findall(pattern1, text))   # ['json']

print("=== 비캡처 그룹 ===")
print(re.findall(pattern2, text))   # ['.json']