from PyPDF2  import PdfReader
from  langchain_text_splitters  import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, OpenAI
import os
import secret_key
os.environ["openai_api_key"]=secret_key.secret_key



def pdf_reader(pdf_path):

    text=""

    reader=PdfReader(pdf_path)

    for pages in reader.pages:

        text+=pages.extract_text()
    
    return text


def text_chunking(text,chunk_size=1000,chunk_overlap=200):

    splitter=RecursiveCharacterTextSplitter(
        chunk_overlap=chunk_overlap,
        chunk_size=chunk_size,
        separators=[".","\n\n","\n"," "]
    )

    text_chunks=splitter.split_text(text)

    return text_chunks


def save_into_db(text_chunks,db_path='./vectorstore_faiss'):

    embeddings=OpenAIEmbeddings()

    if os.path.exists(db_path):

        db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
        print("Existing FAISS index found — adding new chunks...")
        db.add_texts(text_chunks)
    
    else:

        db=FAISS.from_texts(texts=text_chunks,embedding=embeddings)

    db.save_local(db_path)
    print("Data Stored In DB...")



def load_db(db_path='./vectorstore_faiss'):
    embeddings=OpenAIEmbeddings()
    db=FAISS.load_local(db_path,embeddings,allow_dangerous_deserialization=True)

    return db


def query_ans_retrival(query,db,k=5):

    docs=db.similarity_search(query,k=k)

    return [doc.page_content for doc in docs]

def answer_generator(query,db):

    llm=OpenAI(temperature=0.8)

    context=query_ans_retrival(query,db)

    
    prompt = """You are a helpful assistant.
        Use the following context to answer the question clearly.
        Context:
        {context}

        Question:
        {query}

        Answer:
        """.format(context=context, query=query)
    
    answer=llm.invoke(prompt)

    return answer
    
