# ベースイメージとしてPython 3.9を使用
FROM python:3.9

# 必要なライブラリのインストール
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを指定
WORKDIR /usr/src/app

# 必要なライブラリをインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY . .

# Chromeオプションを設定
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver

# アプリケーションを起動
CMD ["python", "./aidma_scrape.py"]
