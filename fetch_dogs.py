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
group_list.insert(210, 'Working Group')


#http://www.akc.org/dog-breeds/?activity_level%5B%5D=regular-exercise
#http://www.akc.org/dog-breeds/ page/ 2 /?activity_level%5B0%5D=regular-exercise

###ACTIVITY LEVEL###

reg_ex = []
for x in range(1,11):
    crawlurl = 'page/' + str(x) + '/?activity_level%5B0%5D=regular-exercise'
    reg_ex.append(baseurl + crawlurl)

reg_ex_dogs = []
for x in reg_ex:
    page_text = make_request_using_cache(x)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    content_div = page_soup.find_all(class_="breed-type-card__title mt0 mb0 f-25 py3 px3")
    for item in content_div:
        breed_text = item.string
        if breed_text not in reg_ex_dogs:
            reg_ex_dogs.append(breed_text)

calm = []
for x in range(1,3):
    crawlurl = 'page/' + str(x) + '/?activity_level%5B0%5D=calm'
    calm.append(baseurl + crawlurl)

calm_dogs = []
for x in calm:
    page_text = make_request_using_cache(x)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    content_div = page_soup.find_all(class_="breed-type-card__title mt0 mb0 f-25 py3 px3")
    for item in content_div:
        breed_text = item.string
        if breed_text not in calm_dogs:
            calm_dogs.append(breed_text)

needs_activity = []
for x in range(1,4):
    crawlurl = 'page/' + str(x) + '/?activity_level%5B0%5D=needs-lots-of-activity'
    needs_activity.append(baseurl + crawlurl)

active_pups = []
for x in needs_activity:
    page_text = make_request_using_cache(x)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    content_div = page_soup.find_all(class_="breed-type-card__title mt0 mb0 f-25 py3 px3")
    for item in content_div:
        breed_text = item.string
        if breed_text not in active_pups:
            active_pups.append(breed_text)

energetic = []
for x in range(1,8):
    crawlurl = 'page/' + str(x) + '/?activity_level%5B0%5D=energetic'
    energetic.append(baseurl + crawlurl)

energetic_dogs = []
for x in energetic:
    page_text = make_request_using_cache(x)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    content_div = page_soup.find_all(class_="breed-type-card__title mt0 mb0 f-25 py3 px3")
    for item in content_div:
        breed_text = item.string
        if breed_text not in energetic_dogs:
            energetic_dogs.append(breed_text)

###BARKING LEVEL###

###CHARACTERISTICS###

###COAT TYPE###

###SHEDDING###

###SIZE###

###TRAINABILITY###

### write code to go through each category by subcategory (new baseurl per category, such as
### http://www.akc.org/dog-breeds/?coat_type%5B%5D=short, http://www.akc.org/dog-breeds/ page/2/ ?coat_type%5B0%5D=short)
### and scrape those pages to make a list of what breeds fall in those categories
### then make a db to match up foreign keys (check project 3 code)

#categories_list = ['Group', 'Activity Level', 'Barking Level', 'Characteristics', 'Coat Type', 'Shedding', 'Size', 'Trainability']
dog_dict = {}
for y in range(len(breed_list)):
    dog_dict[(breed_list[y])] = {}
    dog_dict[(breed_list[y])]['Group'] = group_list[y]
    if breed_list[y] in reg_ex_dogs:
        dog_dict[(breed_list[y])]['Activity Level'] = 'Regular Exercise'
    elif breed_list[y] in calm_dogs:
        dog_dict[(breed_list[y])]['Activity Level'] = 'Calm'
    elif breed_list[y] in active_pups:
        dog_dict[(breed_list[y])]['Activity Level'] = 'Needs Lots Of Activity'
    elif breed_list[y] in energetic_dogs:
        dog_dict[(breed_list[y])]['Activity Level'] = 'Energetic'
    else:
        dog_dict[(breed_list[y])]['Activity Level'] = 'Not Specified'



# my_dict = {'App 1': 'App id1', 'App 2': 'App id2', 'App 3': 'App id3'}
# with open('test.csv', 'w') as f:
#     fieldnames = ['Application Name', 'Application ID']
#     writer = csv.DictWriter(f, fieldnames=fieldnames)
#     writer.writeheader()
#     data = [dict(zip(fieldnames, [k, v])) for k, v in my_dict.items()]
#     writer.writerows(data)
#
# my_dict = {'App 1': 'App id1', 'App 2': 'App id2', 'App 3': 'App id3'}
# with open('test.csv', 'w') as f:
#     f.write('Application Name, Application ID\n')
#     for key in my_dict.keys():
#         f.write("%s,%s\n"%(key,my_dict[key]))

###figure out how to write dictionary to csv

with open('master_list.csv', 'w') as f:
    f.write('Breed, Group, Activity_Level\n')
    for key in dog_dict.keys():
        f.write("%s,%s,%s\n"%(key, dog_dict[key]['Group'], dog_dict[key]['Activity Level']))

f.close()

MASTERCSV = 'master_list.csv'

# with open('breed_list.csv', 'w', newline='') as csv_file:
#     get_dog = csv.writer(csv_file, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
#     headers = ['Breed', 'Group']
#     get_dog.writeheader()
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

#also possible to scrape pages and append all breed names in that category to a list, then
#write a bunch of if/else statements assigning dictionary keys to values based on whether or
#not the dog is in a certain list

def init_db(db_name): #creates/initializes the database

    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    statement = '''
        DROP TABLE IF EXISTS 'Breeds';
    '''
    cur.execute(statement)
    conn.commit()
    make_table = '''
        CREATE TABLE IF NOT EXISTS 'Breeds' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Breed Name' TEXT,
        'Group' TEXT,
        'Activity Level' TEXT
        --add other columns
        );
    '''
    cur.execute(make_table)
    conn.commit()

    statement1 = '''
        DROP TABLE IF EXISTS 'Groups';
    '''
    cur.execute(statement1)
    conn.commit()
    make_table1 = '''
        CREATE TABLE IF NOT EXISTS 'Groups' (
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

def insert_dog_data():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    with open(MASTERCSV) as master_csv:
        csvReader = csv.reader(master_csv)
        for row in list(csvReader)[1:]:
            insertion = (row[0], row[1], row[2])
            statement = 'INSERT INTO "Breeds"'
            statement += 'VALUES (NULL, ?, ?, ?)'
            cur.execute(statement, insertion)
            conn.commit()

    conn.close()

insert_dog_data()

### what I realistically probably want to do is create a master list/db with all of the information by breed
### and then create dbs that draw from that list, so I could make a "Medium" dogs db, which would include just
### dogs with "Medium" as their size and then all of their respective characteristics from the master list
