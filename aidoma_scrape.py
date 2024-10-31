from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
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
# CSVファイルの準備
csv_file = 'output/case_studies.csv'
csv_columns = ['企業名', 'URL', 'タグ']
case_studies = []

# 'case-study__content--list' クラスを持つdivタグを取得
case_list = driver.find_elements(By.CLASS_NAME, "case-study__content--list")

for case in case_list:
    # URLの取得
    a_tag = case.find_element(By.TAG_NAME, "a")
    case_url = a_tag.get_attribute("href")
    
    # 企業名の取得
    company_name_tag = a_tag.find_element(By.TAG_NAME, "p")
    company_name = company_name_tag.text.strip() if company_name_tag else "N/A"
    
    # 各タグ名の取得
    tags = []
    tag_div = case.find_element(By.CLASS_NAME, "tag-list")
    if tag_div:
        tag_elements = tag_div.find_elements(By.TAG_NAME, "span")
        for tag in tag_elements:
            tags.append(tag.text.strip())
    
    # 結果をリストに追加
    case_studies.append({
        "企業名": company_name,
        "URL": case_url,
        "タグ": ", ".join(tags)  # タグをカンマ区切りで結合
    })

print(f"取得したデータ: {case_studies}")

driver.quit()

try:
    with open('output/case_studies.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = case_studies[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for case in case_studies:
            writer.writerow(case)
except Exception as e:
    print(f"Error occurred: {e}")

print(f"結果を {csv_file} に保存しました。")