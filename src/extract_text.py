import fitz  # PyMuPDF
import os
from database import create_db, insert_document

def extract_text_from_pdf(pdf_path):
    """Extrae el texto de un PDF."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc, 1):
            text += f"\n--- Página {i} ---\n{page.get_text('text')}\n"
    return text.strip()

if __name__ == "__main__":
    create_db()  # Crear la base de datos si no existe

    pdf_folder = "data"
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            extracted_text = extract_text_from_pdf(pdf_path)
            insert_document(filename, extracted_text)
            print(f"Texto extraído y almacenado para {filename}")
