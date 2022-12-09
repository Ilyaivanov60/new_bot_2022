from datetime import datetime
from random import choice
from emoji import emojize
from pymongo import MongoClient
import settings

conn_str = settings.MONGO_LINK
# set a 5-second connection timeout
client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")

db = client[settings.MONGO_DB]


def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({'user_id': effective_user.id})
    if not user:
        user = {
            'user_id': effective_user.id,
            'first_name': effective_user.first_name,
            'last_name': effective_user.last_name,
            'username': effective_user.username,
            'chat_id': chat_id,
            "emoji": emojize(choice(settings.USER_EMOJI))
        }
        db.users.insert_one(user)
    return user


def save_anketa(db, user_id, anketa_data):
    user = db.users.find_one({'user_id': user_id})
    anketa_data['created'] = datetime.now()
    if 'anketa' not in user:
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'anketa': [anketa_data]}}
            )
    else:
        db.users.update_one(
            {'_id': user['_id']},
            {'$push': {'anketa': anketa_data}}
        )
