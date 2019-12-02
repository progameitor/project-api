#!/usr/bin/python3

from pymongo import MongoClient
import getpass

from bottle import route, run, get, post, request
import random
from bson.json_util import dumps
import os
import json
import dns
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("URLMONGO")



#Connect to DB
client = MongoClient(url)
def connectCollection(database, collection):
    db = client[database]
    coll = db[collection]
    return db, coll

db, coll = connectCollection('chats','chateo')

'''with open('messages.json') as f:
    messages_json = json.load(f)
    coll.find(messages_json)'''

@get("/")
def index():
    return dumps(coll.find())
    #dumps(coll.find())
run(host="0.0.0.0", port=9090)