import ast
import pandas as pd
from pymilvus import connections, Collection, MilvusException,utility


def connect():
    connections.connect(host="192.168.0.213", port="19530")
    try:
        print("Connecting to database ..........")
        # List all collections
        collections = utility.list_collections()
        print(f"List all collections:\n", collections)
    except MilvusException as e:
        print(e)


def insertData(fileName: str):
    # winter = 'winter_olympics_2022.csv'
    df1=pd.read_csv(fileName)
    df1['embedding'] = df1['embedding'].apply(ast.literal_eval)
    df1=df1[['embedding','text']]
    df1=df1.rename(columns={'embedding':'vector'})
    return df1


def main():
    connect()
    try:
        collection = Collection("documents")      # Get an existing collection.
        #mr = collection.insert(insertData('winter_olympics_2022.csv'))
    except MilvusException as e:
        print(e)
main()