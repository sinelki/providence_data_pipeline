import base64
import mysql.connector
import bson

mydb = mysql.connector.connect(
        host= "localhost",
        user= "root",
        passwd= "password",
        database = "providence_comparison_class2"
        )
ids = [2137059,2300863,2281241,2024666,2033492,2048041,1901163]
for target in ids:
    mycursor = mydb.cursor()
    mycursor.execute("SELECT video_id FROM target_to_context WHERE target_utterance=%s",(target,))
    video_id = mycursor.fetchone()[0]
    mycursor = mydb.cursor()
    mycursor.execute("SELECT video FROM videos WHERE id=%s",(video_id,))
    video_binary = mycursor.fetchone()[0]
    decoded_video = base64.b64decode(video_binary)
    with open("example_videos/"+video_id, "wb") as f:
        f.write(decoded_video)
