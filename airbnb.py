import sqlite3
from collections import Counter
from nltk.corpus import wordnet as wn
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import tqdm
import json
from pprint import pprint

#Reads comments from ListingsAndReviews that match to a town name
def read_from_db(c, currentTown):
    c.execute("SELECT comments FROM ListingsAndReviews WHERE accurate_neighbourhood=?", (currentTown))
    data = c.fetchall()
    return data

def towns_from_db(c):
    c.execute('SELECT neighbourhood FROM neighbourhoods')
    data = c.fetchall()
    return data


def create_town_dicts(c, towns, numberWords):
    townDicts = {}
    
    for currentTown in tqdm.tqdm(towns):
        data = read_from_db(c, currentTown)

        temp = mostCommonWords(data, currentTown, numberWords)
        
        townDicts[currentTown[0].lower()] = temp

    return townDicts

def mostCommonWords(data, currentTown, numWords):
    idx = 0
    c = Counter()
    stop_words = set(stopwords.words('english'))  
    for d in tqdm.tqdm(data):
        adjectives = processAdjectives(d[0], stop_words)
        c += Counter(adjectives)
        idx += 1
    
    if numWords == 'all':
        return(dict(c))
    else:
        return(dict(c.most_common(numWords)))

def processAdjectives(content, stop_words):
    allAdjectives = []
    try:
        #check if there were comments
        if content:
            #regular expression to include hyphenated or apostrophed words as well 
            #r'(?=\S*[\'-]|\w+)(\w[a-zA-Z\'-]+|[a-zA-Z\'-]\w+)'
            #regular expression for words at least 3 characters long: \b\w{3}\w*\b
            tokenized = RegexpTokenizer(r'\w+').tokenize(content)

            filtered = [w for w in tokenized if not w in stop_words]
            tagged = pos_tag(filtered)
            
            allAdjectives.extend([s[0] for s in tagged if s[1] == 'JJ' or s[1] == 'JJS' or s[1] == 'JJR'])  
        
    except Exception as e:
        print(str(e))

    return allAdjectives

def average_rating_by_town(c, currentTown):
    c.execute("SELECT AVG(review_scores_rating) FROM ListingsAndReviews WHERE accurate_neighbourhood=?", (currentTown))
    data = c.fetchall()[0][0]
    return data
    

#Testing method. Should have JSON already loaded (if not, go do it with main method)
def test():
    conn = sqlite3.connect('./Data/airbnb.db')
    c = conn.cursor()

    towns = towns_from_db(c)
    with open('data.json', 'r') as fp:
        townDicts = json.load(fp)

    for town in townDicts:
        town_rating = average_rating_by_town(c, towns[0])
        print(f'{town} has an average rating of {town_rating} with these 40 most common words attributed to them \n')
        print(list(townDicts[town].keys()))
        print("\n")

    c.close
    conn.close()

def main():
    conn = sqlite3.connect('./Data/airbnb.db')
    c = conn.cursor()

    #These should be neighbourhoods not towns
    towns = towns_from_db(c)

    print(f"Welcome to the AirBnb data for NYC. There are {len(towns)} registered neighbourhoods in NYC")

    validAnswer = True
    while validAnswer:
        user = input("Have you processed the neighbourhood files yet? Type yes or no: ").lower()
        if user not in {'yes', 'no'}:
            print("That is not a valid answer!!\n")
        else:
            validAnswer = False
    
    if user == 'yes':
        validAnswer = True
        while validAnswer:
            user = input("Are you reviewing full or top 40 data? Type full or top: ").lower()
            if user not in {'full', 'top'}:
                print("That is not a valid answer!!\n")
            else:
                validAnswer = False

        with open(f'{user}Data.json', 'r') as fp:
            townDicts = json.load(fp)
    
    elif user == 'no':
        
        print("Before we begin, how many adjectives do you want to search for in every neighbourhood? " + 
            "Please give an integer answer. If you want to look through all adjectives, type all \n")
        validNumber = True
        while validNumber: 
            try:
                numberWords = input("Enter your answer: ").lower()
                if numberWords == 'all':
                    validNumber = False
                    prefix = "full"
                else:
                    numberWords = int(numberWords)
                    validNumber = False
                    prefix = "top"
            except ValueError:
                print("That's not a valid answer!")
        
        print("Now processing words for all neighbourhoods")
        townDicts = create_town_dicts(c, towns, numberWords)
        
        with open(f'{prefix}Data.json', 'w') as fp:
            json.dump(townDicts, fp, sort_keys=True, indent=4)
        
        print("Processing done")
    
    notQuit = True
    while notQuit:
        print("\nIf you would like to look for the neighbourhoods available, type neighborhood. " +
        "If you would like to search, type search. " +
        "If you would like to search by keyword, type keyword. " +
        "If you would like to quit, type quit. ")
        user = input().lower()

        if user == 'quit':
            notQuit = False
        elif user == 'search':
            user = input('Enter the neighborhood you want to search up: ').lower()
            if user in townDicts:
                pprint(list(townDicts[user].keys()))
            else:
                print("The town is not in the database!!\n")
        elif user == 'keyword':
            choice = input('\nDo you want to search by neighborhoods that have the keyword or neighborhoods that do not? Type have or not have: ').lower()
            
            valid = False
            while choice not in {'have', 'not have'}:
                print("I don't understand!! ")
                if not valid:
                    choice = input('\nDo you want to search by neighborhoods that have the keyword or neighborhoods that do not? Type have or not have: ').lower()

            user = input('\nEnter the keyword you want to search by: ').lower()
            temp = []
            filler = ''

            if choice == 'have':
                for town, keywords in townDicts.items():
                    if user in keywords:
                        temp.append(town)
                valid = False
            elif choice == 'not have':
                filler = 'not '
                for town, keywords in townDicts.items():
                    if user not in keywords:
                        temp.append(town)
                valid = False                   

            print(f"\nThere were {len(temp)} neighborhoods out of {len(townDicts)} " + 
                    f"that had \"{user}\" {filler}mentioned in their top 40 mentioned adjectives. " +
                    "The list of neighborhoods is printed below: ")
            pprint(temp)
        elif user == 'neighborhood':
            pprint(list(townDicts.keys()))
        else:
            print('\nI didn\'t understand that! Please enter your choice again')

    c.close
    conn.close()

if __name__ == '__main__':
    #Comment out the one you don't want to run

    main()