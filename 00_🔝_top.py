import streamlit as st
import re

# README.md ファイルを開く
with open("README.md", "r", encoding="utf-8") as file:
    contents = file.read()

# Markdownの画像リンクの正規表現パターン
image_pattern = re.compile(r"!\[.*?\]\((.*?)\)")

# README.mdの内容を行ごとに処理
for line in contents.split("\n"):
    # 行内の画像リンクを探す
    match = image_pattern.search(line)
    if match:
        # st.imageを使用して画像を表示
        image_path = match.group(1)
        st.image(image_path)

        # 画像リンクを削除して、残りのテキストを表示
        line = image_pattern.sub("", line)
        if line.strip():
            st.markdown(line)
    else:
        # 画像リンクがない場合、行をそのまま表示
        st.markdown(line)
