import re

text = "2026-02-20 ERROR user_id=12345 latency=203ms  "

# . : 임의의 문자 1개
print(re.findall(r'20..', text))        # ['2026'] - 2000년대 매칭

# + 는 앞의 문자가 1개 이상을 의미
# \d : 숫자 [0-9], \d+ : 숫자가 1개 이상
print(re.findall(r'\d+', text))         # ['2026', '02', '20', '12345', '203']

# \w : 문자+숫자+_ [A-Za-z0-9_], \w+ : 문자, 숫자, '_'가 1개 이상 
print(re.findall(r'\w+', text))         # ['2026', '02', '20', 'ERROR', 'user_id', '12345', 'latency', '203ms']

# \s : 공백, 탭, 줄바꿈, \s+ : 공백, 줄바꿈이 1개 이상
print(re.findall(r'\s+', text))         # [' ', ' ', ' ', '  '] 마지막 공백 포함하여 출력

# \D : 숫자가 아닌 것 (\d 의 반대)
print(re.findall(r'\D+', text))         # ['-', '-', ' ERROR user_id=', ' latency=', 'ms  ']

# \W : 영문, 숫자, '_' 아닌 것 (\w 의 반대)
print(re.findall(r'\W+', text))         # ['-', '-', ' ', ' ', '=', ' ', '=', '  ']

# \S : 공백이 아닌 것 (\s 의 반대)
print(re.findall(r'\S+', text))         # ['2026-02-20', 'ERROR', 'user_id=12345', 'latency=203ms']


# \b : 단어 경계 위치
print(re.findall(r'\b\d+', text))       # ['2026', '02', '20', '12345', '203'] 숫자가 단어의 시작에 있는 것
print(re.findall(r'\d+\b', text))       # ['2026', '02', '20', '12345', '203'] 숫자가 단어의 끝에 있는 것


# \b : 단어 경계 위치 2
example_text = 'ERROR myERROR ERRORS'

print(re.findall(r'ERROR', example_text))
# 결과: ['ERROR', 'ERROR', 'ERROR'] ERROR, myERROR, ERRORS 에 있는 것
print(re.findall(r'ERROR\b', example_text))      
# 결과: ['ERROR', 'ERROR'] ERROR, myERROR와 같이 ERROR로 끝나는 것
print(re.findall(r'\bERROR\b', example_text))    
# 결과: ['ERROR'] ERROR 가 단독으로 사용되는 것

# 음수가 아닌 양수만 선택
example_price = '-100 200 -300 400'
print(re.findall(r'(?<!-)\d+', example_price))  # ['00', '200', '00', '400']
print(re.findall(r'(?<!-)\b\d+', example_price))# ['200', '400']

