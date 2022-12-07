from pymongo import MongoClient

conn_str = "mongodb+srv://doguser:JgYuxCq8lsRO9XW9@cluster0.5vpjiks.mongodb.net/test"
# set a 5-second connection timeout
client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")

db = client.testdb

db.testcollection.insert_one({
    "name": "Грэм Чепмен",
    "chat_id": 12345,
    "messages": [
        {"id": 1, "text": "Стой! Как тебя зовут?"},
        {"id": 2, "text": "Перед тобой Артур, король бриттов."}
    ]
})