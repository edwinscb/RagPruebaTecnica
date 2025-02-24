import fitz  # PyMuPDF
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.db.database import create_db, insert_document
from chunker import split_text_into_chunks
from langdetect import detect
from deep_translator import GoogleTranslator

def extract_text_from_pdf(pdf_path):
    """Extrae el texto de un PDF y lo retorna sin traducir."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc, 1):
            text += f"\n--- Página {i} ---\n{page.get_text('text')}\n"

    return text.strip()

def translate_chunk(chunk):
    """Traduce un fragmento de texto si está en inglés."""
    if detect(chunk) == "en":
        return GoogleTranslator(source="en", target="es").translate(chunk)
    return chunk

if __name__ == "__main__":
    create_db()  # Crea la base de datos si no existe

    pdf_folder = "data"
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            
            extracted_text = extract_text_from_pdf(pdf_path)
            chunks = split_text_into_chunks(extracted_text)

            for i, chunk in enumerate(chunks):
                translated_chunk = translate_chunk(chunk)  # Traducción después del corte
                chunk_name = f"{filename}_chunk_{i}"
                insert_document(chunk_name, translated_chunk)

            print(f"{len(chunks)} fragmentos almacenados para {filename}")
