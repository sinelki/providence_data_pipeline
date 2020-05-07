#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import os

def main(output_location, *args, **kwargs):
    children = ["Alex", "Ethan", "Lily", "Naima", "Violet", "William"]

    for child in children:
        html = requests.get("https://media.talkbank.org/phonbank/Eng-NA/Providence/"+child+"/")
        soup = BeautifulSoup(html.content, "html.parser")
        i = 1
        for link in soup.find_all("a"):
            if ".mp4" not in link.get("href"):
                continue
            video_link = "'https://media.talkbank.org/phonbank/Eng-NA/Providence/"+child+"/"+link.get("href")+"'"
            if i < 10:
                new_name = "'"+child.lower()[:3]+"0"+str(i)+".mp4'"
            else:
                new_name = "'"+child.lower()[:3]+str(i)+".mp4'"
            os.system("youtube-dl "+video_link+" -o " + os.path.join(output_location, new_name))
            i += 1

if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument("-o", "--output-location", type=str, required=True,
            help="Location to dump videos from Providence Corpus")
    args = parser.parse_args()
    main(args.__dict__)
