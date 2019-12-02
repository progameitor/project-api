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
