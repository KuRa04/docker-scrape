# Pythonベースイメージを使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /usr/src/app

# 必要なパッケージをインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# スクリプトファイルをコピー
COPY . .

# スクリプトを実行
CMD ["python", "./scrape.py"]
