"""
al ディレクトリからすべての csv を読み込み、同じハッシュ値の数をカウントする
csv ごとにハッシュ値の数の重み付けをできるようにする
それぞれのフォームに存在する同じハッシュ値の合計と、結果をjsonとcsvで出力する

DATA_DIR = './al/'
=====
./al/1.csv
./al/2.csv
./al/3.csv
...

input
=====
[
    '2024/05/21 20:35:09',
    '@xxxxx1001',
    'xxxxx1001',
    '0xC4a096dFFeA26Dxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'コーヒー大好き人間！'
]

weight = {
    '1.csv': 1,
    '2.csv': 2,
    '3.csv': 3,
}

output:
1. json
=====
{
    '0xC4a096dFFeA26Dxxxxxxxxxxxxxxxxxxxxxxxxxx': {
        'maxClaimable': 10,  # 3*weight['1.csv'] + 2*weight['2.csv'] + 1*weight['3.csv']
        'details': {
            '1.csv': 3,
            '2.csv': 2,
            '3.csv': 1,
        },
    },
    '0x9fa328127FA322XXXXXXXXXXXXXXXXXXXXXXXXXX': {
        'maxClaimable': 3,  # 2*weight['1.csv'] + 1*weight['2.csv']
        'details': {
            '1.csv': 2,
            '2.csv': 1,
        },
    },
    ...
}

2. csv
=====
address,maxClaimable
0x9fa328127FA322XXXXXXXXXXXXXXXXXXXXXXXXXX,3
0xC4a096dFFeA26Dxxxxxxxxxxxxxxxxxxxxxxxxxx,10
...
"""
import csv
import json
import os


DATA_DIR = './al/'

# Define the weights for each CSV file
weight = {
    '1.csv': 1,
    '2.csv': 2,
    '3.csv': 3,
}

# Initialize a dictionary to store the results
result = {}

# Process each CSV file
for filename, w in weight.items():
    print(f'Processing {filename} with weight {w}')
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for _ in range(2):  # Skip the first two rows
            try:
                next(reader)
            except StopIteration:
                break
        for row in reader:
            address = row[3]
            if address not in result:
                result[address] = {'maxClaimable': 0, 'details': {}}
            if filename not in result[address]['details']:
                result[address]['details'][filename] = 0
            result[address]['details'][filename] += 1
            result[address]['maxClaimable'] += w

# Write the result to a JSON file
with open('./al/al_result/result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# Create csv for check total count by weight
with open('./al/al_result/result.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['address', 'maxClaimable'])
    for address, data in result.items():
        writer.writerow([address, data['maxClaimable']])
