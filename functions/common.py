import os
import io
import platform
import zipfile

from pypdf import PdfReader
from pdf2image import convert_from_bytes
from PIL import Image


def save_as_pdf_from_bytes(pdf_bytes: io.BytesIO, filename: str):
    """バイナリデータをPDFファイルとして保存

    Args:
        pdf_bytes (_type_): バイナリデータ
        filename (str): ファイル名
    """
    with open(filename, "wb") as f:
        f.write(pdf_bytes)


def load_pdf_as_bytes(filename: str) -> io.BytesIO:
    """PDFファイルをバイナリデータとして読み込む

    Args:
        filename (str): ファイル名

    Returns:
        io.BytesIO: バイナリデータ
    """
    with open(filename, "rb") as f:
        return f.read()


def load_pdf_as_pdf_reader(pdf_bytes: io.BytesIO) -> PdfReader:
    """PDFファイルをPdfReaderオブジェクトとして読み込む

    Args:
        pdf_bytes (io.BytesIO): PDFファイルのバイナリデータ

    Returns:
        PdfReader: PdfReaderオブジェクト
    """
    return PdfReader(pdf_bytes)


def remove_file(filename: str):
    """ファイル削除

    Args:
        filename (str): ファイル名
    """
    os.remove(filename)


def detect_os() -> str:
    """OSを検出

    Returns:
        str: OS名
    """
    return platform.system()


def pdf_to_images(pdf_bytes: io.BytesIO()) -> list:
    """PDFファイルを画像に変換

    Args:
        pdf_bytes (io.BytesIO): PDFファイルのバイナリデータ

    Returns:
        list: 画像のリスト
    """
    return convert_from_bytes(pdf_bytes)


def check_ext_name(filename: str, ext: str = ".pdf") -> bool:
    """拡張子名のチェック

    Args:
        filename (str): ファイル名

    Returns:
        bool: 拡張子名がextならTrue
    """
    return filename.endswith(ext)


def image_to_bytes(image: Image.Image) -> io.BytesIO:
    img_byte_io = io.BytesIO()
    image.save(img_byte_io, format="PNG")
    img_byte_io.seek(0)
    return img_byte_io


def create_zip_from_dict(images: dict) -> io.BytesIO:
    """画像のリストをZIPファイルに変換

    Args:
        images (list): 画像のリスト

    Returns:
        io.BytesIO: ZIPファイルのバイナリデータ
    """
    zip_byte_io = io.BytesIO()
    with zipfile.ZipFile(zip_byte_io, "w") as zf:
        for i, image in images.items():
            image_byte_io = image_to_bytes(image)
            zf.writestr(f"page_{i+1}.png", image_byte_io.getvalue())
    zip_byte_io.seek(0)
    return zip_byte_io
