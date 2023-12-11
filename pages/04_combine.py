import streamlit as st
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
import io


def resize_image_to_a4(image):
    A4_RATIO = 595 / 842  # A4サイズの比率（幅/高さ）
    image_ratio = image.width / image.height

    if image_ratio > A4_RATIO:
        # 幅ベースでリサイズ
        new_width = 595
        new_height = round(595 / image_ratio)
    else:
        # 高さベースでリサイズ
        new_height = 842
        new_width = round(842 * image_ratio)

    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized_image


def calculate_dpi(image_size, target_size=(595, 842)):
    # ターゲットサイズ（A4）に基づいてDPIを計算
    dpi_x = image_size[0] / (target_size[0] / 72)
    dpi_y = image_size[1] / (target_size[1] / 72)
    return (dpi_x + dpi_y) / 2  # 平均DPIを使用


def ensure_pdf_extension(filename):
    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"
    return filename


st.title("PDF and Image Merger")

uploaded_files = st.file_uploader("Choose PDFs or Images", accept_multiple_files=True)
merged_pdf = PdfWriter()

for uploaded_file in uploaded_files:
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            merged_pdf.add_page(page)
    else:
        image = Image.open(uploaded_file)
        resized_image = resize_image_to_a4(image)
        pdf_bytes = io.BytesIO()
        dpi = calculate_dpi(resized_image.size)
        resized_image.save(pdf_bytes, format="PDF", resolution=dpi)
        pdf_reader = PdfReader(pdf_bytes)
        merged_pdf.add_page(pdf_reader.pages[0])

# ファイル名の入力フィールドを追加
file_name = st.text_input("Enter the name of the merged file", value="merged.pdf")

if st.button("Merge and Download"):
    pdf_bytes = io.BytesIO()
    merged_pdf.write(pdf_bytes)
    pdf_bytes.seek(0)
    final_file_name = ensure_pdf_extension(file_name)  # 拡張子を確認し、必要に応じて追加
    st.download_button(
        label="Download Merged PDF",
        data=pdf_bytes,
        file_name=final_file_name,
        mime="application/pdf",
    )
