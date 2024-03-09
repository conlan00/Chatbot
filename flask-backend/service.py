from openai import OpenAI,AzureOpenAI
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import os
from langchain.text_splitter import CharacterTextSplitter
import pandas as pd
from milvus import create_collection
from pymilvus import MilvusException, utility, Collection
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from itertools import chain

load_dotenv()  # take environment variables from .env.

client = OpenAI()

MODEL="gpt-4-turbo-preview"
client.api_key = os.getenv("OPENAI_API_KEY")
pdf_paths = ['M:\AI\hackhaton-project\kodeks_karny.pdf', 'M:\AI\hackhaton-project\konstytucja.pdf']
inserted_rows_count = 0
conversation_history = []

def get_similarieties(text: str, collection: str, returned_chunks: int):
    output_chunks = []
    print("Collection = " + collection)
    collection = Collection(name=collection)
    
    print("Zamieniam prompt na wektor")
    vector_prompt = get_embbedings(text)
    
    search_params = {
            "metric_type": "L2",
            "offset": 0,
            "ignore_growing": False,
            "params": {"nprobe": 80} #pwinno byc mniejsze niż nlist z indexu kolekcji
        }
    print(f"Loading collection to memory...")
    collection.load()
    print("Przeszukuje collection...")
    result = collection.search(
            data=[vector_prompt], #zmienna do ktorej bedzie przeszukanie
            anns_field="vector", #nazwa kolumny w kolekcji przechowujaca vektory
            param=search_params, #parametry wyszukiwania deklarowane wczesniej
            limit= returned_chunks, #ile ma zwrocic najbardziej podobnych
            output_fields=['text'] #kolumna ktora bedzie zwracana
        )
    collection.release()
    for ids, hit in enumerate(result[0]):
        output_chunks.append(hit.entity.text)
        #print(hit.entity.text)
    
    print("Zwracam wartosci")    
    return output_chunks

def drop_collection(name: str):
    global inserted_rows_count
    exist = utility.has_collection(name)
    
    if(exist):
        try: 
            utility.drop_collection(name)
            str = "Collection: " + name + " successfully dropped"
            inserted_rows_count = 0
            return str
        except MilvusException as e:
            print(e)
            return 1
    else:
        return "Collection doesnt exists"

#dokonczyc
def askGPT_with_knowladge_base(collection_name: str, question: str, returned_chunks: int):
    global conversation_history
    
    knowledge_chunks = get_similarieties(
        text=question,
        collection=collection_name,
        returned_chunks=returned_chunks
    )
    
    conversation_history_str = "\n".join(conversation_history)
    knowledge_chunks_str = "\n".join(knowledge_chunks)
    print("Skojarzone teksty: \n", knowledge_chunks_str)
    print("Historia konwersacji: \n", conversation_history_str)
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Jesteś pomocnym doradcą w sprawach prawniczych, na każde pytanie odpowiadaj profesjonalnym językiem i przy odpowiedzi sugeruj się dostarczonymi tekstami"},
            {"role": "system", "content": conversation_history_str},
            {"role": "assistant", "content": knowledge_chunks_str},
            {"role": "user", "content": question}
        ]
    )
    
    answer = response.choices[0].message.content
    conversation_history.append("Human: " + question)
    conversation_history.append("AI: " + answer)
    
    return answer
#for checkboxes aking GPT with similariteies====
def askGPT_with_knowladge_base_checkboxes(collection_name: str, question: str, returned_chunks: int):
    global conversation_history
    
    knowledge_chunks = get_similarieties(
        text=question,
        collection=collection_name,
        returned_chunks=returned_chunks
    )
    
    conversation_history_str = "\n".join(conversation_history)
    knowledge_chunks_str = "\n".join(knowledge_chunks)
    print("Skojarzone teksty: \n", knowledge_chunks_str)
    print("Historia konwersacji: \n", conversation_history_str)
    instruction ="Jesteś pomocnym doradcą, który szuka niespojności w umowach od klientów w sprawach prawniczych miedzy dużymi korporacjami, na każde pytanie odpowiadaj profesjonalnym językiem, będziesz odpowiadał TAK jeśli podany tekst przez uzytkownika nie zawiera niespójności z wymaganiami asystenta lub będziesz odpowiadał NIE jeśli podany tekst przez uzytkownika zawiera niespójności z wymaganiami asystenta i mówił dlaczego"
    # response = client.chat.completions.create(
    #     model=MODEL,
    #     messages=[
    #         {"role": "system", "content": "},
    #         # {"role": "system", "content": conversation_history_str},
    #         {"role": "assistant", "content": question},
    #         {"role": "user", "content": knowledge_chunks_str}
    #     ]
    # )
    response=GPT4(instruction,question,knowledge_chunks_str)
    
    answer = response
    conversation_history.append("Human: " + question)
    conversation_history.append("AI: " + answer)
    
    return answer


import urllib.request
import json
def GPT4(system: str,assistant: str, user:str):
    url = "https://lr-lm-sandbox-ams.azure-api.net/language-model-sandbox-legal-and-regulatory-v2-prod/api/chat-completions"

    # Przygotowanie nagłówków żądania
    hdr = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': '5cfae7646a2445008ca53f758b04326f',
    }

    # Dane, które chcesz wysłać
    data = {
        "user_id": "LH2024-team05@wolterskluwer.com",
        "chat_completions_config": {
            "model_name": "gpt-4",
            "model_version": "1106-Preview",
            "temperature": 0,
            "max_tokens": 4000,
            "top_p": 1,
            "frequency_penalty": 1,
            "presence_penalty": 1
        },
        "prompt": [
            {"role": "system","content": system},
            {"role": "assistant","content": assistant},
            {"role": "user","content": user}
        ]
    }

    # Konwersja słownika Pythona na ciąg JSON
    data = json.dumps(data).encode('utf-8')

    try:
        # Utworzenie żądania z danymi i nagłówkami
        req = urllib.request.Request(url, data=data, headers=hdr, method='POST')
        
        # Wysyłanie żądania i odbieranie odpowiedzi
        with urllib.request.urlopen(req) as response:
            response_body = response.read()
            decoded_response = response_body.decode('utf-8')
            response_dict = json.loads(decoded_response)
            
            # Wypisanie tylko części 'openai_response'
            z = response_dict.get("openai_response") # Użycie get() zapobiega błędom, jeśli klucz nie istnieje
            x=str(z)
        return x
    except Exception as e:
        print(e)
        return None



#######==============================
def askGPT(question: str) -> str:
    completion = client.chat.completions.create(
        model=MODEL,
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

#1. zamiana plików pdf na ciag znakow
def get_pdf_text(pdf_docs):
    text_all = []
    print("Writing pdfs to single string...")
    for pdf in pdf_docs:
        text = ""
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
        text_all.append(text)
    print("Reading pdfs done.")
    return text_all

#2. podzial ciagu znakow na chunki 
def processPdfs(raw_texts):
    #text splitter na podstawie nowej lini
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks_array = []
    print("Dividing text into chunks...")
    for raw_text in raw_texts:
        chunks = text_splitter.split_text(raw_text)
        print(len(chunks))
        chunks_array.append(chunks)
    return chunks_array

#3. funkcja ktora dostaja rownolegle watki i obsluguja swoje chunki
def process_chunk(chunk, collection):
    try:
        #stworzenie nowego dataFrame i osadzenie danego chunka na vektorach
        data = {'text': chunk, 'vector': get_embbedings(chunk)}
        df_efficient = pd.DataFrame([data])
        #zapis do bazy
        mr = collection.insert(df_efficient)
        return mr.insert_count
    except MilvusException as e:
        print(e)
        return 0

#4. osadzenie chunka na vektorze za pomoca modelu openAI
def get_embbedings(text, **kwargs):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002",
        **kwargs
    )
    return response.data[0].embedding


#funckja do "splaszczenia" wymiarow tablicy chunkow do 1D, zeby latwiej rozdzielic na watki
def flatten_chunks_array(chunks_array):
    return list(chain.from_iterable(chunks_array))

# funkcja powolujaca watki i rozdzielajaca zasoby do przetworzenia(flatten_chunks)    
def execute_concurently(flatten_chunks, num_workers, collection, insertion_lock):
    global inserted_rows_count
    #inserted_rows_count = 0

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_chunk = {executor.submit(process_chunk, chunk, collection): chunk for chunk in flatten_chunks}
    
        for future in as_completed(future_to_chunk):
            chunk = future_to_chunk[future]
            try:
                inserted_count = future.result()
                with insertion_lock:
                    inserted_rows_count += inserted_count
            except Exception as exc:
                print(f'Chunk {chunk} generated an exception: {exc}')
    print(f"Total inserted rows: {inserted_rows_count}")
    return inserted_rows_count

#wywolanie glownych funkcji programu    
def get_vectore_store(chunks_array):
    collection = create_collection('file')
    
    insertion_lock = Lock()
    
    flatten_chunks = flatten_chunks_array(chunks_array)
    inserted_rows = execute_concurently(
        flatten_chunks=flatten_chunks,
        num_workers=50,
        collection=collection,
        insertion_lock=insertion_lock
    )       
    nlist = 4 * int(np.round(np.sqrt(inserted_rows)))
    print(f"Value to nlist parameter of index: {nlist}")
    
    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {
            "nlist": nlist
        }
    }
    
    try:
        indexes = utility.list_indexes(
            collection_name='file'
        )
        if(len(indexes) > 0):
            print("Droping previous index...")
            collection.release()
            collection.drop_index()
        print(f"Creating index to collection: {collection.name}...")
        collection.create_index(
            field_name="vector",
            index_params=index_params,
            index_name="SimpleIndex"
        )
        
        print("Succesfull")
    except MilvusException as e:
        print(e)
    
    
            
            
    
