# project-api

GUIA DEL PROYECTO POR PASOS:
HACER COMO UN GUIÓN Y LUEGO REFERENCIARME A EL (YA EN NAVIDADES)

EL objetivo de este proyecto es crear una API desde 0 y analizar los sentimientos de las distintas conversaciones y por último 
que fuese capaz de recomendar a que usuario te asemejas mas y sería mas interesante mantener una conversación con él, debido
a tus distintos intereses

Para este proyecto he utilizado el mongo db atlas (mongo cloud),donde he subido mis bases de datos. Para ello he creado 
3 bases de datos distintas. La primera base de datos era toda la informacion general con todos los chats. La segunda es una
colección de todos los usuarios y por último la tercera es con todos los mensajes.

Una vez que teniamos nuestras bases de datos subidas al cloud el objetivo es que se actualizasen solas Por ejemplo al crear si 
se metía un usuario nuevo al chat te dijese si estaba creado o no etc. El resto de funciones las explicaré a continuación.

En el fichero de usernew.py es donde tengo todas las funcios:

-@get("/")

En esta función retornas toda la información que hay de la API disponible.

-@post("/user/create/")

En esta funcion creas los usuarios si el nombre no esta cogido previamente. Automaticamente se actualiza la colección de usuarios
para ir ampliando las bases de datos.

-@post("/chat/create")

Creas un nuevo chat y se te actualiza en la coleccion

-@get("/user/all_users")

En esta función obtienes todos los usuarios existentes.

-@get("/chats")

En esta función obtienes todos los chats existentes.

-@get("/chatswant=<x>,<y>")

Obtienes los chats que quieres observar dentro de tu base de datos.

-@post('/chat/<chat_id>/addmessage')

Añades mensajes en la API

- @get("/usertext")

Obtienes los usuarios con distintos nombres.

PASO 2

ANÁLISIS DEL SENTIMIENTO:

Para realizar este análisis he utilizado dos librerias de python Sentiment TextBlob y nltk

Primero con Sentiment TextBlob

-@get("/sentimenttext")

Sacas el sentimiento de todo el texto.

-@get("/sentimentchat=<x>")

Sacas el sentimiento de todo el chat a que te referiences.

-@get("/sentimentuser=<x>,<y>")

Sacas el sentimiento del chat al que te refieres y por usuario

Ahora análisis de sentimiento de nltk




