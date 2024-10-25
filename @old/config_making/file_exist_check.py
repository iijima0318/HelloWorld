import os

# スクリプトのディレクトリを基にフルパスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, 'hostname.csv')
#input_file_path = os.path.join(script_dir, 'input.conf')

print(f"CSV file exists: {os.path.exists(csv_file_path)}")
print(csv_file_path)
#print(f"Input file exists: {os.path.exists(input_file_path)}")

if not os.path.exists(csv_file_path):
    print(f"CSV file not found at: {csv_file_path}")
#if not os.path.exists(input_file_path):
#    print(f"Input file not found at: {input_file_path}")
