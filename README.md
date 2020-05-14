# Providence Data Pipeline

This repo is one of several projects related to [CCLYC](https://github.com/sinelki/cclyc.git). It contains scripts used to bootstrap the dataset for [Comparison Class Learning in Young Children](http://library.mit.edu/F/PQKXE2YAGSC2MEUE92G1NESLJHRCHALE3ABDPS867K4HJBR97F-00503?func=file&amp=&amp=&amp=&amp=&amp=&amp=&file%5Fname=find-b&local%5Fbase=THESES2).

## Project Folders <a href=”folders”></a>
`examples/`: Contains example python scripts for extracting information from the database

`sql_tables/`: Contains`.sql` dumps of each table used in the database

`data/`: Contains csv files of the annotations

### Data Files <a href=”data”></a>
`data/annotations.csv` is a csv file that contains the compiled, cleaned (duplicates removed)
annotation data from myself and the other annotators of the dataset. Only the “AS” annotator
has annotations marked in certain columns (demonstrative, indefinite pronoun, pronoun, subject
noun prenominal, subject noun predicate, predicate noun prenominal, predicate noun predicate,
stand alone prenominal, adjective alone frame) because those utterances were reannotated for
those specific properties. The Methods section of _Comparison Class Learning in Young Children_
describes how to interpret each property. The columns speaker code, speaker role, speaker name,
target child name, target child age, and target child sex all come directly from the CHILDES
database.

`data/syntactic_frame_spacy_agreement.csv` has the agreement information of spacy annotations versus my annotations of 100 randomly selected utterances. See the Methods section of _Comparison Class Learning in Young Children_ for more information.

## Setup <a href=”setup”></a>

### Prerequisites <a href=”prerequisites”></a>

Download and install copies of the following software.

- [Python3](https://www.python.org/downloads/)
- [MySQL Server](https://dev.mysql.com/downloads/mysql/5.5.html)
- [youtube-dl](https://github.com/ytdl-org/youtube-dl)
- [ffmpeg](https://www.ffmpeg.org/download.html)

### Database Setup <a href=”database-setup”></a>
Follow these steps to set up the database and recreate the videos table. The videos table is not included in this repo because the video segments need ~4Gb of storage. Following steps 1-3 will recreate the videos segments and place them into the table.

1. Import all `*.sql` files into providence_comparison_class2 database (this database should be created when the first .sql file is imported). I recommend using MySQL Workbench to import the files as the GUI will make it easy to navigate the tables and perform test queries.
1. Run `download_providence_videos.py` to download the videos corresponding to the [Providence corpus](https://phonbank.talkbank.org/access/Eng-NA/Providence.html)
   ```bash
   download_providence_videos.py --output-location [OUTPUT_PATH]
   ```
1. Run `cut_videos.py`. This will cut the downloaded videos into segments matching the timestamps found in the database and upload these segments to the videos table. 
   ```bash
   cut_videos.py --videos-location [VIDEOS_PATH]
   ```

#### Data Format<a href=”data-format”></a>
The videos, annotations, and annotator metadata are stored as base64 encoded strings and must be decoded to be human readable. You can view how to do this by viewing the [example scripts](./examples).

> *Note*: annotator metadata is stored in the same format as the annotations, therefore the example code can be easily adapted for either.


## Citations <a href=”citations”></a>
Providence corpus:

Demuth, Katherine, Jennifer Culbertson, & Jennifer Alter. 2006. Word-minimality, Epenthesis, and Coda Licensing in the Acquisition of English. Language & Speech, 49, 137-174.

CHILDES database:

MacWhinney, B. (2000). _The CHILDES Project: Tools for analyzing talk. Third Edition._ Mahwah, NJ: Lawrence Erlbaum Associates.
