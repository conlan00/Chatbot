from openai import OpenAI
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import os
from langchain.text_splitter import CharacterTextSplitter
import pandas as pd
from milvus import create_collection
from pymilvus import MilvusException
import numpy as np

load_dotenv()  # take environment variables from .env.

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")
pdf_paths = ['M:\AI\hackhaton-project\kodeks_karny.pdf']

def askGPT(question: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": question}
        ],
        temperature=0.2
    )
    answer = completion.choices[0].message.content
    return answer

def handleFiles(files):
    texts = get_pdf_text(files)
    chunks = processPdfs(texts)
    get_vectore_store(chunks)

def get_pdf_text(pdf_docs):
    text_all = []
    for pdf in pdf_docs:
        text = ""
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
        text_all.append(text)
    return text_all

def processPdfs(raw_texts):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks_array = []
    for raw_text in raw_texts:
        chunks = text_splitter.split_text(raw_text)
        print(len(chunks))
        chunks_array.append(chunks)
    return chunks_array

def get_embbedings(text, **kwargs):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002",
        **kwargs
    )
    return response.data[0].embedding
    

def get_vectore_store(chunks_array):
    collection = create_collection('test')
    inserted_rows = 0
    for chunks in chunks_array:
        data = [{'text': chunk, 'vector': get_embbedings(chunk)} for chunk in chunks]
        df_efficient = pd.DataFrame(data)
        try:
            mr = collection.insert(df_efficient)
            inserted_rows += mr.insert_count
            print(mr)
        except MilvusException as e:
            print(e)
    print(inserted_rows)        
    nlist = 4 * int(np.round(np.sqrt(inserted_rows)))
    print(nlist)
    
    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {
            "nlist": nlist
        }
    }
    
    try:
        collection.create_index(
            field_name="vector",
            index_params=index_params,
            index_name="SimpleIndex"
        )
    except MilvusException as e:
        print(e)
    
    
            
            
    
