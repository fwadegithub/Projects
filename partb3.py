## Part B Task 3
import re
import sys
import pandas as pd
import nltk
import os

doc_IDs = pd.read_csv('partb1.csv', encoding = 'ISO-8859-1')

# reuse the function for preprocessing text
def preprocess(article_name):
    article_text = open(article_name, "r").read()
    preproc_text = re.sub(r'[^a-zA-Z]+', ' ', article_text)
    return preproc_text.lower()

fulldir = os.getcwd()
os.chdir(r"cricket")

# iterate through the articles searching for the keywords
article_list = os.listdir()
contain_keywords = []

for article_name in article_list:
    # make sure its only the text files becuase the notebook is in the currect dir
    if article_name[-3:] != 'txt':
        continue
    article_text = preprocess(article_name)
    contains_keywords = 1
    for keyword in sys.argv[1:]:
        pattern = r'( |\n|^)'+keyword.lower()+r'( |\n|\.)'
        if not re.search(pattern, article_text):     
            contains_keywords = 0
            break
    if contains_keywords:
        doc_ID = list(doc_IDs.loc[doc_IDs['filename'] == article_name].documentID.values)[0]
        contain_keywords.append(doc_ID)

# print a list of the document ID's representing documents that contain all the keywords exactly
print("Files containing the keywords: ")
print(contain_keywords, file = sys.stdout)  
        
os.chdir(fulldir)
