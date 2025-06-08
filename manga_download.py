import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from time import sleep

# ========== 設定ここから ==========

base_url = "https://www.mangajikan.com/chapter-15833.html"  # 保存したい最初の話数URL
chapter_count = 5                                           # 保存する話数（連番）
folder_name = "進撃の巨人_保存"                              # 保存フォルダ名（任意）

# ========== 設定ここまで ==========

# 保存先: デスクトップ配下
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
save_path = os.path.join(desktop_path, folder_name)
os.makedirs(save_path, exist_ok=True)

# チャプター番号取得
def extract_chapter_id(url):
    try:
        return int(url.split("chapter-")[-1].replace(".html", ""))
    except:
        raise ValueError("URLの形式が不正です")

start_id = extract_chapter_id(base_url)

for i in range(chapter_count):
    chapter_id = start_id + i
    chapter_url = f"https://www.mangajikan.com/chapter-{chapter_id}.html"
    print(f"[+] Downloading: {chapter_url}")

    try:
        response = requests.get(chapter_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # HTML保存
        html_path = os.path.join(save_path, f"chapter-{chapter_id}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        # 画像保存
        img_folder = os.path.join(save_path, f"chapter-{chapter_id}_images")
        os.makedirs(img_folder, exist_ok=True)

        for img in soup.find_all("img"):
            src = img.get("src")
            if src and src.startswith("http"):
                img_name = os.path.basename(urlparse(src).path)
                img_path = os.path.join(img_folder, img_name)

                try:
                    img_data = requests.get(src, timeout=10).content
                    with open(img_path, "wb") as out_file:
                        out_file.write(img_data)
                    print(f"  └ Saved image: {img_name}")
                except Exception as e:
                    print(f"  └ Failed image: {src} ({e})")

        sleep(1)  # サーバー負荷軽減のため1秒待機

    except Exception as e:
        print(f"[×] Failed to fetch {chapter_url}: {e}")
