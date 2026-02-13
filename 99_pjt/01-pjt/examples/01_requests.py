import requests

URL = 'https://jsonplaceholder.typicode.com/todos'
# 어떤 GET 요청을 보내 보겠다.
response = requests.get(URL).json()
# print(response)
# id와 title 필드만 남긴 새로운 리스트 만들기
completed_items = []
fields = ['id', 'title']
for item in response:
    if item['completed']:
        temp_item = {}
        for key in fields:
            temp_item[key] = item[key]
        completed_items.append(temp_item)
print(completed_items)