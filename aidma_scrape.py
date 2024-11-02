from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import time

# ケーススタディURLが保存されているCSVファイルのパス
input_csv_file = 'aidma_casestudy_url.csv'
output_csv_file = 'output/case_study_details.csv'
csv_columns = ['ケーススタディ_URL', '事業内容', '会社HP']

# Chromeオプションを設定
chrome_options = Options()
chrome_options.add_argument("--headless")  # ヘッドレスモード
chrome_options.add_argument("--no-sandbox")  # サンドボックスを無効にする
chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shmのメモリ制限を回避
chrome_options.binary_location = "/usr/bin/chromium"  # Chromiumのパスを指定

# WebDriverを起動
driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)

driver.implicitly_wait(10)

# 入力CSVからケーススタディURLを読み込む
with open(input_csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    case_study_urls = [row['ケーススタディ_URL'] for row in reader]

# データを格納するリスト
case_study_details = []

for case_url in case_study_urls:
    try:
        driver.get(case_url)
        
        # 事業内容と会社HPのURLを取得
        business_content = None
        company_website = None
        try:
            overview_section = driver.find_element(By.CLASS_NAME, "single-content__introduction--desc")
            content_lists = overview_section.find_elements(By.CLASS_NAME, "single-content__introduction--desc__list")

            # 事業内容と会社HPを取得
            for content in content_lists:
                if "事業内容" in content.text:
                    business_content = content.find_elements(By.TAG_NAME, "p")[1].text
                elif "URL" in content.text:
                    company_website = content.find_element(By.TAG_NAME, "a").get_attribute("href")
        
        except Exception as e:
            print(f"Error accessing case details for {case_url}: {e}")

        # 結果をリストに追加
        case_study_details.append({
            "ケーススタディ_URL": case_url,
            "事業内容": business_content,
            "会社HP": company_website,
        })
        
        print(f"Data extracted for {case_url}")

        time.sleep(2)  # ページが読み込まれるのを待つ

    except Exception as e:
        print(f"Error while extracting data from {case_url}: {e}")

# CSVファイルの準備
with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for case in case_study_details:
        writer.writerow(case)

print(f"データを {output_csv_file} に書き込みました。")

# WebDriverを閉じる
driver.quit()