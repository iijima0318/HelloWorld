#seleniumの必要なライブラリをインポート
from selenium import webdriver
from selenium.webdriver.common.by import By

#tkinter（メッセージボックス表示）の必要なライブラリをインポート
import tkinter
from tkinter import messagebox

#chromeのwebドライバーインスタンスを作成
driver=webdriver.Chrome()

driver.get('https://mondai.ping-t.com/users/sign_in')