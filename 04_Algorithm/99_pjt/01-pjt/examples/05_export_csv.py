import requests
import csv


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

with open('completed_todos.csv','w',newline='',encoding='utf-8') as file:
    csv_writer = csv.DictWriter(file,fieldnames=fields)
    csv_writer.writeheader()
    csv_writer.writerows(completed_items)