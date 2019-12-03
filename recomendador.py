import os
from pymongo import MongoClient
from dotenv import load_dotenv
import dns
from bson.json_util import dumps, loads
import re
from sklearn.metrics.pairwise import cosine_similarity as distance
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from bottle import get, run
import numpy as np
from connect import connectCollection
import json

load_dotenv()
url=os.getenv('URLMONGO')
client = MongoClient(url)

database, collection =connectCollection('chats','chateo')

def getting_every_sentence(lista):
    users_dict=dict()
    for dicc in lista:
        if dicc['userName'] not in users_dict:
            users_dict[dicc['userName']]=dicc['text']
        else:
            users_dict[dicc['userName']]+=' ' +dicc['text']
    for e in users_dict:
        users_dict[e]=re.sub(r"[^a-zA-Z0-9]+", ' ', users_dict[e])
    return users_dict


@get('/recommendation/user=<userName>')
def recommending_user(userName):
    database, collection =connectCollection('chats','chateo')
    query = list(collection.find({},{'userName':1,"text":1,'_id':0}))
    diccionario = getting_every_sentence(query)   
    recommendation_dict=dict()
    count_vectorizer=CountVectorizer(stop_words='english')
    sparse_matrix = count_vectorizer.fit_transform(diccionario.values())
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, columns=count_vectorizer.get_feature_names(), index=diccionario.keys())
    similarity_matrix = distance(df, df)
    sim_df = pd.DataFrame(similarity_matrix, columns=diccionario.keys(), index=diccionario.keys())
    np.fill_diagonal(sim_df.values, 0)
    final_matrix=sim_df.idxmax()
    recommended = list(sim_df.sort_values(by=userName, ascending = False).index[0:3])
    return json.dumps(recommended)

run(host="localhost", port=9090, debug=True)