import csv
import datetime
import os
import re
import chardet

print("Current working directory:", os.getcwd())

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data=file.read()
    result=chardet.detect(raw_data)
    return result['encoding']

def replace_hostname_in_file(input_file, csv_file):
    #今日の日付の取得
    today_date=datetime.datetime.now().strftime('%Y%m%d')

    #CSVファイルから新しいホスト名を取得
    with open(csv_file, 'r') as file:
        reader=csv.reader(file)

        new_hostnames=[]
        ip_addresses=[]

        for row in reader:
            new_hostnames.append(row[0])
            ip_addresses.append(row[1])
    
        print(new_hostnames,ip_addresses)

    #文字コードを検出する
    input_encoding=detect_encoding(input_file)
    print(f'Detect encoding: {input_encoding}')

    #新しいホスト名を1つずつ適用
    for i, (new_hostname,ip_address) in enumerate(zip(new_hostnames,ip_addresses)):
        output_file=f'config_making\\{new_hostname}_{today_date}.conf'

        # コンフィグファイルの読み込み
        with open(input_file, 'r', encoding=input_encoding) as file:
            config_lines = file.readlines()

        # パターン定義
        pattern = re.compile(r'^\s{4}set hostname "(.*?)"')

        # コンフィグファイルの内容を置換
        with open(output_file, 'w', encoding=input_encoding) as file:
            for line in config_lines:
                
                # "set hostname"行のみ置換
                if pattern.match(line):
                    line = pattern.sub(f'    set hostname "{new_hostname}"', line)
                file.write(line)
        
        new_section = f"""
    edit "VLAN400"
        set vdom "root"
        set ip {ip_address} 255.255.255.128
        set allowaccess ping https ssh
        set device-identification enable
        set role lan
        set snmp-index 35
        set ip-managed-by-fortiipam disable
        set interface "mgmt"
        set vlanid 400
    next
    """

        with open(output_file, 'r', encoding=input_encoding) as file:
            config_content=file.read()
        
        #"edit "fortilink""の次の"next"の後に新しいセクションを追加する
        pattern_2=re.compile(r'(edit "fortilink".*?next)', re.DOTALL)
        modified_content=pattern_2.sub(r'\1'+new_section,config_content)

        with open(output_file, 'w', encoding=input_encoding) as file:
            file.write(modified_content)

        print(f'Generated file: {output_file}')

#入力ファイルとCSVファイルのパスを指定
input_file=r'config_making\ES01-FW-01_20240514.conf'
csv_file=r'config_making\hostname.csv'

replace_hostname_in_file(input_file,csv_file)