import os
import io
import platform


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
