from selenium import webdriver

#環境変数で設定するとここではchrome driverのパスを指定する必要はない
driver=webdriver.Chrome()

#Googleのページを開く
driver.get('https://www.google.com')

print("ページタイトル：",driver.title)

#ブラウザを閉じる
driver.quit()

