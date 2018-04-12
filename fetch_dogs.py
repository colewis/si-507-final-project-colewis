import sqlite3
import csv
import json
import requests
import webbrowser
import random
from bs4 import BeautifulSoup
# import plotly.plotly as py
# import pandas as pd

CACHE_FNAME = 'cache_money.json'
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

def scrape_breed_names(list1, list2):
    for x in list1:
        page_text = make_request_using_cache(x)
        page_soup = BeautifulSoup(page_text, 'html.parser')
        content_div = page_soup.find_all(class_="breed-type-card__title mt0 mb0 f-25 py3 px3")
        for item in content_div:
            breed_text = item.string
            if breed_text not in list2:
                list2.append(breed_text)
    return list2

breed_list = []
k = scrape_breed_names(crawl_list, breed_list)

breed_urls = []
for x in breed_list:
    if ' ' in x:
        x = x.replace(' ', '-')
        breedname = baseurl + x + '/'
        breed_urls.append(breedname)
    else:
        breedname = baseurl + x + '/'
        breed_urls.append(breedname)

group_list = []
for x in breed_urls:
    page_text = make_request_using_cache(x)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    content_div = page_soup.find_all(class_="attribute-list__description attribute-list__text ")
    for item in content_div:
        a_tag = item.find('a')
        if a_tag != None:
            group_list.append(a_tag.string)

### fixing random mistakes in the list
group_list.insert(13, 'Foundation Stock Service')
group_list.insert(76, 'Hound Group')
group_list.insert(118, 'Hound Group')
group_list.insert(155, 'Non-Sporting Group')
group_list.insert(185, 'Hound Group')
group_list.insert(210, 'Working Group')

###URL PIECES###
page = 'page/'
gibberish = '%5B0%5D='

def crawl_urls(x,y,category,string,list):
    if x != y:
        for i in range(x,y):
            crawlurl = page + str(i) + category + gibberish + string
            list.append(baseurl + crawlurl)
        return list
    else:
        crawlurl = category[1:] + gibberish + string
        list.append(baseurl + crawlurl)
        return list

activity_level = '/?activity_level'
barking_level = '/?barking_level'
coat_type = '/?coat_type'
shedding = '/?shedding'
size = '/?size'
trainability = '/?trainability'

###ACTIVITY LEVEL###

reg_ex = []
calm = []
needs_activity = []
energetic = []

crawl_urls(1,11,activity_level,'regular-exercise',reg_ex)
crawl_urls(1,3,activity_level,'calm',calm)
crawl_urls(1,4,activity_level,'needs-lots-of-activity',needs_activity)
crawl_urls(1,8,activity_level,'energetic',energetic)

reg_ex_dogs = []
calm_dogs = []
active_pups = []
energetic_dogs = []

scrape_breed_names(reg_ex, reg_ex_dogs)
scrape_breed_names(calm, calm_dogs)
scrape_breed_names(needs_activity, active_pups)
scrape_breed_names(energetic, energetic_dogs)

###BARKING LEVEL###

necessity = []
medium = []
talkative = []
in_frequent = []
out_frequent = []

crawl_urls(1,4,barking_level,'when_necessary',necessity)
crawl_urls(1,12,barking_level,'medium',medium)
crawl_urls(1,4,barking_level,'likes-to-be-vocal',talkative)
crawl_urls(1,3,barking_level,'infrequent',in_frequent)
crawl_urls(1,3,barking_level,'frequent',out_frequent)

when_necessary = []
medium_bark = []
vocal = []
infrequent = []
frequent =[]

scrape_breed_names(necessity, when_necessary)
scrape_breed_names(medium, medium_bark)
scrape_breed_names(talkative, vocal)
scrape_breed_names(in_frequent, infrequent)
scrape_breed_names(out_frequent, frequent)

###COAT TYPE###

hairless = []
medium_hair = []
smooth = []
short_hair = []
long_hair = []
wire = []

crawl_urls(1,1,coat_type,'hairless',hairless)
crawl_urls(1,10,coat_type,'medium',medium_hair)
crawl_urls(1,1,coat_type,'smooth',smooth)
crawl_urls(1,10,coat_type,'short',short_hair)
crawl_urls(1,5,coat_type,'long',long_hair)
crawl_urls(1,1,coat_type,'wire',wire)

no_hair = []
med_hair = []
smooth_hair = []
short_hair_dogs = []
long_hair_dogs = []
wire_hair = []

scrape_breed_names(hairless, no_hair)
scrape_breed_names(medium_hair, med_hair)
scrape_breed_names(smooth, smooth_hair)
scrape_breed_names(short_hair, short_hair_dogs)
scrape_breed_names(long_hair, long_hair_dogs)
scrape_breed_names(wire, wire_hair)

###SHEDDING###

infrq_shed = []
frq_shed = []
reg_shed = []
seas_shed = []
occ_shed = []

crawl_urls(1,4,shedding,'infrequent',infrq_shed)
crawl_urls(1,1,shedding,'frequent',frq_shed)
crawl_urls(1,4,shedding,'regularly',reg_shed)
crawl_urls(1,11,shedding,'seasonal',seas_shed)
crawl_urls(1,6,shedding,'occasional',occ_shed)

infrq_shedder = []
frq_shedder = []
reg_shedder = []
seas_shedder = []
occ_shedder = []

scrape_breed_names(infrq_shed, infrq_shedder)
scrape_breed_names(frq_shed, frq_shedder)
scrape_breed_names(reg_shed, reg_shedder)
scrape_breed_names(seas_shed, seas_shedder)
scrape_breed_names(occ_shed, occ_shedder)

###SIZE###

sz_xsmall = []
sz_small = []
sz_medium = []
sz_large = []
sz_xlarge = []

crawl_urls(1,3,size,'xsmall',sz_xsmall)
crawl_urls(1,6,size,'small',sz_small)
crawl_urls(1,10,size,'medium',sz_medium)
crawl_urls(1,6,size,'large',sz_large)
crawl_urls(1,3,size,'xlarge',sz_xlarge)

xs_dogs = []
small_dogs = []
med_dogs = []
large_dogs = []
xl_dogs = []

scrape_breed_names(sz_xsmall, xs_dogs)
scrape_breed_names(sz_small, small_dogs)
scrape_breed_names(sz_medium, med_dogs)
scrape_breed_names(sz_large, large_dogs)
scrape_breed_names(sz_xlarge, xl_dogs)

###TRAINABILITY###

may_be_stubborn = []
eager_to_please = []
easy_training = []
agreeable = []
independent = []

crawl_urls(1,3,trainability,'may-be-stubborn',may_be_stubborn)
crawl_urls(1,6,trainability,'eager-to-please',eager_to_please)
crawl_urls(1,5,trainability,'easy-training',easy_training)
crawl_urls(1,8,trainability,'agreeable',agreeable)
crawl_urls(1,7,trainability,'independent',independent)

stubborn = []
eager = []
easy = []
agree = []
indp = []

scrape_breed_names(may_be_stubborn, stubborn)
scrape_breed_names(eager_to_please, eager)
scrape_breed_names(easy_training, easy)
scrape_breed_names(agreeable, agree)
scrape_breed_names(independent, indp)


### write code to go through each category by subcategory (new baseurl per category, such as
### http://www.akc.org/dog-breeds/?coat_type%5B%5D=short, http://www.akc.org/dog-breeds/ page/2/ ?coat_type%5B0%5D=short)
### and scrape those pages to make a list of what breeds fall in those categories
### then make a db to match up foreign keys (check project 3 code)



#'Coat Type', 'Shedding', 'Size', 'Trainability'
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
    if breed_list[y] in when_necessary:
        dog_dict[(breed_list[y])]['Barking Level'] = 'When Necessary'
    elif breed_list[y] in medium_bark:
        dog_dict[(breed_list[y])]['Barking Level'] = 'Medium'
    elif breed_list[y] in vocal:
        dog_dict[(breed_list[y])]['Barking Level'] = 'Likes To Be Vocal'
    elif breed_list[y] in infrequent:
        dog_dict[(breed_list[y])]['Barking Level'] = 'Infrequent'
    elif breed_list[y] in frequent:
        dog_dict[(breed_list[y])]['Barking Level'] = 'Frequent'
    else:
        dog_dict[(breed_list[y])]['Barking Level'] = 'Not Specified'
    if breed_list[y] in no_hair:
        dog_dict[(breed_list[y])]['Coat Type'] = 'Hairless'
    elif breed_list[y] in med_hair:
        dog_dict[(breed_list[y])]['Coat Type'] = 'Medium'
    elif breed_list[y] in smooth_hair:
        dog_dict[(breed_list[y])]['Coat Type'] = 'Smooth'
    elif breed_list[y] in short_hair_dogs:
        dog_dict[(breed_list[y])]['Coat Type'] = 'Short'
    elif breed_list[y] in long_hair_dogs:
        dog_dict[(breed_list[y])]['Coat Type'] = 'Long'
    elif breed_list[y] in wire_hair:
        dog_dict[(breed_list[y])]['Coat Type'] = 'Wire'
    else:
        dog_dict[(breed_list[y])]['Coat Type'] = 'Not Specified'
    if breed_list[y] in infrq_shedder:
        dog_dict[(breed_list[y])]['Shedding'] = 'Infrequent'
    elif breed_list[y] in frq_shedder:
        dog_dict[(breed_list[y])]['Shedding'] = 'Frequent'
    elif breed_list[y] in reg_shedder:
        dog_dict[(breed_list[y])]['Shedding'] = 'Regularly'
    elif breed_list[y] in seas_shedder:
        dog_dict[(breed_list[y])]['Shedding'] = 'Seasonal'
    elif breed_list[y] in occ_shedder:
        dog_dict[(breed_list[y])]['Shedding'] = 'Occasional'
    else:
        dog_dict[(breed_list[y])]['Shedding'] = 'Not Specified'
    if breed_list[y] in xs_dogs:
        dog_dict[(breed_list[y])]['Size'] = 'XSmall'
    elif breed_list[y] in small_dogs:
        dog_dict[(breed_list[y])]['Size'] = 'Small'
    elif breed_list[y] in med_dogs:
        dog_dict[(breed_list[y])]['Size'] = 'Medium'
    elif breed_list[y] in large_dogs:
        dog_dict[(breed_list[y])]['Size'] = 'Large'
    elif breed_list[y] in xl_dogs:
        dog_dict[(breed_list[y])]['Size'] = 'XLarge'
    else:
        dog_dict[(breed_list[y])]['Size'] = 'Not Specified'
    if breed_list[y] in stubborn:
        dog_dict[(breed_list[y])]['Trainability'] = 'May Be Stubborn'
    elif breed_list[y] in eager:
        dog_dict[(breed_list[y])]['Trainability'] = 'Eager To Please'
    elif breed_list[y] in easy:
        dog_dict[(breed_list[y])]['Trainability'] = 'Easy Training'
    elif breed_list[y] in agree:
        dog_dict[(breed_list[y])]['Trainability'] = 'Agreeable'
    elif breed_list[y] in indp:
        dog_dict[(breed_list[y])]['Trainability'] = 'Independent'
    else:
        dog_dict[(breed_list[y])]['Trainability'] = 'Not Specified'



###CSV###

with open('master_list.csv', 'w') as f:
    f.write('Breed, Group, Activity_Level, Barking_Level, Coat_Type, Shedding, Size, Trainability\n') #, Shedding
    for key in dog_dict.keys():
        f.write("%s,%s,%s,%s,%s,%s,%s,%s\n"%(key, dog_dict[key]['Group'], dog_dict[key]['Activity Level'], dog_dict[key]['Barking Level'], dog_dict[key]['Coat Type'], dog_dict[key]['Shedding'], dog_dict[key]['Size'], dog_dict[key]['Trainability']))

f.close()

MASTERCSV = 'master_list.csv'


###DATABASE###

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
        'Activity Level' TEXT,
        'Barking Level' TEXT,
        'Coat Type' TEXT,
        'Shedding' TEXT,
        'Size' TEXT,
        'Trainability' TEXT
        --FOREIGN KEY('BroadBeanOriginId') REFERENCES 'Countries'('Id'),
        --FOREIGN KEY('CompanyLocationId') REFERENCES 'Countries'('Id')
        );
    '''
    cur.execute(make_table)
    conn.commit()

    statement1 = '''
        DROP TABLE IF EXISTS 'XS_Dogs';
    '''
    cur.execute(statement1)
    conn.commit()
    make_table1 = '''
        CREATE TABLE IF NOT EXISTS 'XS_Dogs' (
        'Breed Name' TEXT,
        'Group' TEXT,
        'Activity Level' TEXT,
        'Barking Level' TEXT,
        'Coat Type' TEXT,
        'Shedding' TEXT,
        'Trainability' TEXT
        );
    '''
    cur.execute(make_table1)
    conn.commit()


    statement2 = '''
        DROP TABLE IF EXISTS 'Small_Dogs';
    '''
    cur.execute(statement2)
    conn.commit()
    make_table2 = '''
        CREATE TABLE IF NOT EXISTS 'Small_Dogs' (
        'Breed Name' TEXT,
        'Group' TEXT,
        'Activity Level' TEXT,
        'Barking Level' TEXT,
        'Coat Type' TEXT,
        'Shedding' TEXT,
        'Trainability' TEXT
        );
    '''
    cur.execute(make_table2)
    conn.commit()

    statement3 = '''
        DROP TABLE IF EXISTS 'Medium_Dogs';
    '''
    cur.execute(statement3)
    conn.commit()
    make_table3 = '''
        CREATE TABLE IF NOT EXISTS 'Medium_Dogs' (
        'Breed Name' TEXT,
        'Group' TEXT,
        'Activity Level' TEXT,
        'Barking Level' TEXT,
        'Coat Type' TEXT,
        'Shedding' TEXT,
        'Trainability' TEXT
        );
    '''
    cur.execute(make_table3)
    conn.commit()

    statement4 = '''
        DROP TABLE IF EXISTS 'Large_Dogs';
    '''
    cur.execute(statement4)
    conn.commit()
    make_table4 = '''
        CREATE TABLE IF NOT EXISTS 'Large_Dogs' (
        'Breed Name' TEXT,
        'Group' TEXT,
        'Activity Level' TEXT,
        'Barking Level' TEXT,
        'Coat Type' TEXT,
        'Shedding' TEXT,
        'Trainability' TEXT
        );
    '''
    cur.execute(make_table4)
    conn.commit()

    statement5 = '''
        DROP TABLE IF EXISTS 'XL_Dogs';
    '''
    cur.execute(statement5)
    conn.commit()
    make_table5 = '''
        CREATE TABLE IF NOT EXISTS 'XL_Dogs' (
        'Breed Name' TEXT,
        'Group' TEXT,
        'Activity Level' TEXT,
        'Barking Level' TEXT,
        'Coat Type' TEXT,
        'Shedding' TEXT,
        'Trainability' TEXT
        );
    '''
    cur.execute(make_table5)
    conn.commit()

    # statement6 = '''
    #     DROP TABLE IF EXISTS 'Size';
    # '''
    # cur.execute(statement6)
    # conn.commit()
    # make_table6 = '''
    #     CREATE TABLE IF NOT EXISTS 'Size' (
    #         'XSmall' TEXT,
    #         'Small' TEXT,
    #         'Medium' TEXT,
    #         'Large' TEXT,
    #         'XLarge' TEXT
    #     );
    # '''
    # cur.execute(make_table6)
    # conn.commit()
    #
    # statement7 = '''
    #     DROP TABLE IF EXISTS 'Trainability';
    # '''
    # cur.execute(statement7)
    # conn.commit()
    # make_table7 = '''
    #     CREATE TABLE IF NOT EXISTS 'Trainability' (
    #         'May Be Stubborn' TEXT,
    #         'Eager To Please' TEXT,
    #         'Easy Training' TEXT,
    #         'Agreeable' TEXT,
    #         'Independent' TEXT
    #     );
    # '''
    # cur.execute(make_table7)
    # conn.commit()

    conn.close()

init_db(DBNAME)

def insert_dog_data():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    with open(MASTERCSV) as master_csv:
        csvReader = csv.reader(master_csv)
        for row in list(csvReader)[1:]:
            insertion = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) #, row[5]
            statement = 'INSERT INTO "Breeds"'
            statement += 'VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
            conn.commit()

    conn.close()

insert_dog_data()

### what I realistically probably want to do is create a master list/db with all of the information by breed
### and then create dbs that draw from that list, so I could make a "Medium" dogs db, which would include just
### dogs with "Medium" as their size and then all of their respective characteristics from the master list
