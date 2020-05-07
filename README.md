# Providence Data Pipeline

Scripts used to bootstrap the dataset for [Comparison Class Learning in Young Children](http://library.mit.edu/F/PQKXE2YAGSC2MEUE92G1NESLJHRCHALE3ABDPS867K4HJBR97F-00503?func=file&amp=&amp=&amp=&amp=&amp=&amp=&file%5Fname=find-b&local%5Fbase=THESES2).

## Prerequisites

Download and install copies of the following software.

- [Python3](https://www.python.org/downloads/)
- [MySQL Server](https://dev.mysql.com/downloads/mysql/5.5.html)
- [youtube-dl](https://github.com/ytdl-org/youtube-dl)
- [ffmpeg](https://www.ffmpeg.org/download.html)

## Setup

1. Import all `*.sql` files into providence_comparison_class2 database (this database should be created when the first .sql file is imported)
1. Run `download_providence_videos.py` to download the videos corresponding to the [Providence corpus](https://phonbank.talkbank.org/access/Eng-NA/Providence.html)
   ```bash
   download_providence_videos.py --output-location [OUTPUT_PATH]
   ```
1. Run `cut_videos.py`. This will cut the downloaded videos into segments matching the timestamps found in the database and upload these segments to the videos table. 
   ```bash
   cut_videos.py --videos-location [VIDEOS_PATH]
   ```

## Data Format
The videos, annotations, and annotator metadata are stored as base64 encoded strings and must be decoded to be human readable. You can view how to do this by viewing the [example scripts](./examples).

> *Note*: annotator metadata is stored in the same format as the annotations, therefore the example code can be easily adapted for either.

## Citation Information
Providence corpus:

Demuth, Katherine, Jennifer Culbertson, & Jennifer Alter. 2006. Word-minimality, Epenthesis, and Coda Licensing in the Acquisition of English. Language & Speech, 49, 137-174.

CHILDES database:

MacWhinney, B. (2000). The CHILDES Project: Tools for analyzing talk. Third Edition. Mahwah, NJ: Lawrence Erlbaum Associates.