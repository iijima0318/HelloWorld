import os
import csv

def find_poe_files(directory):
    poe_files = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            if "PoE" in file_name and file_name.endswith(".txt"):
                file_path = os.path.join(root, file_name)
                poe_files.append(file_path)
    return poe_files

def read_replacement_patterns(csv_file):
    patterns = []
    with open(csv_file, 'r', encoding='utf-8', errors='ignore') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                patterns.append((row[0].strip(), row[1].strip()))
    return patterns

def replace_multiline_text_in_file(file_path, patterns):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    
    new_content = content
    found_any = False
    for search_text, replacement_text in patterns:
        search_text = search_text.replace('\\n', '\n')  # CSVから読み込んだテキストを正しい改行形式に変換
        replacement_text = replacement_text.replace('\\n', '\n')  # 置換後のテキストも同様に変換
        if search_text in new_content:
            found_any = True
            new_content = new_content.replace(search_text, replacement_text)
    
    with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
        file.write(new_content)
    if found_any:
        print(f'Replaced text in {file_path}')
    else:
        print(f'{file_path}: 検索対象が見つかりませんでした。')

def process_files_in_directory(directory, patterns):
    poe_files = find_poe_files(directory)
    for file_path in poe_files:
        replace_multiline_text_in_file(file_path, patterns)

# 使用例
directory = input("ディレクトリのパスを入力してください: ")
csv_file = input("CSVファイルのパスを入力してください: ")

patterns = read_replacement_patterns(csv_file)
process_files_in_directory(directory, patterns)
