import requests
from bs4 import BeautifulSoup
import csv
import os

BASE_URL = "https://eigyo-mfg.com"
CASE_LIST_URL = BASE_URL + "/casestudy/casestudy_category/eigyo-engine"
OUTPUT_FILE = "output/client_data.csv"

# CSVヘッダーの初期化
CSV_HEADER = ["URL"]

def scrape_detail_page(detail_url):
    try:
        response = requests.get(detail_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # data の初期化
        data = {
            "URL": detail_url,
        }

        # <div class="right-wrap"> の中から ul を取得
        right_wrap = soup.select_one("div.right-wrap")

        if right_wrap:  # right_wrap が None でない場合
            # ul タグ内のすべての li タグを取得（info-list-item のみ）
            li_elements = right_wrap.select("ul.info-list li.info-list-item")

            # 順番に代入
            for li in li_elements:
                title_elem = li.select_one("p.ttl")  # タイトルを取得
                lead_text_elem = li.select_one("p.lead-txt")  # lead-txt を取得
                
                if title_elem and lead_text_elem:  # 要素が存在するか確認
                    title = title_elem.text.strip()  # タイトルを取得
                    lead_text = lead_text_elem.text.strip()  # lead-txt を取得
                    
                    # 新しいタイトルの場合、ヘッダーに追加
                    if title not in data:
                        data[title] = lead_text
                        if title not in CSV_HEADER:
                            CSV_HEADER.append(title)  # 新しいタイトルをCSVヘッダーに追加

        # デバッグ用に出力
        print(data)
        return data
    except Exception as e:
        print(f"Error scraping {detail_url}: {e}")
        return None

def scrape_case_study_pages():
    current_page = 1
    all_data = []

    while True:
        if current_page == 1:
            url = CASE_LIST_URL
        else:
            url = f"{CASE_LIST_URL}/page/{current_page}/"

        response = requests.get(url)
        if response.status_code != 200:
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        case_links = [a['href'] for a in soup.select('.casestudy-list-item a')]

        if not case_links:
            break

        for link in case_links:
            if not link.startswith("http"):
                detail_url = BASE_URL + link
            else:
                detail_url = link
            data = scrape_detail_page(detail_url)
            if data and data["URL"] != CASE_LIST_URL:  # データが正常に取得できた場合かつURLが詳細ページの場合
                all_data.append(data)
                print(f"Scraped data from {detail_url}")

        current_page += 1
    
    return all_data

def save_to_csv(data):
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=CSV_HEADER)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    scraped_data = scrape_case_study_pages()
    save_to_csv(scraped_data)
