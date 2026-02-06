import requests

URL = 'https://jsonplaceholder.typicode.com/todos'

response = requests.get(URL).json()
completed_items = []
fields = ['id','title']

for item in response:
    if item['completed']:
        temp_item = {}
        for key in fields:
            temp_item[key] = item[key]
        completed_items.append(temp_item)

print(completed_items)