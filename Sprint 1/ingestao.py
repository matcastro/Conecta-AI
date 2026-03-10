from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from pathlib import Path
import os

def load_file(path):
    loader = PyPDFLoader(path)
    docs = loader.load()

    for doc in docs:
        doc.metadata["fonte"] = path.split('/')[1].replace(".pdf", "")
    
    return docs

def load_files():
    documents = []
    
    docs_cdc = load_file(os.getenv("CDC_PATH"))
    total_cdc = len(docs_cdc)
    documents.extend(docs_cdc)

    docs_lgpd = load_file(os.getenv("LGPD_PATH"))
    total_lgpd = len(docs_lgpd)
    documents.extend(docs_lgpd)

    print(f'Documentos CDC: {total_cdc}\nDocumentos LGPD: {total_lgpd}\nTotal de documentos: {len(documents)}')
    return documents

def recursive_chunk_docs(docs, overlap):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=overlap)
    chunks = text_splitter.split_documents(docs)
    return chunks

def chunk_docs(docs, overlap):
    text_splitter = CharacterTextSplitter(chunk_size=600, chunk_overlap=overlap, separator="\n\n")
    chunks = text_splitter.split_documents(docs)
    return chunks

def load_db():
    db_dir = Path(os.getenv("CHROMA_DB_PATH"))
    embedding = OpenAIEmbeddings(model=os.getenv("EMBEDDINGS_MODEL"))

    if(db_dir.exists()):
        print("Banco vetorial já existe. Carregando...")
        return Chroma(embedding_function=embedding, persist_directory=db_dir, collection_name="documentos_juridicos")
    
    documents = load_files()
    chunks = recursive_chunk_docs(documents, 100)
    print(f'\nDocuments: {len(documents)}\nChunks: {len(chunks)}')
    return Chroma.from_documents(chunks, embedding, persist_directory=str(db_dir), collection_name="documentos_juridicos")
    
def validate_retriver(retriever):
    # results = retriever_invoke("O fornecedor pode se eximir de responsabilidade?")
    results = retriever.invoke("Em que casos o consentimento é obrigatório?")
    for i, doc in enumerate(results):
        print(f"\nResult {i+1}")
        print(f"Source: {doc.metadata["fonte"]}")
        print(f"Content: {doc.page_content}")

load_dotenv()
# validate_retriver(get_retriever())
