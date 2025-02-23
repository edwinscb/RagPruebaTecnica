"""
Extrae texto de un PDF y lo guarda en un archivo de texto.
"""

import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"El archivo {pdf_path} no existe.")

    text = ""
    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc, 1):
            text += f"\n--- Página {i} ---\n{page.get_text('text')}\n"

    return text.strip()

if __name__ == "__main__":
    pdf_path = "data/document1.pdf"
    output_path = "data/extracted_text.txt"


    extracted_text = extract_text_from_pdf(pdf_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    print(f"Texto guardado en {output_path}")
