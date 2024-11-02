from bs4 import BeautifulSoup
import csv


def extract_data_from_html(file_path):
    case_studies = []
    existing_companies = set()

    # HTMLファイルを読み込む
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')

    # alm-revealクラスを持つdivタグを取得
    case_list = soup.find_all("div", class_="alm-reveal")

    for case in case_list:
        # case-study__content--listクラスを持つdivタグを取得
        case_study_divs = case.find_all("div", class_="case-study__content--list")

        for case_study in case_study_divs:
            try:
                # URLの取得
                a_tag = case_study.find("a")
                case_url = a_tag['href'] if a_tag else "N/A"
              
                # 企業名の取得
                company_name_tag = a_tag.find("p") if a_tag else None
                company_name = company_name_tag.text.strip() if company_name_tag else "N/A"
                
                # すでに取得済みの企業名の場合はスキップ
                if company_name in existing_companies:
                    continue

                # 各タグ名の取得
                tags = []
                tag_div = case_study.find("div", class_="tag-list")
                if tag_div:
                    tag_elements = tag_div.find_all("span")
                    for tag in tag_elements:
                        tags.append(tag.text.strip())

                # 結果をリストに追加
                case_studies.append({
                    "企業名": company_name,
                    "ケーススタディ_URL": case_url,
                    "タグ": ", ".join(tags),
                })
                
                existing_companies.add(company_name)
                print(f"Data extracted for {company_name}")

            except Exception as e:
                print(f"Error while extracting data: {e}")

    return case_studies

html_file_path = "aidoma.html"  # HTMLファイルのパスを指定
case_studies_data = extract_data_from_html(html_file_path)
    
csv_file = 'output/case_studies_local_html.csv'
csv_columns = ['企業名', 'ケーススタディ_URL', 'タグ']

with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for case in case_studies_data:
        writer.writerow(case)

print(f"データを {csv_file} に書き込みました。")
