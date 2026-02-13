import csv

with open('data.csv', 'w', encoding='utf-8', newline='') as file:
    filed_names = ['이름', '나이', '직업']
    csv_writer = csv.DictWriter(file, fieldnames=filed_names)
    
    csv_writer.writeheader( )
    csv_writer.writerow({'이름': '홍길동', '나이': 30, '직업': '개발자'})
    # csv_writer = csv.writer(file)
    # csv_writer.writerow(['이름', '나이', '직업'])
    # csv_writer.writerow(['홍길동', 30, '개발자'])
