## Part B Task 5
import re
import os
import sys
import pandas as pd
import nltk
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfTransformer
import math
from numpy import dot
from numpy.linalg import norm
from nltk.stem.porter import *
from nltk.tokenize.treebank import TreebankWordDetokenizer
# nltk.download('stopwords')
from nltk.corpus import stopwords
stopWords = set(stopwords.words('english'))

# reuse the code from part b task 4 to get the list of documents containing all the keywords.

porterStemmer = PorterStemmer()

doc_IDs = pd.read_csv('partb1.csv', encoding = 'ISO-8859-1')

# reuse the function for preprocessing text, this time removing stop words as well
def preprocess(article_name):
    article_text = open(article_name, "r").read()
    preproc_text = re.sub(r'[^a-zA-Z]+', ' ', article_text)
    wordlist = nltk.word_tokenize(preproc_text)
    for i in range(len(wordlist)):
        wordlist[i] = porterStemmer.stem(wordlist[i])   
    stopwords_removed = [word for word in wordlist if not word in stopWords]
    preproc_text = TreebankWordDetokenizer().detokenize(stopwords_removed)
    return preproc_text.lower()

# navigate to the correct directory.
fulldir = os.getcwd()
os.chdir(r'cricket')

# iterate through the articles searching for the keywords
article_list = os.listdir()
contain_keywords = []
total_wordlist = []
keyword_list=[]

for article_name in article_list:
    # make sure its only the text files being searched.
    if article_name[-3:] != 'txt':
        continue
    article_text = preprocess(article_name)
    contains_keywords = 1
    
# search for the stem of each keyword in the updated stem text files.
    for keyword in sys.argv[1:]:
        stem = porterStemmer.stem(keyword)
        keyword_list.append(stem)
        pattern = r'( |\n|^)'+stem.lower()+r'( |\n|\.)'
        if not re.search(pattern, article_text):     
            contains_keywords = 0
            break
    if contains_keywords:
        doc_ID = list(doc_IDs.loc[doc_IDs['filename'] == article_name].documentID.values)[0]
        contain_keywords.append(doc_ID)
# create a list of all the words contained in articles that have all the keywords.
        for word in nltk.word_tokenize(article_text):
            total_wordlist.append(word)
        
# find the term count of the total words in each document.
# Each document from contain_keywords will be represented by a row in the term counts array.
total_words = set(total_wordlist)
term_counts = []

for docID in contain_keywords:
    article = list(doc_IDs.loc[doc_IDs['documentID'] == docID].filename.values)[0]
    article_text = preprocess(article)
    article_dic = defaultdict(int)
    for word in total_words:
        pattern = r'( |\n|^)'+word+r'( |\n|\.)'
        article_dic[word] = len(re.findall(pattern, article_text))
    term_counts.append(list(article_dic.values()))
    
# find the TF-IDF vector for each document.
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(term_counts)
tfidf_array = tfidf.toarray()

# create the query vector of the stemmed keywords.
query = []
for i in range(len(total_words)):
    if list(total_words)[i] in keyword_list:
        query.append(1/math.sqrt(len(keyword_list)))
    else:
        query.append(0)
        
# calculate the cosine similarities between the query and the TF-IDF vector of each document.
cosine_sims = []

for i in range(len(contain_keywords)):
    tfidf_vec = tfidf_array[i]
    cosine_sim = dot(query, tfidf_vec)/(norm(query)*norm(tfidf_vec))
    cosine_sims.append(cosine_sim)
    
# present the results in a dataframe.
similarity_scores = pd.DataFrame(cosine_sims, index = contain_keywords, columns = ['score'])
similarity_scores.index.name = 'documentID'
sorted_similarity_scores = similarity_scores.sort_values( by = 'score', ascending = False)
print(sorted_similarity_scores, file = sys.stdout)

os.chdir(fulldir)