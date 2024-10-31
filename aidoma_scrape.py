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

# ページの全体HTMLを表示
html_content = driver.page_source
print("全体のHTML:")
print(html_content) 

# # データの格納用リスト
# case_studies = []

# # 'archive-case' クラスを持つdivタグを取得
# case_list = driver.find_elements(By.CLASS_NAME, "archive-case")
# print(f"取得した件数: {len(case_list)}")

# for case in case_list:
#     # URLの取得
#     a_tag = case.find_element(By.TAG_NAME, "a")
#     case_url = a_tag.get_attribute("href")
    
#     # 企業名の取得
#     company_name_tag = a_tag.find_element(By.TAG_NAME, "p")
#     company_name = company_name_tag.text.strip() if company_name_tag else "N/A"
    
#     # 各タグ名の取得
#     tags = []
#     tag_div = case.find_element(By.CLASS_NAME, "tag-list")
#     if tag_div:
#         tag_elements = tag_div.find_elements(By.TAG_NAME, "span")
#         for tag in tag_elements:
#             tags.append(tag.text.strip())
    
#     # 結果をリストに追加
#     case_studies.append({
#         "企業名": company_name,
#         "URL": case_url,
#         "タグ": tags
#     })

# # 結果の表示
# for study in case_studies:
#     print(f"企業名: {study['企業名']}")
#     print(f"URL: {study['URL']}")
#     print(f"タグ: {', '.join(study['タグ'])}")
#     print("="*50)

# # ブラウザを閉じる
driver.quit()
