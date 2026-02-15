from ingestao import load_db
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatOpenAI(model=os.getenv("LLM_MODEL"))
db = load_db()

def get_retriever():
    return db.as_retriever(search_type="mmr", search_kwargs={"k": 4, "fetch_k": 10})

def get_qa_chain():
    prompt = ChatPromptTemplate.from_template("""
    Responda somente com base no contexto fornecido.
    
    Documentos:
    {context}

    Pergunta:
    {input}

    Resposta:
    """)
    document_chain = create_stuff_documents_chain(llm, prompt)
    qa_chain = create_retrieval_chain(
        get_retriever(),
        document_chain
    )
    return qa_chain

def ask_a_question(question):
    return get_qa_chain().invoke({
        "input": question 
    })
