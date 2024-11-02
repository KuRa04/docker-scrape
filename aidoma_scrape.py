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

# スクロールする関数
def scroll_and_collect_data(driver):
    case_studies = []  # データを格納するリスト
    existing_companies = set() 
    last_height = driver.execute_script("return document.body.scrollHeight")  # 初期の高さを取得
    
    while True:
        # 現在のcase-study__content--listの個数を取得
        # 新しいデータを取得
        case_list = driver.find_elements(By.CLASS_NAME, "case-study__content--list")
        
        for case in case_list:
            try:
                # URLの取得
                a_tag = case.find_element(By.TAG_NAME, "a")
                case_url = a_tag.get_attribute("href")
              
                # 企業名の取得
                company_name_tag = a_tag.find_element(By.TAG_NAME, "p")
                company_name = company_name_tag.text.strip() if company_name_tag else "N/A"
                
                # すでに取得済みの企業名の場合はスキップ
                if company_name in existing_companies:
                  continue

                # 各タグ名の取得
                tags = []
                tag_div = case.find_element(By.CLASS_NAME, "tag-list")
                if tag_div:
                    tag_elements = tag_div.find_elements(By.TAG_NAME, "span")
                    for tag in tag_elements:
                        tags.append(tag.text.strip())

                # ケーススタディのページに遷移
                # driver.get(case_url)

                # 必要に応じて待機時間を調整
                # time.sleep(5)

                # business_content = None
                # company_website = None

                # # 事業内容と会社HPの取得
                # try: 
                #   overview_section = driver.find_elements(By.CLASS_NAME, "single-content__introduction--desc")
                #   content_lists = overview_section.find_elements(By.CLASS_NAME, "single-content__introduction--desc__list")

                #   for content in content_lists:
                #     if "事業内容" in content.text:
                #         business_content = content.find_elements(By.TAG_NAME, "p")[1].text
                #     elif "URL" in content.text:
                #         company_website = content.find_element(By.TAG_NAME, "a").get_attribute("href")

                # except Exception as e:
                #     print(f"Error accessing case details for {company_name}: {e}")

                # 結果をリストに追加
                case_studies.append({
                    "企業名": company_name,
                    # "会社HP": company_website,
                    # "事業内容": business_content,
                    "ケーススタディ_URL": case_url,
                    "タグ": ", ".join(tags),
                })
                
                existing_companies.add(company_name)
                print(f"Data extracted for {existing_companies}")

                # トップページに戻る
                # driver.back()
                # time.sleep(5)  # Adjust waiting time as needed

            except Exception as e:
                print(f"Error while extracting data: {e}")

        # 画面の半分までスクロールダウン
        driver.execute_script("window.scrollBy(0, 2500);")
        
        # スクロール後の待機時間
        time.sleep(5)
        print("Scrolled down")

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        
        last_height = new_height  # 高さを更新
      
    return case_studies


# ページの読み込み待ち
time.sleep(5)

# スクロールしながらデータを取得
case_studies = scroll_and_collect_data(driver)

# CSVファイルの準備
csv_file = 'output/case_studies.csv'
csv_columns = ['企業名', 'ケーススタディ_URL', 'タグ']

with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for case in case_studies:
        writer.writerow(case)

print(f"データを {csv_file} に書き込みました。")