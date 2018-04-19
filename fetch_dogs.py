import sqlite3
import csv
import json
import requests
import requests_cache
import webbrowser
import random
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, url_for

###FILE NAMES###

MASTERCSV = 'master_list.csv'
DBNAME = 'good_boys.db'
CACHE_FNAME = 'cache_money.json'

###URL PIECES###

baseurl = 'http://www.akc.org/dog-breeds/'
page = 'page/'
gibberish = '%5B0%5D='
activity_level = '/?activity_level'
barking_level = '/?barking_level'
coat_type = '/?coat_type'
shedding = '/?shedding'
size = '/?size'
trainability = '/?trainability'

###CACHE CODE###

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

###FUNCTION DEFINITIONS###

def scrape_breed_names(list1, list2):
    for x in list1:
        page_text = make_request_using_cache(x)
        page_soup = BeautifulSoup(page_text, 'html.parser')
        ###can I impliment caching here?
        content_div = page_soup.find_all(class_="breed-type-card__title mt0 mb0 f-25 py3 px3")
        for item in content_div:
            breed_text = item.string
            if breed_text not in list2:
                list2.append(breed_text)
    return list2

###CALL ALL FUNCTIONS AT BOTTOM###

crawl_list = []
for x in range(1,24): #24
    crawlurl = 'page/' + str(x) + '/'
    crawl_list.append(baseurl + crawlurl)

breed_list = []
k = scrape_breed_names(crawl_list, breed_list)

##MAKE BELOW INTO FUNCTIONS OR CLASSES OR WHATEVER###

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
for x in breed_urls[0:15]:
    page_text = make_request_using_cache(x)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    content_div = page_soup.find_all(class_="attribute-list__description attribute-list__text ")
    for item in content_div:
        a_tag = item.find('a')
        if a_tag != None:
            group_list.append(a_tag.string)

### fixing random mistakes in the list
group_list.insert(13, 'Foundation Stock Service')



def crawl_urls(x,y,category,string,list):
    # if x != y:
    #     for i in range(x,y):
    #         crawlurl = page + str(i) + category + gibberish + string
    #         list.append(baseurl + crawlurl)
    #     return list
    # else:
    crawlurl = category[1:] + gibberish + string
    list.append(baseurl + crawlurl)
    return list

###ACTIVITY LEVEL###

reg_ex = []
calm = []
needs_activity = []
energetic = []

crawl_urls(1,1,activity_level,'regular-exercise',reg_ex)
crawl_urls(1,1,activity_level,'calm',calm)
crawl_urls(1,1,activity_level,'needs-lots-of-activity',needs_activity)
crawl_urls(1,1,activity_level,'energetic',energetic)

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

crawl_urls(1,1,barking_level,'when_necessary',necessity)
crawl_urls(1,1,barking_level,'medium',medium)
crawl_urls(1,1,barking_level,'likes-to-be-vocal',talkative)
crawl_urls(1,1,barking_level,'infrequent',in_frequent)
crawl_urls(1,1,barking_level,'frequent',out_frequent)

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
crawl_urls(1,1,coat_type,'medium',medium_hair)
crawl_urls(1,1,coat_type,'smooth',smooth)
crawl_urls(1,1,coat_type,'short',short_hair)
crawl_urls(1,1,coat_type,'long',long_hair)
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

crawl_urls(1,1,shedding,'infrequent',infrq_shed)
crawl_urls(1,1,shedding,'frequent',frq_shed)
crawl_urls(1,1,shedding,'regularly',reg_shed)
crawl_urls(1,1,shedding,'seasonal',seas_shed)
crawl_urls(1,1,shedding,'occasional',occ_shed)

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

crawl_urls(1,1,size,'xsmall',sz_xsmall)
crawl_urls(1,1,size,'small',sz_small)
crawl_urls(1,1,size,'medium',sz_medium)
crawl_urls(1,1,size,'large',sz_large)
crawl_urls(1,1,size,'xlarge',sz_xlarge)

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

crawl_urls(1,1,trainability,'may-be-stubborn',may_be_stubborn)
crawl_urls(1,1,trainability,'eager-to-please',eager_to_please)
crawl_urls(1,1,trainability,'easy-training',easy_training)
crawl_urls(1,1,trainability,'agreeable',agreeable)
crawl_urls(1,1,trainability,'independent',independent)

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

###DOG_DICT###

dog_dict = {}
for y in range(len(breed_list[0:15])):
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
        'BreedName' TEXT,
        'Group_Id' INTEGER,
        'ActivityLevel_Id' INTEGER,
        'BarkingLevel_Id' TEXT,
        'CoatType_Id' TEXT,
        'Shedding_Id' TEXT,
        'Size_Id' INTEGER,
        'Trainability_Id' TEXT,
        FOREIGN KEY('Size_Id') REFERENCES 'Size'('Id'),
        FOREIGN KEY('Group_Id') REFERENCES 'Group'('Id'),
        FOREIGN KEY('ActivityLevel_Id') REFERENCES 'Activity_Level'('Id'),
        FOREIGN KEY('BarkingLevel_Id') REFERENCES 'Barking_Level'('Id'),
        FOREIGN KEY('CoatType_Id') REFERENCES 'Coat_Type'('Id'),
        FOREIGN KEY('Shedding_Id') REFERENCES 'Shedding'('Id'),
        FOREIGN KEY('Trainability_Id') REFERENCES 'Trainability'('Id')
        );
    '''
    cur.execute(make_table)
    conn.commit()

    statement1 = '''
        DROP TABLE IF EXISTS 'Size';
    '''
    cur.execute(statement1)
    conn.commit()
    make_table1 = '''
        CREATE TABLE IF NOT EXISTS 'Size' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Description' TEXT
        );
    '''
    cur.execute(make_table1)
    conn.commit()

    statement2 = '''
        DROP TABLE IF EXISTS 'Group';
    '''
    cur.execute(statement2)
    conn.commit()
    make_table2 = '''
        CREATE TABLE IF NOT EXISTS 'Group' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Description' TEXT
        );
    '''
    cur.execute(make_table2)
    conn.commit()

    statement3 = '''
        DROP TABLE IF EXISTS 'Activity_Level';
    '''
    cur.execute(statement3)
    conn.commit()
    make_table3 = '''
        CREATE TABLE IF NOT EXISTS 'Activity_Level' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Description' TEXT
        );
    '''
    cur.execute(make_table3)
    conn.commit()

    statement4 = '''
        DROP TABLE IF EXISTS 'Barking_Level';
    '''
    cur.execute(statement4)
    conn.commit()
    make_table4 = '''
        CREATE TABLE IF NOT EXISTS 'Barking_Level' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Description' TEXT
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
        'Description' TEXT
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
        'Description' TEXT
        );
    '''
    cur.execute(make_table6)
    conn.commit()

    statement7 = '''
        DROP TABLE IF EXISTS 'Trainability';
    '''
    cur.execute(statement7)
    conn.commit()
    make_table7 = '''
        CREATE TABLE IF NOT EXISTS 'Trainability' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Description' TEXT
        );
    '''
    cur.execute(make_table7)
    conn.commit()

    conn.close()

###############################

def insert_dog_data():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    with open(MASTERCSV) as master_csv:
        csvReader = csv.reader(master_csv)
        pupdata = {}
        for row in list(csvReader)[1:]:
            pupdata[row[0]] = [row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
            insertion = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            statement = 'INSERT INTO "Breeds"'
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)
            conn.commit()

    conn.close()
    return pupdata

############################

def insert_size_data(pupdata):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement1 = '''
    INSERT INTO 'Size'('Description')
    VALUES ('XSmall')
    '''
    cur.execute(statement1)
    conn.commit()

    statement2 = '''
    INSERT INTO 'Size'('Description')
    VALUES ('Small')
    '''
    cur.execute(statement2)
    conn.commit()

    statement3 = '''
    INSERT INTO 'Size'('Description')
    VALUES ('Medium')
    '''
    cur.execute(statement3)
    conn.commit()

    statement4 = '''
    INSERT INTO 'Size'('Description')
    VALUES ('Large')
    '''
    cur.execute(statement4)
    conn.commit()

    statement5 = '''
    INSERT INTO 'Size'('Description')
    VALUES ('XLarge')
    '''
    cur.execute(statement5)
    conn.commit()

    statement6 = '''
    INSERT INTO 'Size'('Description')
    VALUES ('Not Specified')
    '''
    cur.execute(statement6)
    conn.commit()

    size_dict = {'XSmall':1, 'Small':2, 'Medium':3, 'Large':4, 'XLarge':5, 'Not Specified':6}

    for key in pupdata:
        statement8 = 'UPDATE Breeds SET Size_Id =' + str(size_dict[(pupdata[key][5])]) + ' WHERE BreedName =' '"' + key + '"'
        cur.execute(statement8)
        conn.commit()

    conn.close()

############################

def insert_group_data(pupdata):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement1 = '''
    INSERT INTO 'Group'('Description')
    VALUES ('Sporting Group')
    '''
    cur.execute(statement1)
    conn.commit()

    statement2 = '''
    INSERT INTO 'Group'('Description')
    VALUES ('Working Group')
    '''
    cur.execute(statement2)
    conn.commit()

    statement3 = '''
    INSERT INTO 'Group'('Description')
    VALUES ('Toy Group')
    '''
    cur.execute(statement3)
    conn.commit()

    statement4 = '''
    INSERT INTO 'Group'('Description')
    VALUES ('Herding Group')
    '''
    cur.execute(statement4)
    conn.commit()

    statement5 = '''
    INSERT INTO 'Group'('Description')
    VALUES ('Foundation Stock Service')
    '''
    cur.execute(statement5)
    conn.commit()

    statement6 = '''
    INSERT INTO 'Group'('Description')
    VALUES ('Hound Group')
    '''
    cur.execute(statement6)
    conn.commit()

    statement7 = '''
    INSERT INTO 'Group'('Description')
    VALUES ('Terrier Group')
    '''
    cur.execute(statement7)
    conn.commit()

    statement8 = '''
    INSERT INTO 'Group'('Description')
    VALUES ('Non-Sporting Group')
    '''
    cur.execute(statement8)
    conn.commit()

    statement9 = '''
    INSERT INTO 'Group'('Description')
    VALUES ('Miscellaneous Class')
    '''
    cur.execute(statement9)
    conn.commit()

    statement10 = '''
    INSERT INTO 'Group'('Description')
    VALUES ('Not Specified')
    '''
    cur.execute(statement10)
    conn.commit()

    group_dict = {'Sporting Group':1, 'Working Group':2, 'Toy Group':3, 'Herding Group':4, 'Foundation Stock Service':5, 'Hound Group':6, 'Terrier Group':7, 'Non-Sporting Group':8, 'Miscellaneous Class':9, 'Not Specified':10}

    for key in pupdata:
        statement8 = 'UPDATE Breeds SET Group_Id =' + str(group_dict[(pupdata[key][0])]) + ' WHERE BreedName =' '"' + key + '"'
        cur.execute(statement8)
        conn.commit()

    conn.close()

############################

def insert_act_data(pupdata):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement1 = '''
    INSERT INTO 'Activity_Level'('Description')
    VALUES ('Regular Exercise')
    '''
    cur.execute(statement1)
    conn.commit()

    statement2 = '''
    INSERT INTO 'Activity_Level'('Description')
    VALUES ('Calm')
    '''
    cur.execute(statement2)
    conn.commit()

    statement3 = '''
    INSERT INTO 'Activity_Level'('Description')
    VALUES ('Needs Lots Of Activity')
    '''
    cur.execute(statement3)
    conn.commit()

    statement4 = '''
    INSERT INTO 'Activity_Level'('Description')
    VALUES ('Energetic')
    '''
    cur.execute(statement4)
    conn.commit()

    statement5 = '''
    INSERT INTO 'Activity_Level'('Description')
    VALUES ('Not Specified')
    '''
    cur.execute(statement5)
    conn.commit()

    act_dict = {'Regular Exercise':1, 'Calm':2, 'Needs Lots Of Activity':3, 'Energetic':4, 'Not Specified':5}

    for key in pupdata:
        statement8 = 'UPDATE Breeds SET ActivityLevel_Id =' + str(act_dict[(pupdata[key][1])]) + ' WHERE BreedName =' '"' + key + '"'
        cur.execute(statement8)
        conn.commit()

    conn.close()

#############################

def insert_bark_data(pupdata):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement1 = '''
    INSERT INTO 'Barking_Level'('Description')
    VALUES ('When Necessary')
    '''
    cur.execute(statement1)
    conn.commit()

    statement2 = '''
    INSERT INTO 'Barking_Level'('Description')
    VALUES ('Medium')
    '''
    cur.execute(statement2)
    conn.commit()

    statement3 = '''
    INSERT INTO 'Barking_Level'('Description')
    VALUES ('Likes To Be Vocal')
    '''
    cur.execute(statement3)
    conn.commit()

    statement4 = '''
    INSERT INTO 'Barking_Level'('Description')
    VALUES ('Infrequent')
    '''
    cur.execute(statement4)
    conn.commit()

    statement5 = '''
    INSERT INTO 'Barking_Level'('Description')
    VALUES ('Frequent')
    '''
    cur.execute(statement5)
    conn.commit()

    statement6 = '''
    INSERT INTO 'Barking_Level'('Description')
    VALUES ('Not Specified')
    '''
    cur.execute(statement6)
    conn.commit()

    bark_dict = {'When Necessary':1, 'Medium':2, 'Likes To Be Vocal':3, 'Infrequent':4, 'Frequent':5, 'Not Specified':6}

    for key in pupdata:
        statement8 = 'UPDATE Breeds SET BarkingLevel_Id =' + str(bark_dict[(pupdata[key][2])]) + ' WHERE BreedName =' '"' + key + '"'
        cur.execute(statement8)
        conn.commit()

    conn.close()

############################

def insert_coat_data(pupdata):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement1 = '''
    INSERT INTO 'Coat_Type'('Description')
    VALUES ('Hairless')
    '''
    cur.execute(statement1)
    conn.commit()

    statement2 = '''
    INSERT INTO 'Coat_Type'('Description')
    VALUES ('Medium')
    '''
    cur.execute(statement2)
    conn.commit()

    statement3 = '''
    INSERT INTO 'Coat_Type'('Description')
    VALUES ('Smooth')
    '''
    cur.execute(statement3)
    conn.commit()

    statement4 = '''
    INSERT INTO 'Coat_Type'('Description')
    VALUES ('Short')
    '''
    cur.execute(statement4)
    conn.commit()

    statement5 = '''
    INSERT INTO 'Coat_Type'('Description')
    VALUES ('Long')
    '''
    cur.execute(statement5)
    conn.commit()

    statement6 = '''
    INSERT INTO 'Coat_Type'('Description')
    VALUES ('Wire')
    '''
    cur.execute(statement6)
    conn.commit()

    statement7 = '''
    INSERT INTO 'Coat_Type'('Description')
    VALUES ('Not Specified')
    '''
    cur.execute(statement7)
    conn.commit()

    coat_dict = {'Hairless':1, 'Medium':2, 'Smooth':3, 'Short':4, 'Long':5, 'Wire':6, 'Not Specified':7}

    for key in pupdata:
        statement8 = 'UPDATE Breeds SET CoatType_Id =' + str(coat_dict[(pupdata[key][3])]) + ' WHERE BreedName =' '"' + key + '"'
        cur.execute(statement8)
        conn.commit()

    conn.close()

############################

def insert_shed_data(pupdata):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement1 = '''
    INSERT INTO 'Shedding'('Description')
    VALUES ('Infrequent')
    '''
    cur.execute(statement1)
    conn.commit()

    statement2 = '''
    INSERT INTO 'Shedding'('Description')
    VALUES ('Frequent')
    '''
    cur.execute(statement2)
    conn.commit()

    statement3 = '''
    INSERT INTO 'Shedding'('Description')
    VALUES ('Regularly')
    '''
    cur.execute(statement3)
    conn.commit()

    statement4 = '''
    INSERT INTO 'Shedding'('Description')
    VALUES ('Seasonal')
    '''
    cur.execute(statement4)
    conn.commit()

    statement5 = '''
    INSERT INTO 'Shedding'('Description')
    VALUES ('Occasional')
    '''
    cur.execute(statement5)
    conn.commit()

    statement6 = '''
    INSERT INTO 'Shedding'('Description')
    VALUES ('Not Specified')
    '''
    cur.execute(statement6)
    conn.commit()

    shedding_dict = {'Infrequent':1, 'Frequent':2, 'Regularly':3, 'Seasonal':4, 'Occasional':5, 'Not Specified':6}

    for key in pupdata:
        statement8 = 'UPDATE Breeds SET Shedding_Id =' + str(shedding_dict[(pupdata[key][4])]) + ' WHERE BreedName =' '"' + key + '"'
        cur.execute(statement8)
        conn.commit()

    conn.close()

############################

def insert_train_data(pupdata):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement1 = '''
    INSERT INTO 'Trainability'('Description')
    VALUES ('May Be Stubborn')
    '''
    cur.execute(statement1)
    conn.commit()

    statement2 = '''
    INSERT INTO 'Trainability'('Description')
    VALUES ('Eager To Please')
    '''
    cur.execute(statement2)
    conn.commit()

    statement3 = '''
    INSERT INTO 'Trainability'('Description')
    VALUES ('Easy Training')
    '''
    cur.execute(statement3)
    conn.commit()

    statement4 = '''
    INSERT INTO 'Trainability'('Description')
    VALUES ('Agreeable')
    '''
    cur.execute(statement4)
    conn.commit()

    statement5 = '''
    INSERT INTO 'Trainability'('Description')
    VALUES ('Independent')
    '''
    cur.execute(statement5)
    conn.commit()

    statement6 = '''
    INSERT INTO 'Trainability'('Description')
    VALUES ('Not Specified')
    '''
    cur.execute(statement6)
    conn.commit()

    train_dict = {'May Be Stubborn':1, 'Eager To Please':2, 'Easy Training':3, 'Agreeable':4, 'Independent':5, 'Not Specified':6}

    for key in pupdata:
        statement8 = 'UPDATE Breeds SET Trainability_Id =' + str(train_dict[(pupdata[key][6])]) + ' WHERE BreedName =' '"' + key + '"'
        cur.execute(statement8)
        conn.commit()

    conn.close()

############################

init_db(DBNAME)

x = insert_dog_data()
insert_size_data(x)
insert_group_data(x)
insert_act_data(x)
insert_bark_data(x)
insert_coat_data(x)
insert_shed_data(x)
insert_train_data(x)

# ###FLASK APP###

def fetch_data():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    results = cur.execute('SELECT * FROM Breeds WHERE Size_Id=5 ORDER BY BreedName')
    res_list = results.fetchall()
    return res_list
    conn.close()

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contents')
def contents():
    return render_template('contents.html')

@app.route('/petitepups')
def petitepups():
    return render_template('petitepups.html')

@app.route('/bigboys')
def bigboys():
    rows = fetch_data()
    fetch_template = {
    'res_list':rows
    }
    return render_template('bigboys.html', **fetch_template)

if __name__ == '__main__':
    print('starting Flask app', app.name)
    app.run(debug=True)
