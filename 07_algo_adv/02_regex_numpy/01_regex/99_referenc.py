import re
# 참고

# \b : 단어 경계 위치
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



# Lookahead를 활용한 And 표현 (문장에 특정 단어가 모두 존재하는지 체크)
sample_text = 'Officer:\nWe support pdf, csv, json formats only.\n Customer:\nI have csv, pdf and json files.'
# pdf와 csv와 json이 모두 존재하는 문장
text_pattern = re.compile(r'(?=.*pdf)(?=.*csv)(?=.*json).*')    
print(text_pattern.findall(sample_text))
# ['We support pdf, csv, json formats only.', 'I have csv, pdf and json files.']


# 후방 탐색 가변 길이 제한
number_pattern = r'(?<=\d+)\w' 
print(re.findall(number_pattern, '12000원 20개 10m'))
# re.error: look-behind requires fixed-width pattern

text = "abc1 abbc2"
pattern = r'(?<=ab*c)\d'
print(re.findall(pattern, text))
# re.error: look-behind requires fixed-width pattern