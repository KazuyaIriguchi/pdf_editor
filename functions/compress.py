import subprocess
import argparse
import platform
import shutil


GHOSTSCRIPT_CMD = {"Windows": "gswin64c.exe", "Linux": "gs"}


def get_gs_path() -> str:
    """Ghostscriptのパスを取得する

    Returns:
        str: パス
    """
    return shutil.which(GHOSTSCRIPT_CMD.get(platform.system()))


def compress(input_file: str, output_name: str, command: str):
    """圧縮処理

    Args:
        input_file (str): 入力ファイル
        output_name (str): 出力ファイル名
        command (str): Ghostscriptのコマンド
    """
    print("Compressing...")

    subprocess.run(
        [
            command,
            "-sDEVICE=pdfwrite",  # 出力フォーマットとしてPDFを指定
            "-dCompatibilityLevel=1.4",  # 生成されるPDFをのバージョンを指定
            "-dPDFSETTINGS=/ebook",  # PDFの品質と圧縮レベルを指定
            "-dNOPAUSE",  # 処理の各ページで一時停止せず、全ページを連続して処理
            "-dQUIET",  # エラーメッセージやログメッセージの出力を抑制
            "-dBATCH",  # 処理が完了したらスクリプトを終了する
            "-sOutputFile=" + output_name,
            input_file,
        ]
    )

    print(f"Done. output: {output_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    parser.add_argument("--output_name", type=str, default="compressed.pdf")
    args = parser.parse_args()

    compress(args.input_file, args.output_name)
