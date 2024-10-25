import csv

def generate_dhcp_config(csv_filename):
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        output_text = ""

        # デバッグ用にヘッダーを表示
        headers = reader.fieldnames
        print("CSV Headers:", headers)

        for row in reader:
            # デバッグ用に各行を表示
            print("CSV Row:", row)
            site_code = row['\ufeff拠点コード']
            vlan_name = row['VLAN Name']
            network_segment = row['ネットワークセグメント']
            gateway_address = row['ゲートウェイアドレス']

            output_text += f"ip dhcp pool {site_code}-{vlan_name}\n"
            output_text += f" network {network_segment}\n"
            output_text += f" default-router {gateway_address}\n"
            output_text += " dns-server 8.8.8.8\n"
            output_text += " exit\n\n"

        return output_text

# CSVファイルのパスを指定してください
csv_filename = r"C:\Users\artenica19\Desktop\workspace\浦安市教育委員会\SSID検証.csv"
config_text = generate_dhcp_config(csv_filename)
print(config_text)

# 必要に応じて、結果をファイルに保存
with open('dhcp_config.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(config_text)
