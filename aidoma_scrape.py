from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# スクレイピングするURL
url = "https://www.aidma-hd.jp/?companyservice=3212&s=&post_type=case"

# Chromeオプションを設定
chrome_options = Options()
chrome_options.add_argument("--headless")  # ヘッドレスモード
chrome_options.add_argument("--no-sandbox")  # サンドボックスを無効にする
chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shmのメモリ制限を回避
chrome_options.binary_location = "/usr/bin/chromium"  # Chromiumのパスを指定

# WebDriverを起動
driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)

driver.implicitly_wait(10)

driver.get(url)

# ページの読み込みを待機
time.sleep(5)  # 必要に応じて待機時間を調整

# スクロールする関数
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # スクロールダウン
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # 新しい高さを取得
        time.sleep(5)  # スクロール後の待機時間
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # 新しい高さが変わらなければ終了
        if new_height == last_height:
            break
        
        last_height = new_height

# ページの一番下までスクロール
scroll_to_bottom(driver)

# ページの全体HTMLを表示
html_content = driver.page_source
print("全体のHTML:")
print(html_content) 

driver.quit()
