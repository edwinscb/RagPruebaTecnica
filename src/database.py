import sqlite3

DB_PATH = "data/extracted_text.db"

def create_db():
    """Crea la base de datos y la tabla si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_archivo TEXT UNIQUE,
            contenido_texto TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_document(nombre_archivo, contenido_texto):
    """Inserta un fragmento de texto en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO documentos (nombre_archivo, contenido_texto) VALUES (?, ?)", 
                       (nombre_archivo, contenido_texto))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"El fragmento {nombre_archivo} ya está en la base de datos.")
    conn.close()

def get_documents():
    """Recupera todos los documentos almacenados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre_archivo, contenido_texto FROM documentos")
    documentos = cursor.fetchall()
    conn.close()
    return documentos
