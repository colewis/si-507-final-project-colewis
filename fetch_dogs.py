import sqlite3
import csv
import json
import requests
import webbrowser
import random
from bs4 import BeautifulSoup
# import plotly.plotly as py
# import pandas as pd

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

DBNAME = 'good_boys.db'
baseurl = 'http://www.akc.org/dog-breeds/'

crawl_list = []
for x in range(1,24):
    crawlurl = 'page/' + str(x) + '/'
    crawl_list.append(baseurl + crawlurl)

breed_list = []
for x in crawl_list:
    page_text = make_request_using_cache(x)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    content_div = page_soup.find_all(class_="breed-type-card__title mt0 mb0 f-25 py3 px3")
    for item in content_div:
        breed_text = item.string
        if breed_text not in breed_list:
            breed_list.append(breed_text)

breed_urls = []
for x in breed_list:
    if ' ' in x:
        x = x.replace(' ', '-')
        breedname = baseurl + x + '/'
        breed_urls.append(breedname)
    else:
        breedname = baseurl + x + '/'
        breed_urls.append(breedname)

groups = ['Sporting Group', 'Working Group', 'Toy Group', 'Herding Group', 'Foundation Stock Service', 'Hound Group', 'Terrier Group', 'Non-Sporting Group', 'Miscellaneous Class']
group_list = []
for x in breed_urls:
    page_text = make_request_using_cache(x)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    content_div = page_soup.find_all(class_="attribute-list__description attribute-list__text ")
    for item in content_div:
        a_tag = item.find('a')
        if a_tag != None:
            #if a_tag in groups:
            group_list.append(a_tag.string)

### fixing random mistakes in the list
group_list.insert(13, 'Foundation Stock Service')
group_list.insert(76, 'Hound Group')
group_list.insert(118, 'Hound Group')
group_list.insert(155, 'Non-Sporting Group')
group_list.insert(185, 'Hound Group')
#print(len(breed_list)) 265
print(len(group_list)) #264 - looking for 1 incorrect one


#categories_list = ['Group', 'Activity Level', 'Barking Level', 'Characteristics', 'Coat Type', 'Shedding', 'Size', 'Trainability']
dog_dict = {}
# for x in breed_list:
#     dog_dict[x] = {}
#     for y in range(len(group_list)):
#         dog_dict[x]['Group'] = group_list[y]
for y in range(len(group_list)):
    dog_dict[(breed_list[y])] = {}
    dog_dict[(breed_list[y])]['Group'] = group_list[y]

print(dog_dict)

# print(len(group_list)) 258
# print(len(breed_list)) 264


# with open('breed_list.csv', 'w', newline='') as csv_file:
#     get_dog = csv.writer(csv_file, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
#     for puppy in breed_list:
#         get_dog.writerow([puppy])
# csv_file.close()

#creating a dictionary for each breed where the breed name is the key to another dictionary
#and within that dictionary the category names are the keys and the values are the answers to
#that particular dog breed

#what I will ultimately want to do is figure out how I can either write a dictionary to a csv
#file and subsequently establish a database from there, or how to write dictionary elements into
#a database. I will also need to code to scrape the webpages for individual dogs to find out
#the value for each category in dog_dict[key/breedname]
#something along the lines of "if <whatever tag text> == dog_dict[key/breedname], then
#dog_dict[k/b][0] = <whatever group>, dog_dict[k/b][1] = <whatever activity level>, etc"

# def init_db(db_name): #creates/initializes the database
#
#     try:
#         conn = sqlite3.connect(DBNAME)
#         cur = conn.cursor()
#     except Error as e:
#         print(e)
#
#     statement = '''
#         DROP TABLE IF EXISTS 'Breeds';
#     '''
#     cur.execute(statement)
#     conn.commit()
#     make_table = '''
#         CREATE TABLE IF NOT EXISTS 'Breeds' (
#         'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
#         'Breed Name' TEXT
#         );
#     '''
#     cur.execute(make_table)
#     conn.commit()
#
#     statement1 = '''
#         DROP TABLE IF EXISTS 'Groups';
#     '''
#     cur.execute(statement1)
#     conn.commit()
#     make_table1 = '''
#         CREATE TABLE IF NOT EXISTS 'Groups' (
#             'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
#             'Sporting Group' TEXT,
#             'Working Group' TEXT,
#             'Toy Group' TEXT,
#             'Herding Group' TEXT,
#             'Foundation Stock Service' TEXT,
#             'Hound Group' TEXT,
#             'Terrier Group' TEXT,
#             'Non-Sporting Group' TEXT,
#             'Miscellaneous Class' TEXT
#             --FOREIGN KEY('BroadBeanOriginId') REFERENCES 'Countries'('Id'),
#             --FOREIGN KEY('CompanyLocationId') REFERENCES 'Countries'('Id')
#         );
#     '''
#     cur.execute(make_table1)
#     conn.commit()
#
#
#     statement2 = '''
#         DROP TABLE IF EXISTS 'Activity_Level';
#     '''
#     cur.execute(statement2)
#     conn.commit()
#     make_table2 = '''
#         CREATE TABLE IF NOT EXISTS 'Activity_Level' (
#             'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
#             'Couch Potato' TEXT,
#             'Regular Exercise' TEXT,
#             'Calm' TEXT,
#             'Needs Lots Of Activity' TEXT,
#             'Energetic' TEXT
#         );
#     '''
#     cur.execute(make_table2)
#     conn.commit()
#
#     statement3 = '''
#         DROP TABLE IF EXISTS 'Barking_Level';
#     '''
#     cur.execute(statement3)
#     conn.commit()
#     make_table3 = '''
#         CREATE TABLE IF NOT EXISTS 'Barking_Level' (
#             'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
#             'When Necessary' TEXT,
#             'Medium' TEXT,
#             'Likes To Be Vocal' TEXT,
#             'Infrequent' TEXT,
#             'Frequent' TEXT
#         );
#     '''
#     cur.execute(make_table3)
#     conn.commit()
#
#     statement4 = '''
#         DROP TABLE IF EXISTS 'Characteristics';
#     '''
#     cur.execute(statement4)
#     conn.commit()
#     make_table4 = '''
#         CREATE TABLE IF NOT EXISTS 'Characteristics' (
#             'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
#             'Smallest Dog Breeds' TEXT,
#             'Largest Dog Breeds' TEXT,
#             'Hypoallergenic Dogs' TEXT,
#             'Best Guard Dogs' TEXT,
#             'Best Dogs For Apartment Dwellers' TEXT,
#             'Medium Dog Breeds' TEXT,
#             'Smartest Dogs' TEXT,
#             'Best Family Dogs' TEXT,
#             'Best Dog Breeds For Children' TEXT,
#             'Hairless Dog Breeds' TEXT
#         );
#     '''
#     cur.execute(make_table4)
#     conn.commit()
#
#     statement5 = '''
#         DROP TABLE IF EXISTS 'Coat_Type';
#     '''
#     cur.execute(statement5)
#     conn.commit()
#     make_table5 = '''
#         CREATE TABLE IF NOT EXISTS 'Coat_Type' (
#             'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
#             'Hairless' TEXT,
#             'Medium' TEXT,
#             'Smooth' TEXT,
#             'Short' TEXT,
#             'Long' TEXT,
#             'Wire' TEXT
#         );
#     '''
#     cur.execute(make_table5)
#     conn.commit()
#
#     statement6 = '''
#         DROP TABLE IF EXISTS 'Shedding';
#     '''
#     cur.execute(statement6)
#     conn.commit()
#     make_table6 = '''
#         CREATE TABLE IF NOT EXISTS 'Shedding' (
#             'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
#             'Infrequent' TEXT,
#             'Frequent' TEXT,
#             'Regularly' TEXT,
#             'Seasonal' TEXT,
#             'Occasional' TEXT
#         );
#     '''
#     cur.execute(make_table6)
#     conn.commit()
#
#     statement7 = '''
#         DROP TABLE IF EXISTS 'Size';
#     '''
#     cur.execute(statement7)
#     conn.commit()
#     make_table7 = '''
#         CREATE TABLE IF NOT EXISTS 'Size' (
#             'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
#             'XSmall' TEXT,
#             'Small' TEXT,
#             'Medium' TEXT,
#             'Large' TEXT,
#             'XLarge' TEXT
#         );
#     '''
#     cur.execute(make_table7)
#     conn.commit()
#
#     statement8 = '''
#         DROP TABLE IF EXISTS 'Trainability';
#     '''
#     cur.execute(statement8)
#     conn.commit()
#     make_table8 = '''
#         CREATE TABLE IF NOT EXISTS 'Trainability' (
#             'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
#             'May Be Stubborn' TEXT,
#             'Eager To Please' TEXT,
#             'Easy Training' TEXT,
#             'Agreeable' TEXT,
#             'Independent' TEXT
#         );
#     '''
#     cur.execute(make_table8)
#     conn.commit()
#
#     conn.close()
#
# init_db(DBNAME)
