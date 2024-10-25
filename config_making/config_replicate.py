import csv
import datetime
import os

print("Current working directory:", os.getcwd())

def replace_hostname_in_file(input_file, csv_file):
    #今日の日付の取得
    today_date=datetime.datetime.now().strftime('%y%m%d')

    #CSVファイルから新しいホスト名を取得
    with open(csv_file, 'r') as file:
        reader=csv.reader(file)
        new_hostname=[row[0] for row in reader]

    #新しいホスト名を1つずつ適用
    for i, new_hostname in enumerate(new_hostname):
        output_file=f'{new_hostname}_{today_date}.conf'

        with open(input_file, 'r', encoding='utf-8') as file:
            content=file.read()

        #"set hostname"の後ろにある文字列を新しいホスト名に置換
        new_content=content.replace('set hostname', f'set hostname {new_hostname}')

        #新しいホスト名で保存
        with open(output_file, 'w') as file:
            file.write(new_content)
        print(f'Generated file: {output_file}')

#入力ファイルとCSVファイルのパスを指定
input_file='config_making\ES01-FW-01_20240514.conf'
csv_file=f'config_making\hostname.csv'

replace_hostname_in_file(input_file,csv_file)