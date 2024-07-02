"""
fm ディレクトリからすべての csv を読み込み、ハッシュ値毎の枚数を集計する
それぞれのフォームに存在する同じハッシュ値の合計と、結果をjsonとcsvで出力する

DATA_DIR = './fm/'
=====
./fm/表【FM】ホルダー用.csv
./fm/表【FM】特別枠.csv


input
=====
枚数,名前,ウォレットアドレス
4,aaa,0x355cD95466fXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
4,bbb,0x9d17e09C8d1xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

...

output:
1. json
=====
{
    '0x355cD95466fXXXXXXXXXXXXXXXXXXXXXXXXXXXXX': {
        'maxClaimable': 5,
        'details': {
            '表【FM】ホルダー用.csv': 3,
            '表【FM】特別枠.csv': 2
        },
    },
    '0x9d17e09C8d1xxxxxxxxxxxxxxxxxxxxxxxxxxxxx': {
        'maxClaimable': 3,
        'details': {
            '表【FM】ホルダー用.csv': 2,
            '表【FM】特別枠.csv': 1,
        },
    },
    ...
}

2. csv
=====
address,maxClaimable
0x355cD95466fXXXXXXXXXXXXXXXXXXXXXXXXXXXXX,5
0x9d17e09C8d1xxxxxxxxxxxxxxxxxxxxxxxxxxxxx,3
...
"""
import csv
import json
import os


DATA_DIR = './fm/'

# Initialize a dictionary to store the results
result = {}

# Process each CSV file
for filename in os.listdir(DATA_DIR):
    if filename.endswith('.csv'):
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for _ in range(1):  # Skip the first two rows
                try:
                    next(reader)
                except StopIteration:
                    break
            for row in reader:
                address = row[2]
                if address not in result:
                    result[address] = {'maxClaimable': 0, 'details': {}}
                if filename not in result[address]['details']:
                    result[address]['details'][filename] = 0
                result[address]['details'][filename] = row[0]
                result[address]['maxClaimable'] += int(row[0])

# Write the result to a JSON file
with open('./fm/fm_result/fm_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# Create csv for check total count by weight
with open('./fm/fm_result/fm_result.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['address', 'maxClaimable'])
    for address, data in result.items():
        writer.writerow([address, data['maxClaimable']])
