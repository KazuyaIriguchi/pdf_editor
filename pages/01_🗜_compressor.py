import streamlit as st

import os
import tempfile

from functions.compress import compress, get_gs_path
from functions.common import (
    save_as_pdf_from_bytes,
    load_pdf_as_bytes,
    remove_file,
    detect_os,
)


st.title("PDF data Compressor")

# Ghostscriptのパスが見つからなかったら教える
command = get_gs_path()
if command is None:
    reference_msg = ""
    if detect_os() == "Windows":
        reference_msg = "refer: [Ghostscript : Releases](https://ghostscript.com/releases/index.html)"
    elif detect_os() == "Linux":
        reference_msg = "`sudo apt install ghostscript`"
    elif detect_os() == "Darwin":
        reference_msg = "`brew install ghostscript`"
    st.error(
        f"""
        Ghostscript is not found. Please install Ghostscript.

        {reference_msg}
        """
    )

else:
    uploaded_files = st.file_uploader(
        "Upload PDF files", type=["pdf"], accept_multiple_files=True
    )

    if uploaded_files:
        with st.spinner("Compressing..."):
            with tempfile.TemporaryDirectory() as tmpdirname:
                compressed_info = []
                for i, uploaded_file in enumerate(uploaded_files):
                    uploaded_pdf = os.path.join(tmpdirname, f"uploaded.pdf")
                    compressed_pdf = os.path.join(tmpdirname, "compressed.pdf")
                    save_as_pdf_from_bytes(uploaded_file.read(), uploaded_pdf)
                    compress(uploaded_pdf, compressed_pdf, command)
                    compressed_info.append(
                        {
                            "name": f"{os.path.splitext(uploaded_file.name)[0]}_{i}_compressed.pdf",
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
