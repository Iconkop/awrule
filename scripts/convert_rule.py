import requests
import hashlib
import os
import sys
from datetime import datetime

# 原始规则地址（仍然拉取的是 TG-Twilight 仓库）
RAW_URL = "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Clash-Classical.yaml"

# 输出文件及缓存哈希
OUTPUT_FILE = "AWAvenue-Ads-Rule-Clash-Classical.list"
HASH_FILE = "scripts/.last_hash"

# 你自己的仓库信息
REPO_URL = "https://github.com/Iconkop/awrule"
REPO_BRANCH = "main"

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
    os.makedirs(os.path.dirname(HASH_FILE), exist_ok=True)
    with open(HASH_FILE, "w", encoding="utf-8") as f:
        f.write(hash_val)

def get_now_string():
    # 转换时间格式：2025-07-24 23:10:56 UTC+8
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC+8")

def convert_yaml(raw_text):
    lines = raw_text.splitlines()
    header_lines = []
    rule_lines = []
    in_payload = False

    for line in lines:
        stripped = line.strip()
        if stripped == "payload:":
            in_payload = True
            continue
        if not in_payload:
            if stripped.startswith("Title:"):
                line = "#" + line  # 补注释符
            header_lines.append(line)
        else:
            if stripped.startswith("- "):
                rule_lines.append(stripped[2:].strip())

    # 顶部声明块：转换说明 + 仓库链接 + 时间
    meta_block = [
        "# This file was auto-converted from Clash Classical YAML format.",
        f"# Repository: {REPO_URL}",
        f"# Branch: {REPO_BRANCH}",
        f"# Converted at: {get_now_string()}",
        ""
    ]

    # 拼接完整内容（只保留一个空行）
    return "\n".join(meta_block + header_lines).rstrip() + "\n\n" + "\n".join(rule_lines)

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

    os.makedirs(os.path.dirname(OUTPUT_FILE) or ".", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(converted)

    save_hash(current_hash)
    print(f"✅ 已生成文件：{OUTPUT_FILE}，并更新 SHA 缓存。")

if __name__ == "__main__":
    main()