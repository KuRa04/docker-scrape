import requests
from bs4 import BeautifulSoup

# スクレイピングするURL
url = "https://www.aidma-hd.jp/?companyservice=3212&s=&post_type=case"

# ヘッダーを指定してリクエストを送信
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
}
response = requests.get(url, headers=headers)
response.raise_for_status()  # リクエストの成功を確認

# BeautifulSoupでHTMLを解析
soup = BeautifulSoup(response.text, "html.parser")

# データの格納用リスト
case_studies = []

# 'case-study__content--list' クラスを持つdivタグ内のaタグを取得
case_list = soup.find_all("div", class_="archive-case")
print(f"取得した件数: {case_list}")

for case in case_list:
    # URLの取得
    a_tag = case.find("a", href=True)
    if a_tag:
        case_url = a_tag["href"]
        
        # 企業名の取得
        company_name_tag = a_tag.find("p")
        company_name = company_name_tag.get_text(strip=True) if company_name_tag else "N/A"
        
        # 各タグ名の取得
        tags = []
        tag_div = case.find("div", class_="tag-list")
        if tag_div:
            for tag in tag_div.find_all("span"):
                tags.append(tag.get_text(strip=True))
        
        # 結果をリストに追加
        case_studies.append({
            "企業名": company_name,
            "URL": case_url,
            "タグ": tags
        })

# 結果の表示
for study in case_studies:
    print(f"企業名: {study['企業名']}")
    print(f"URL: {study['URL']}")
    print(f"タグ: {', '.join(study['タグ'])}")
    print("="*50)
