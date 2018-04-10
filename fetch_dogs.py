import sqlite3
import csv
import json
import requests
import webbrowser
import random
from bs4 import BeautifulSoup
# import plotly.plotly as py
# import pandas as pd

DBNAME = 'good_boys.db'
baseurl = 'http://www.akc.org/dog-breeds/'

crawl_list = []
for x in range(1,23):
    crawlurl = 'page/' + str(x) + '/'
    crawl_list.append(baseurl + crawlurl)


CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

page_text = make_request_using_cache(baseurl)
page_soup = BeautifulSoup(page_text, 'html.parser')
content_div = page_soup.find_all(class_="breed-type-card__title mt0 mb0 f-25 py3 px3")
breed_list = []
for item in content_div:
    if item not in breed_list:
        breed_list.append(item)
    #print(item.string)


def init_db(db_name): #creates/initializes the database

    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)


    statement1 = '''
        DROP TABLE IF EXISTS 'Groups';
    '''
    cur.execute(statement1)
    conn.commit()
    make_table1 = '''
        CREATE TABLE IF NOT EXISTS 'Groups' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Sporting Group' TEXT,
            'Working Group' TEXT,
            'Toy Group' TEXT,
            'Herding Group' TEXT,
            'Foundation Stock Service' TEXT,
            'Hound Group' TEXT,
            'Terrier Group' TEXT,
            'Non-Sporting Group' TEXT,
            'Miscellaneous Class' TEXT
            --FOREIGN KEY('BroadBeanOriginId') REFERENCES 'Countries'('Id'),
            --FOREIGN KEY('CompanyLocationId') REFERENCES 'Countries'('Id')
        );
    '''
    cur.execute(make_table1)
    conn.commit()


    statement2 = '''
        DROP TABLE IF EXISTS 'Activity_Level';
    '''
    cur.execute(statement2)
    conn.commit()
    make_table2 = '''
        CREATE TABLE IF NOT EXISTS 'Activity_Level' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Couch Potato' TEXT,
            'Regular Exercise' TEXT,
            'Calm' TEXT,
            'Needs Lots Of Activity' TEXT,
            'Energetic' TEXT
        );
    '''
    cur.execute(make_table2)
    conn.commit()

    statement3 = '''
        DROP TABLE IF EXISTS 'Barking_Level';
    '''
    cur.execute(statement3)
    conn.commit()
    make_table3 = '''
        CREATE TABLE IF NOT EXISTS 'Barking_Level' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'When Necessary' TEXT,
            'Medium' TEXT,
            'Likes To Be Vocal' TEXT,
            'Infrequent' TEXT,
            'Frequent' TEXT
        );
    '''
    cur.execute(make_table3)
    conn.commit()

    statement4 = '''
        DROP TABLE IF EXISTS 'Characteristics';
    '''
    cur.execute(statement4)
    conn.commit()
    make_table4 = '''
        CREATE TABLE IF NOT EXISTS 'Characteristics' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Smallest Dog Breeds' TEXT,
            'Largest Dog Breeds' TEXT,
            'Hypoallergenic Dogs' TEXT,
            'Best Guard Dogs' TEXT,
            'Best Dogs For Apartment Dwellers' TEXT,
            'Medium Dog Breeds' TEXT,
            'Smartest Dogs' TEXT,
            'Best Family Dogs' TEXT,
            'Best Dog Breeds For Children' TEXT,
            'Hairless Dog Breeds' TEXT
        );
    '''
    cur.execute(make_table4)
    conn.commit()

    statement5 = '''
        DROP TABLE IF EXISTS 'Coat_Type';
    '''
    cur.execute(statement5)
    conn.commit()
    make_table5 = '''
        CREATE TABLE IF NOT EXISTS 'Coat_Type' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Hairless' TEXT,
            'Medium' TEXT,
            'Smooth' TEXT,
            'Short' TEXT,
            'Long' TEXT,
            'Wire' TEXT
        );
    '''
    cur.execute(make_table5)
    conn.commit()

    statement6 = '''
        DROP TABLE IF EXISTS 'Shedding';
    '''
    cur.execute(statement6)
    conn.commit()
    make_table6 = '''
        CREATE TABLE IF NOT EXISTS 'Shedding' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Infrequent' TEXT,
            'Frequent' TEXT,
            'Regularly' TEXT,
            'Seasonal' TEXT,
            'Occasional' TEXT
        );
    '''
    cur.execute(make_table6)
    conn.commit()

    statement7 = '''
        DROP TABLE IF EXISTS 'Size';
    '''
    cur.execute(statement7)
    conn.commit()
    make_table7 = '''
        CREATE TABLE IF NOT EXISTS 'Size' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'XSmall' TEXT,
            'Small' TEXT,
            'Medium' TEXT,
            'Large' TEXT,
            'XLarge' TEXT
        );
    '''
    cur.execute(make_table7)
    conn.commit()

    statement8 = '''
        DROP TABLE IF EXISTS 'Trainability';
    '''
    cur.execute(statement8)
    conn.commit()
    make_table8 = '''
        CREATE TABLE IF NOT EXISTS 'Trainability' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'May Be Stubborn' TEXT,
            'Eager To Please' TEXT,
            'Easy Training' TEXT,
            'Agreeable' TEXT,
            'Independent' TEXT
        );
    '''
    cur.execute(make_table8)
    conn.commit()

    conn.close()

init_db(DBNAME)
