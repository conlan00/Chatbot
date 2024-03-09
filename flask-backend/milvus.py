from pymilvus import connections, Collection, MilvusException, utility, CollectionSchema, FieldSchema, DataType
import pandas as pd

def connect():
    connections.connect(
        host = "192.168.56.1",
        port = "19530"
    )
    try:
        print("Connecting to database...")
        collections = utility.list_collections()
        print(f"List all collections:\n", collections)
    except MilvusException as e:
        print(e)
        
def create_collection(name: str):
    id = FieldSchema(
        name="id",
        dtype=DataType.INT64,
        is_primary=True,
        auto_id=True
    )
    text = FieldSchema(
        name="text",
        dtype=DataType.VARCHAR,
        max_length=1300
    )
    vector = FieldSchema(
        name="vector",
        dtype=DataType.FLOAT_VECTOR,
        dim=1536
    )
    schema = CollectionSchema(
        fields=[id, text, vector],
        description="Test collection",
        enable_dynamic_field=True
    )
    new_collection = Collection(
        name=name,
        schema=schema,
        using='default',
        shards_num=4
    )
    return new_collection
    
connect()
# text = "ala ma kota"
# vectors = service.get_embbedings(text)

# df = pd.DataFrame(columns=['vector', 'text'])

# new_row = {'vector':vectors, 'text': text}
# df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# print(df)

# try:
#     test = Collection("test")
#     mr = test.insert(df)
#     print(mr, "successfull")
# except MilvusException as e:
#     print(e)


