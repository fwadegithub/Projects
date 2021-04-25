# Part B Task 2
import re
import os
import sys

# record the current directory to change back at after execution
fulldir = os.getcwd()
os.chdir(r"cricket")

# create a function to preprocess the article
def preprocess(article_name):
    article_text = open(article_name, "r").read()
    preproc_text = re.sub(r'[^a-zA-Z]+', ' ', article_text)
    return preproc_text.lower()

# extract the article name from the input, precprocess it and print it to standard output
article_name = sys.argv[1]
article = str(article_name[-7:])

preprocessed_article = preprocess(article)
print(preprocessed_article, file = sys.stdout)

os.chdir(fulldir)