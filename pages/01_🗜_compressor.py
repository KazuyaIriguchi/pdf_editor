import streamlit as st
import os

from functions.compress import compress
from functions.common import save_as_pdf_from_bytes, load_pdf_as_bytes, remove_file

TEMP_DIR = "temp"


st.title("PDF data Compressor")
uploaded_files = st.file_uploader(
    "Upload PDF files", type=["pdf"], accept_multiple_files=True
)

if uploaded_files:
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    compressed_info = []
    with st.spinner("Compressing..."):
        for i, uploaded_file in enumerate(uploaded_files):
            uploaded_pdf = os.path.join(TEMP_DIR, f"uploaded.pdf")
            compressed_pdf = os.path.join(TEMP_DIR, "compressed.pdf")
            save_as_pdf_from_bytes(uploaded_file.read(), uploaded_pdf)
            compress(uploaded_pdf, compressed_pdf)
            compressed_info.append(
                {
                    "name": f"{uploaded_file.name}_{compressed_pdf}",
                    "data": load_pdf_as_bytes(compressed_pdf),
                }
            )
            remove_file(uploaded_pdf)
            remove_file(compressed_pdf)
    st.success("Done!")
    for info in compressed_info:
        st.download_button(
            label=f"Download {info['name']=}",
            data=info["data"],
            file_name=info["name"],
            mime="application/pdf",
        )
