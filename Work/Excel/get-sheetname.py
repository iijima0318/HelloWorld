import pandas as pd
import tkinter as tk
from tkinter import filedialog

#ダイアログでExcelファイルを選択する関数
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path=filedialog.askopenfilename(
       title="Excelファイルを選択してください",
       filetypes=[("Excel files", "*.xlsx .xls")]
    )
    return file_path

#Excelファイルを選択
file_path = select_file()

#ファイルが選択されなかった場合の処理
if not file_path:
    print("Excelファイルが選択されませんでした。")
else:
    #シュル直結果を格納するリスト
    result = []

    #全シートをループして処理
    excel_file=pd.ExcelFile(file_path)
    for sheet_name in excel_file.sheet_names:
        #各シートをDataFrameとして読み込む
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        #"GE 1.0"を含むセルを探す
        found = df.isin(["GE a.0"])

        #"GE 1.0"が見つかった場合
        if found.any().any():
            #見つかったセルの位置を取得
            row , col = found.stack()[found.stack()].index[0]

            #右隣のセルの値を取得（列が最後の列でない場合）
            if col + 1 < len(df.columns):
                next_value=df.iat[row, col + 1]
                result.append(f"{sheet_name}   :   {next_value}")

#結果を出力
if result:
    for item in result:
        print(item)
    else:
        print("GE 1.0が含まれるセルが見つかりませんでした。")

