# Data
This folder contains the data gathering scripts I used ... except the web scraper. My client requested that the scraping access to their database remain classified.

The databases are to remain classified as well so will not be posted to github.

## Files

### dbs.py 
Accesses the 40 SQL databases stored on my local computer.

### make_db.py
Accesses the scraped MongoDB stored on my system and transforms it to a better formatted MongoDB. It's output can be directly pulled into a df.

### pull_from_mongo.py
Access the MongoDB stored on my system and transforms it to a pandas DataFrame
