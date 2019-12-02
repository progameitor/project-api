
from pymongo import MongoClient
import getpass
import json

#Get Password
password = getpass.getpass("Insert your AtlasMongoDB admin_1019 password: ")
connection = 'mongodb+srv://javigarzas27:{}@chats-zrrzp.mongodb.net/test?retryWrites=true&w=majority'.format(password)

#Connect to DB
client = MongoClient(connection)
def connectCollection(database, collection):
    db = client[database]
    coll = db[collection]
    return db, coll

db, users = connectCollection('chats','users')
db, chateo = connectCollection('chats','chateo')
db, messages = connectCollection('chats','messages')