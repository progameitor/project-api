
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

run(host="localhost", port=9090, debug=True)    