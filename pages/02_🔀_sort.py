import streamlit as st

from functions.common import pdf_to_images, check_ext_name
from functions.sort import rearrange_pdf


if "images" not in st.session_state:
    st.session_state["images"] = None
if "uploaded_filename" not in st.session_state:
    st.session_state["uploaded_filename"] = ""

# PDFのページを並べ替えるツール
st.title("PDF sorting")

uploaded_file = st.file_uploader("Upload PDF File", type=["pdf"])
if uploaded_file:
    if uploaded_file.name != st.session_state.uploaded_filename:
        st.session_state.uploaded_filename = uploaded_file.name
        pdf_bytes = uploaded_file.getvalue()
        with st.spinner("Processing..."):
            st.session_state.images = pdf_to_images(pdf_bytes)

    images = st.session_state.images
    num_of_images = len(images)

    selected_order = st.session_state.get("selected_order", [])

    # 3列のカラムを作成して画像とチェックボックスを表示
    for i in range(0, num_of_images, 3):
        cols = st.columns(3)
        for j in range(3):
            index = i + j
            if index < num_of_images:
                with cols[j]:
                    st.image(
                        images[index], caption=f"ページ {index + 1}", use_column_width=True
                    )
                    checked = index in selected_order
                    if st.checkbox(f"ページ {index + 1}", key=index, value=checked):
                        if index not in selected_order:
                            selected_order.append(index)
                    elif index in selected_order:
                        selected_order.remove(index)

    # テキストボックスでの表示を1始まりにして反映
    page_order_input = st.text_input(
        "ページの順序をカンマ区切りで入力してください (例: 1,3,2)",
        ",".join([str(i + 1) for i in selected_order]),
    )

    if page_order_input:
        try:
            # 1始まりを0始まりに変換
            selected_order = [int(i) - 1 for i in page_order_input.split(",")]
            if not all(0 <= i < num_of_images for i in selected_order):
                st.warning("無効なページ順序が入力されました。")
                selected_order = []
        except ValueError:
            st.warning("無効な入力です。数字とカンマのみを使用してください。")
            selected_order = []

    st.session_state.selected_order = selected_order

    output_name = st.text_input("出力ファイル名", value="rearranged.pdf")
    if st.button("並び替え"):
        if not check_ext_name(output_name):
            output_name += ".pdf"
        rearranged_pdf = rearrange_pdf(uploaded_file, selected_order)
        st.download_button(
            "ダウンロード",
            rearranged_pdf,
            file_name=output_name,
            mime="application/pdf",
        )
