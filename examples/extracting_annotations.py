import base64
import json
import mysql.connector
import bson

mydb = mysql.connector.connect(
    host= "localhost",
    user= "root",
    passwd= "password",
    database = "providence_comparison_class2"
)

mycusor = mydb.cursor()
mycursor.execute("SELECT * FROM annotations")
all_annotations = mycursor.fetchall()

for anno in all_annotations:
    identifier, target, annotation, annotator = anno[0], anno[1], anno[2], anno[4]
    #if the annotator is null, it was done by Anna

    #to get the corresponding utterance
    mycursor = mydb.cursor()
    mycursor.execute("SELECT gloss, speaker_code, target_child_age FROM all_utterances where id=%s", (target,))
    utterance = mycursor.fetchone()
    utt, speaker, age = utterance[0], utterance[1], utterance[2]
    decoded = base64.b64decode(annotation)
    anno_dict = json.loads(json.dumps(bson.BSON.decode(decoded)))
    print(utterance, anno_dict)
    break
