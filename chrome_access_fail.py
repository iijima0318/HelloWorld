from selenium import webdriver

# ChromeDriverのパスを指定(Windowsの場合)
driver_path = "C:\Users\artenica19\HelloWorld\application\chromedriver-win32\chromedriver.exe"  
driver = webdriver.Chrome(executable_path=driver_path)

# URLにアクセス
driver.get("https://www.example.com")

# ブラウザを表示(確認用)
driver.maximize_window() 

# 処理が終わったらブラウザを閉じる
driver.quit()
