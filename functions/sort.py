import io

from pypdf import PdfReader, PdfWriter


def rearrange_pdf(pdf_bytes: io.BytesIO, order: list) -> io.BytesIO:
    pdf_reader = PdfReader(pdf_bytes)
    pdf_writer = PdfWriter()

    for page in order:
        pdf_writer.add_page(pdf_reader.pages[page])

    output = io.BytesIO()
    pdf_writer.write(output)
    output.seek(0)
    return output
