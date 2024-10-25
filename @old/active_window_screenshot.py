import pyautogui
from PIL import ImageGrab
import time
import os
from datetime import datetime

def take_screenshot():
    # スクリプト実行前にウィンドウをアクティブにするための待機時間（例：5秒）
    time.sleep(0.1)

    # アクティブなウィンドウの位置とサイズを取得
    window = pyautogui.getActiveWindow()
    x, y, width, height = window.left, window.top, window.width, window.height

    # タイトルバーの高さを考慮したオフセットを加える
    # これはOSやアプリケーションによって異なる場合があるので、調整が必要です。
    title_bar_height = 130  # 例として130ピクセル

    # ファイル名が重複しないようにファイル名に連番を追加
    filename = "screenshot"
    extension = ".png"
    now=datetime.now()
    date=now.strftime("%Y%m%d_%H%M%S")
    new_filename = f"{filename}_{date}{extension}"
    
    """
    # 同名のファイルが存在する場合は、番号をインクリメント
    while os.path.exists(new_filename):
        counter += 1
        new_filename = f"{filename}{counter}{extension}"
    """

    # アクティブウィンドウのスクリーンショットを取得（タイトルバーを除外）
    screenshot = ImageGrab.grab(bbox=(x, y + title_bar_height, x + width, y+height))

    # スクリーンショットを保存
    screenshot.save(new_filename)
    print(f"Screenshot saved as {new_filename}")

if __name__ == "__main__":
    take_screenshot()
