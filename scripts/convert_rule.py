import requests
import hashlib
import os
import sys

RAW_URL = "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Clash-Classical.yaml"
OUTPUT_FILE = "AWAvenue-Ads-Rule-Clash-Classical.list"
HASH_FILE = "scripts/.last_hash"

def get_remote_file(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ 获取远程文件失败: {e}")
        sys.exit(1)

def calc_hash(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def load_last_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def save_hash(hash_val):
    with open(HASH_FILE, "w", encoding="utf-8") as f:
        f.write(hash_val)

def convert_yaml(raw_text):
    lines = raw_text.splitlines()
    converted_lines = []
    # 保留注释和规则之间空行（空行）
    last_was_comment_or_empty = False
    for line in lines:
        stripped = line.strip()
        if stripped == "payload:" or not stripped:
            # 跳过"payload:"，保留空行
            if not stripped:
                converted_lines.append("")
            continue
        if stripped.startswith("#"):
            converted_lines.append(line)
            last_was_comment_or_empty = True
            continue
        if stripped.startswith("- "):
            converted_lines.append(stripped[2:].strip())
            last_was_comment_or_empty = False
            continue
        # 其他行按需处理，这里默认忽略
    return "\n".join(converted_lines)

def main():
    print("🛰️ 获取远程规则...")
    raw_text = get_remote_file(RAW_URL)
    current_hash = calc_hash(raw_text)
    last_hash = load_last_hash()

    if current_hash == last_hash:
        print("✅ 规则未变更，无需更新。")
        return

    print("🔁 规则已更新，开始转换格式...")
    converted = convert_yaml(raw_text)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(converted)

    save_hash(current_hash)
    print(f"✅ 已生成文件：{OUTPUT_FILE}，并更新 SHA 缓存。")

if __name__ == "__main__":
    main()