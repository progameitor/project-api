import requests
from bottle import route, run, post, request,get
import bson
from bson.json_util import dumps
from connect import connectCollection
from textblob import TextBlob
import nltk # install nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
sid = SentimentIntensityAnalyzer()
nltk.download('vader_lexicon')

# retornas toda la informacion de la api
@get("/")
def index():
    return dumps(collection.find())
    #dumps(coll.find()) QUERY QUE ME FUNCIONO Y QUE DEVOLVIA TODAS LAS COSAS

# me crea usuarios y me dice si estan bien o no
@post("/user/create/")
def createUser():    
    database, collection = connectCollection('chats','users')
    name =str(request.forms.get("name"))    
    ids = collection.distinct("idUser")[-1] + 1
    user_new = {
        "idUser":ids,
        "userName": name
    }    
    takenNames = list(collection.aggregate([{'$project': {'userName': 1}}]))
    if user_new['userName'] in [e['userName'] for e in takenNames]: 
        return {"Error!" : "Username already in use"}   
    else:
        user_id = collection.insert_one(user_new)
        return {'NEW USER CREATED!'  'userName': name, 'UserId': int(user_new['idUser'])}


#consigo que me cree los chats pero no tienen ninguna relacion
@post("/chat/create")
def newChat():
    new_id= max(collection.distinct("idChat")) + 1
    name = str(request.forms.get("name", f"chat{new_id}"))
    new_chat=  {
        "id_Chat": new_id,
        "name": name
    }
    collection.insert_one(new_chat)
    print("Chat created")
    database, collection =connectCollection('chats','chateo')

# aqui obtienes todos los usuarios de la api
@get("/user/all_users")
def getUsers():
    database, collection = connectCollection('chats','users')
    return dumps(collection.find({}).distinct("userName"))
    

# Aqui obtengo todos los chats
@get("/chats")
def getChats():
    database, collection = connectCollection('chats','chateo')
    all_chats=dumps(collection.find().distinct("text")[0:])
    return all_chats

#Aqui obtienes los chats que quieres
@get("/chatswant=<x>,<y>")
def chatsWant(x,y):
    x=int(x)
    y=int(y)
    database, collection =connectCollection('chats','chateo')
    chats_want= []
    for a in range(x,y):
        chats_want.append(dumps(collection.find({"idChat":a},{"userName":1,"text":1})))
    return chats_want


@post('/chat/<chat_id>/addmessage')
def addMessage():
    def createMessage(chat_id):
    datauser, user = mc.connectCollection("apiproject","users")
    regis = list(user.aggregate([{'$project':{'userName':1, 'idUser':1,'_id':0}}]))
    name = str(request.forms.get("name"))
    message = str(request.forms.get("message"))
    new_id = coll.distinct("idMessage")[-1] + 1
    new_message = {
        "idUser":0,
        "userName": name,
        "idChat": int(chat_id),
        "idMessage":new_id,
        "text" : message
    }
   
    for i in range(len(regis)):
        if regis[i]['userName']==name:
            new_message['idUser'] = regis[i]['idUser']
            new_message['userName']=name
        else:
            new_message['idUser'] = user.distinct("idUser")[-1] +1
            new_message['userName'] = name
            
    coll.insert_one(new_message)

 

@get("/sentimenttext")
def sentimentalltext():
    database, collection =connectCollection('chats','chateo')
    sentiment = {}
    sentimental =dumps(collection.find({},{"text":1}))
    sentiment["analysis"]=TextBlob(sentimental).sentiment
    return sentiment



@get("/sentimentchat=<x>")
def sentimentchat(x):
    database, collection =connectCollection('chats','chateo')
    x = int(x)
    sentitext = {}
    sentitext_want = []
    for a in range(x):
        sentitext_want.append(dumps(collection.find({"idChat":x},{"text":1, "idChat":1})))
        sentitext["analyze"]=TextBlob(str(sentitext_want)).sentiment
    return sentitext

#HASTA AQUI TODOS FUNCIONAN 

@get("/sentimentuser=<x>,<y>")
def sentimentuser(x,y):
    database, collection =connectCollection('chats','chateo')
    x = int(x)
    y = int(y)
    sentitextuser= {}
    sentitext_user = []
    for a in range(x,y):
        sentitext_user.append(dumps(collection.find({"idChat":x, "idUser":y},{"text":1,"idChat":1, "userName":1})))
        sentitextuser["user"]=TextBlob(str(sentitext_user)).sentiment
    return sentitextuser

# analizar con nltk todos los textos
@get("/nltksentimenttext")
def nltktext():
    database, collection =connectCollection('chats','chateo')
    nltk_sentiment = {}
    nltk_sentimental =dumps(collection.find({},{"text":1}))
    nltk_sentiment["nltk_analysis"]=sid.polarity_scores(nltk_sentimental)
    return nltk_sentiment

# analizar por idChat para analizar cada chat por separado con nltk
@get("/nltksentimentchat=<x>")
def nltkchat(x):
    database, collection =connectCollection('chats','chateo')
    nltk_sentitext = {}
    nltk_sentitext_want = []
    x = int(x)
    for a in range(x):
        nltk_sentitext_want.append(dumps(collection.find({"idChat":x},{"text":1, "idChat":1})))
        nltk_sentitext["analyze"]=sid.polarity_scores(str(nltk_sentitext_want))
    return nltk_sentitext


# analizar por idChat para analizar cada chat por separado y usuario con nltk
@get("/nltksentimentchatuser=<x>,<y>")
def nltkuser(x,y):
    database, collection =connectCollection('chats','chateo')
    x = int(x)
    y = int(y)
    nltk_sentitextuser= {}
    nltk_sentitext_user = []
    for a in range(x,y):
        nltk_sentitext_user.append(dumps(collection.find({"idChat":x, "idUser":y},{"text":1,"idChat":1, "userName":1})))
        nltk_sentitextuser["user"]=sid.polarity_scores(str(nltk_sentitext_user))
    return nltk_sentitextuser


run(host="localhost", port=9090, debug=True)