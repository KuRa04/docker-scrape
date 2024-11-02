import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# CSVファイルからURLを読み込む
def load_case_study_urls(csv_file):
    df = pd.read_csv(csv_file)
    return df['URL'].tolist()  # 'URL'カラムのリストを返す

# ケーススタディのデータを取得する関数
def fetch_case_study_data(driver, urls):
    case_studies = []
    
    for case_url in urls:
        driver.get(case_url)
        time.sleep(5)  # ページが読み込まれるのを待つ
        
        business_content = None
        company_website = None

        try:
            overview_section = driver.find_element(By.CLASS_NAME, "single-content__introduction--desc")
            content_lists = overview_section.find_elements(By.CLASS_NAME, "single-content__introduction--desc__list")
            
            # 事業内容と会社のURLを取得
            for content in content_lists:
                if "事業内容" in content.text:
                    business_content = content.find_elements(By.TAG_NAME, "p")[1].text
                elif "URL" in content.text:
                    company_website = content.find_element(By.TAG_NAME, "a").get_attribute("href")
        
        except Exception as e:
            print(f"Error accessing case details for {case_url}: {e}")

        # 取得したデータをリストに追加
        case_studies.append({

            "URL": case_url,
            "事業内容": business_content,
            "会社HP": company_website,
        })

    return case_studies

csv_file_path = "aidma_casestudy_url.csv"  # CSVファイルのパスを指定
output_csv_file = "output/case_studies_overview.csv"  # 出力先のCSVファイル名
urls = load_case_study_urls(csv_file_path)

# Selenium WebDriverの初期化
driver = webdriver.Chrome()  # Chromeドライバーの設定（必要に応じてオプションを追加）

try:
    case_studies_data = fetch_case_study_data(driver, urls)
    
    # 結果の表示
    for study in case_studies_data:
        print(study)

finally:
    driver.quit()  # WebDriverを閉じる
