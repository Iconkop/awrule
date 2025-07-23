import requests
import hashlib
import os

RAW_URL = "https://cdn.jsdelivr.net/gh/TG-Twilight/AWAvenue-Ads-Rule@main/Filters/AWAvenue-Ads-Rule-Clash-Classical.yaml"
OUTPUT_FILE = "AWAvenue-Ads-Rule-Clash-Classical.list"
HASH_FILE = "scripts/.last_hash"

def get_remote_file(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def calc_hash(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def load_last_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_hash(hash_val):
    with open(HASH_FILE, "w") as f:
        f.write(hash_val)

def convert_yaml(raw_text):
    lines = raw_text.strip().splitlines()
    converted_lines = []
    for line in lines:
        line = line.strip()
        if line == "payload:" or not line:
            continue
        if line.startswith("- "):
            converted_lines.append(line[2:].strip())
    return "\n".join(converted_lines)

def main():
    print("🛰️ 获取远程规则...")
    raw_text = get_remote_file(RAW_URL)
    current_hash = calc_hash(raw_text)
    last_hash = load_last_hash()

    if current_hash == last_hash:
        print("✅ 无需更新。")
        return

    print("🔁 检测到更新，开始转换格式...")
    converted = convert_yaml(raw_text)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(converted)

    save_hash(current_hash)
    print(f"✅ 已生成文件：{OUTPUT_FILE}")

if __name__ == "__main__":
    main()