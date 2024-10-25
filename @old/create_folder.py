import os
import csv
import tkinter as tk
from tkinter import filedialog, messagebox

def create_folders():
    # CSVファイルのパスを取得
    csv_file_path = filedialog.askopenfilename(title="CSVファイルを選択", filetypes=[("CSV files", "*.csv")])
    if not csv_file_path:
        messagebox.showerror("エラー", "CSVファイルが選択されませんでした。")
        return

    # 保存先のディレクトリを選択
    save_dir = filedialog.askdirectory(title="保存先フォルダを選択")
    if not save_dir:
        messagebox.showerror("エラー", "保存先フォルダが選択されませんでした。")
        return

    try:
        # CSVファイルからフォルダ名を読み取り、フォルダを作成
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                folder_name = row[0]  # A列のデータを取得
                folder_path = os.path.join(save_dir, folder_name)
                os.makedirs(folder_path, exist_ok=True)
        
        messagebox.showinfo("完了", "フォルダーの作成が完了しました。")
    except Exception as e:
        messagebox.showerror("エラー", f"フォルダーの作成中にエラーが発生しました。\n{str(e)}")

# GUIの作成
root = tk.Tk()
root.title("フォルダー作成ツール")

# ボタンを配置
button = tk.Button(root, text="フォルダーを作成", command=create_folders)
button.pack(pady=20)

root.mainloop()
