import requests
from bs4 import BeautifulSoup
import csv
import os

BASE_URL = "https://eigyo-mfg.com"
CASE_LIST_URL = BASE_URL + "/casestudy/casestudy_category/eigyo-engine"
OUTPUT_FILE = "output/client_data.csv"

# CSVヘッダーを番号で指定
CSV_HEADER = ["URL", "所在地", "会社HP", "従業員数", "事業内容", "得意な材質", "得意な大きさ", "得意な板厚", "得意なロット"]

def scrape_detail_page(detail_url):
    try:
        response = requests.get(detail_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # data の初期化
        data = {
            "URL": detail_url,
            "所在地": None,
            "会社HP": None,
            "従業員数": None,
            "事業内容": None,
            "得意な材質": None,
            "得意な大きさ": None,
            "得意な板厚": None,
            "得意なロット": None,
        }

        # <div class="right-wrap"> の中から ul を取得
        right_wrap = soup.select_one("div.right-wrap")

        if right_wrap:  # right_wrap が None でない場合
            # ul タグ内のすべての li タグを取得（info-list-item のみ）
            li_elements = right_wrap.select("ul.info-list li.info-list-item")

            # 順番にリストに代入
            lead_texts = []
            for li in li_elements:
                lead_text_elem = li.select_one("p.lead-txt")  # lead-txt を取得
                
                if lead_text_elem:  # 要素が存在するか確認
                    lead_text = lead_text_elem.text.strip()  # lead-txt を取得
                    lead_texts.append(lead_text)  # リストに追加

            # dataにリストを格納
            for i, text in enumerate(lead_texts):
                if i < len(CSV_HEADER) - 1:  # CSV_HEADERのサイズを考慮
                    data[CSV_HEADER[i + 1]] = text  # 順番に代入（URLは最初にあるため +1）

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
            
            if detail_url != CASE_LIST_URL:  # 不要なURLをスキップ
                data = scrape_detail_page(detail_url)
                if data:  # データが正常に取得できた場合
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
