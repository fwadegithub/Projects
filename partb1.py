## Part B Task 1

import re
import pandas as pd
import os
import argparse

# change the directory to access the cricket articles, and record current directory to change back once the file has executed
fulldir = os.getcwd()
os.chdir(r"cricket")

# iterate through the articles and extract the filenames and document ID's
article_list = os.listdir() 
docID_list = []

for article_name in article_list:
# make sure its only the text files being iterated, not any notebooks
    if article_name[-3:] != 'txt':
        continue
    article = open(article_name, "r")
    article_text = article.read()
    triple_numberlist = re.findall(r'\d{3}', article_text)
    
# find all occurences of three consecutive integers and determine which is attached to a document ID

    for number in triple_numberlist:
        location = re.search(number, article_text).start()
        end = len(article_text)-1
        if (location<5) or (end-location<2):
            continue
        if (end-location<4):
            relevant_string = article_text[location-5:]
        else: 
            relevant_string = article_text[location-5:location+5]
        if (relevant_string[4] != '-') or (not relevant_string[0:4].isupper()):
            continue
        if (len(relevant_string) == 9) and (relevant_string[8].isupper()):
            isnine = 1
            if (len(relevant_string) == 10) and (relevant_string[9].islower()):
                isnine = 0
            if isnine:
                docID = relevant_string[0:9]
            break
        else:
            docID = relevant_string[0:8]
            break
            
    article_ID = [article_name, docID]
    docID_list.append(article_ID)

# identify the file input as the name of the csv the output will be saved to.
parser = argparse.ArgumentParser()
parser.add_argument("csv_name")
args = parser.parse_args()    
    
# make a dataframe of the filenames and docID's and export it to a csv in the assignment directory
os.chdir(fulldir)
columns = ['filename', 'documentID']
documents = pd.DataFrame(docID_list, columns = columns)

documents.to_csv(args.csv_name, index=False, header=True)
