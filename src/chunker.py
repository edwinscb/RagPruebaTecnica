from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text_into_chunks(text, chunk_size=1000, overlap=200):
    """Divide el texto en fragmentos (chunks) con solapamiento."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)
