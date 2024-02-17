import ast
import pandas as pd
from pymilvus import connections, Collection, MilvusException,utility
from altair import List
from openai import OpenAI
import tiktoken
#----------------------------------------------------------------------------+
client=OpenAI(api_key='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')#|
embedding_model = "text-embedding-ada-002"                                  #|
GPT_MODEL = "gpt-3.5-turbo"                                                 #|
#----------------------------------------------------------------------------+
#tworzenie wektorów za pomoca OpenAI 
def get_embedding(text: str, model="text-embedding-ada-002", **kwargs) -> List[float]:
    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model, **kwargs)
    return response.data[0].embedding

#Return the number of tokens in a string.
def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

#laczenie z baza 
def connect():
    connections.connect(host="192.168.0.213", port="19530")
    try:
        print("Connecting to database ..........")
        # List all collections
        collections = utility.list_collections()
        print(f"List all collections:\n", collections)
    except MilvusException as e:
        print(e)

#przykladowe zaladowanie daych --> lepiej w pliku szachy.ipynb
def insertData(fileName: str):
    # winter = 'winter_olympics_2022.csv'
    df1=pd.read_csv(fileName)
    df1['embedding'] = df1['embedding'].apply(ast.literal_eval)
    df1=df1[['embedding','text']]
    df1=df1.rename(columns={'embedding':'vector'})
    return df1

#przeszukiwanie bazy aby znalezc jak najbardziej odpowiedznie rekordy 
# za pomocą knn(odpowiada za to baza)
def similarities(prompt: str):
    try:
        #prompt='Which athletes won the gold medal in curling at the 2022 Winter Olympics?'
        vector_prompt=get_embedding(prompt)
        #print(vector_prompt)
        search_params = {
            "metric_type": "L2",
            "offset": 0,
            "ignore_growing": False,
            "params": {"nprobe": 10}
        }
        collection = Collection("documents")#nazwa kolekcji w bazie
        similarity_search_result = collection.search(
            data=[vector_prompt],
            anns_field="vector",#nazwa kolumny z wektorem
            param=search_params,
            limit=1,#ile ma zwrocic najbardziej podobnych
            output_fields=['text']
        )
        tab=[]
        # Display search results to the user
        for idx, hit in enumerate(similarity_search_result[0]):
            score = hit.distance
            description = hit.entity.text
            #print(f"{idx + 1}. {description} (distance: {score})")
            tab.append(description)
            return tab
            
    except MilvusException as e:
        print(e)


def query_message(query: str,model: str,token_budget: int) -> str:
    """Return a message for GPT, with relevant source texts pulled from a dataframe."""
    strings = similarities(query)
    introduction = 'Aby odpowiedzieć na kolejne pytanie, skorzystaj z poniższych artykułów na temat Mistrzostw szach szybkich. Jeśli odpowiedzi nie znajdziesz w artykułach, napisz: „Nie mogłem znaleźć odpowiedzi."'
    question = f"\n\nQuestion: {query}"
    message = introduction
    for string in strings:
        next_article = f'\n\nWikipedia article section:\n"""\n{string}\n"""'
        if (
            num_tokens(message + next_article + question, model=model)
            > token_budget
        ):
            break
        else:
            message += next_article
            print(message)
    return message + question

def ask(query: str,model: str = GPT_MODEL,token_budget: int = 4096 - 500,print_message: bool = False,) -> str:
    """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
    message = query_message(query,model=model, token_budget=token_budget)
    if print_message:
        print(message)
    messages = [
        {"role": "system", "content": "Odpowiadasz na pytania dotyczące mistrzostw w szachach szybkich"},
        {"role": "user", "content": message},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    response_message = response.choices[0].message.content
    return  response_message






def main():
    connect()
   # similarities()
    print(ask('Podaj informacje jakie posiadasz na o szachach szybkich z 2023 roku'))
   
    try:
        collection = Collection("documents")      # Get an existing collection.
        #mr = collection.insert(insertData('winter_olympics_2022.csv'))
    except MilvusException as e:
        print(e)
main()