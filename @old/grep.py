import os
import re
from tkinter import Tk, filedialog

def get_folder_path():
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    return folder_path

def extract_device_serial_number(folder_path, filter_string):
    output_file = "output.txt"
    with open(output_file, 'w') as out_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if filter_string in file:
                    file_path = os.path.join(root, file)
                    host_name_match = re.search(r'5_(.*)_ES01-PoE-01\.log', file)
                    if host_name_match:
                        host_name = host_name_match.group(1)
                        with open(file_path, 'r') as f:
                            for line in f:
                                if 'DEVICE_SERIAL_NUMBER' in line:
                                    serial_number = line.split(':', 1)[1].strip()
                                    out_file.write(f"{host_name}: {serial_number}\n")

if __name__ == "__main__":
    filter_string = input("フィルタリングに使用する文字列を入力してください: ")
    folder_path = get_folder_path()
    extract_device_serial_number(folder_path, filter_string)
    print("抽出が完了しました。出力結果はoutput.txtに保存されました。")
