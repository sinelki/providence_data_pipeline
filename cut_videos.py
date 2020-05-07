#!/usr/bin/env python3

#step 1: connect to mysql
#step 2: get utterance id, and find the corresponding video file
#        get start and end times, if both are null, print out video file and utterance id
#step 3: use ffmpeg to make cut
#step 4: upload cut video to mongodb blob storage
#        update table with unique id for that segment
#step 5: spot check
import mysql.connector
import os
import datetime
import base64
import hashlib
import sys

def get_unique_id(output):
    unique = hashlib.md5(output.encode('utf-8'))
    return unique.hexdigest()

def main(videos_location, *args, **kwargs):
    #getting all downloaded video filenames
    all_videos = os.listdir(videos_location)

    #setting up connection to mysql
    mydb = mysql.connector.connect(
            host= "localhost",
            user= "root",
            passwd= "password",
            database = "providence_comparison_class2"
            )

    #get all target utterances from target_to_context
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM target_to_context")
    all_targets = cursor.fetchall()
    #failed_cuts = open("failed_cuts.txt", "a")
    for target in all_targets:
        if target['video_id']:
            continue
        start = target["media_start"]
        end = target["media_end"]
        if not start and not end:
            #no_timestamps.write(str(target['target_utterance']))
            continue
        elif not start:
            start = end - 40
        elif not end:
            end = start + 40
        start = str(datetime.timedelta(seconds=start))
        end = str(datetime.timedelta(seconds=end))
        #Find transcript_id belong to this target utterance
        cursor = mydb.cursor()
        cursor.execute("SELECT transcript_id FROM all_utterances WHERE id=?", (target['target_utterance'],))
        transcript_id = cursor.fetchone()['transcript_id']
        #Find filename/video that corresponds to transcript
        cursor = sql_conn.cursor()
        cursor.execute("SELECT filename FROM transcript_to_filename WHERE transcript_id=?", (transcript_id,))
        fname = cursor.fetchone()['filename']
        #video we are looking for is part of fname
        video_name = videos_loc + fname[-9:-4]+".mp4"
        if video_name[3:] in all_videos:
            output_name = str(get_unique_id(video_name[3:]+start+end))+".mp4"
            #cut video segment
            try:
                os.system("ffmpeg -i " + video_name + " -ss " + start + " -to " + end + " " + output_name)

                cut_video = open(output_name, "rb").read()
                encoded = base64.b64encode(cut_video)

                cursor = mydb.cursor()
                cursor.execute("INSERT INTO videos (id, video) VALUES(%s, %s)", (output_name, encoded))
                mydb.commit()

                cursor = mydb.cursor()
                cursor.execute("UPDATE target_to_context SET video_id=%s WHERE target_utterance=%s", (output_name, target['target_utterance']))
                mydb.commit()

                os.system("rm " + output_name)
            except Exception as e:
                print("EXCEPTION " + target['target_utterance'], ":\n", e)

if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument("-l", "--videos-location", metavar="videos_loc", type=str, required=True,
            help="Location of full length Providence videos. You can download them using download_providence_videos.py")
    args = parser.parse_args()
    main(args.__dict__)
