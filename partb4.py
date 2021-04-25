## Part B Task 4
import re
import pandas as pd
import os
import sys
import nltk
from nltk.stem.porter import *
from nltk.tokenize.treebank import TreebankWordDetokenizer
# nltk.download('punkt')

porterStemmer = PorterStemmer()

doc_IDs = pd.read_csv('partb1.csv', encoding = 'ISO-8859-1')

# reuse the function for preprocessing text, this time taking the stem of each word
def preprocess(article_name):
    article_text = open(article_name, "r").read()
    preproc_text = re.sub(r'[^a-zA-Z]+', ' ', article_text)
    wordlist = nltk.word_tokenize(preproc_text)
    for i in range(len(wordlist)):
        wordlist[i] = porterStemmer.stem(wordlist[i])
    preproc_text = TreebankWordDetokenizer().detokenize(wordlist)
    return preproc_text.lower()

# navigate to the correct directory.
fulldir = os.getcwd()
os.chdir(r'cricket')

# iterate through the articles searching for the keywords
article_list = os.listdir()
contain_keywords = []

for article_name in article_list:
    # make sure its only the text files being searched.
    if article_name[-3:] != 'txt':
        continue
    article_text = preprocess(article_name)
    contains_keywords = 1
    
# search for the stem of each keyword in the updated stem text files.
    for keyword in sys.argv[1:]:
        stem = porterStemmer.stem(keyword)
        pattern = r'( |\n|^)'+stem.lower()+r'( |\n|\.)'
        if not re.search(pattern, article_text):     
            contains_keywords = 0
            break
    if contains_keywords:
        doc_ID = list(doc_IDs.loc[doc_IDs['filename'] == article_name].documentID.values)[0]
        contain_keywords.append(doc_ID)
        
# print a list of the document ID's representing documents that contain all the keyword stem matches
print("Files containing the keywords: ")
print(contain_keywords, file = sys.stdout)    
os.chdir(fulldir)