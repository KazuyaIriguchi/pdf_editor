import streamlit as st

from functions.common import pdf_to_images, create_zip_from_dict

if "images" not in st.session_state:
    st.session_state["images"] = None
if "uploaded_filename" not in st.session_state:
    st.session_state["uploaded_filename"] = ""

st.title("PDF to Image Converter")

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

    st.session_state.selected_order = selected_order

    if len(selected_order):
        selected_images = {}
        for idx in selected_order:
            selected_images[idx] = images[idx]
        zip_data = create_zip_from_dict(selected_images)
        st.download_button(
            label=f"Download Selected Images as ZIP: {','.join(list(map(str, map(lambda x: x+1, selected_order))))}",
            data=zip_data,
            file_name="selected_images.zip",
            mime="application/zip",
        )
