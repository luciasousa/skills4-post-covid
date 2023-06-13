#engenharia computacional (introdução e projeto) inglês e português

import base64
import re
import zlib
import pandas as pd
from bs4 import BeautifulSoup
import time
from pprint import pprint
import nltk
nltk.download('punkt')
import spacy
from sklearn.feature_extraction.text import CountVectorizer
import requests
import json
import textract
import os

# Define the ESCO API endpoint and language
ESCO_API_ENDPOINT = "http://localhost:8080/search"
ESCO_API_LANG_EN = "en"
ESCO_API_LANG_PT = "pt"


file = "../DPUC_2021_2022.xlsx"

cols = ['CodUC', 'NomeUC', 'Ano', 'Semestre', 'Estado', 'Campo', 'TextoPT', 'TextoEN']

db = pd.read_excel(file, usecols=cols)

filtered_db_intro_pt = db.loc[db['NomeUC'].isin(['INTRODUÇÃO À ENGENHARIA COMPUTACIONAL'])].copy()
filtered_db_intro_en = db.loc[db['NomeUC'].isin(['INTRODUÇÃO À ENGENHARIA COMPUTACIONAL'])].copy()
filtered_db_proj_pt = db.loc[db['NomeUC'].isin(['PROJETO EM ENGENHARIA COMPUTACIONAL'])].copy()
filtered_db_proj_en = db.loc[db['NomeUC'].isin(['PROJETO EM ENGENHARIA COMPUTACIONAL'])].copy()

# Remove HTML tags and extract text content
filtered_db_intro_pt.loc[:, 'TextoPT'] = filtered_db_intro_pt['TextoPT']
filtered_db_intro_en.loc[:, 'TextoEN'] = filtered_db_intro_en['TextoEN']

filtered_db_proj_pt.loc[:, 'TextoPT'] = filtered_db_proj_pt['TextoPT']
filtered_db_proj_en.loc[:, 'TextoEN'] = filtered_db_proj_en['TextoEN']

#remove stopwords
stopwords_pt = nltk.corpus.stopwords.words('portuguese')
stopwords_en = nltk.corpus.stopwords.words('english')

text_tokens_intro_pt = [nltk.word_tokenize(text) for text in filtered_db_intro_pt['TextoPT'].tolist() if isinstance(text, str)]
text_tokens_intro_en = [nltk.word_tokenize(text) for text in filtered_db_intro_en['TextoEN'].tolist() if isinstance(text, str)]
text_tokens_proj_pt = [nltk.word_tokenize(text) for text in filtered_db_proj_pt['TextoPT'].tolist() if isinstance(text, str)]
text_tokens_proj_en = [nltk.word_tokenize(text) for text in filtered_db_proj_en['TextoEN'].tolist() if isinstance(text, str)]

#extract the sentences from the text
sentences_intro_pt = [nltk.sent_tokenize(' '.join(tokens)) for tokens in text_tokens_intro_pt]
sentences_intro_en = [nltk.sent_tokenize(' '.join(tokens)) for tokens in text_tokens_intro_en]
sentences_proj_pt = [nltk.sent_tokenize(' '.join(tokens)) for tokens in text_tokens_proj_pt]
sentences_proj_en = [nltk.sent_tokenize(' '.join(tokens)) for tokens in text_tokens_proj_en]

#remove stopwords from the sentences

sentences_without_sw_intro_pt = []
for sentence in sentences_intro_pt:
    sentence_tokens = nltk.word_tokenize(str(sentence))
    sentence_without_sw = [word for word in sentence_tokens if not word in stopwords_pt]
    sentences_without_sw_intro_pt.append(sentence_without_sw)


sentences_without_sw_intro_en = []
for sentence in sentences_intro_en:
    sentence_tokens = nltk.word_tokenize(str(sentence))
    sentence_without_sw = [word for word in sentence_tokens if not word in stopwords_en]
    sentences_without_sw_intro_en.append(sentence_without_sw)


sentences_without_sw_proj_pt = []
for sentence in sentences_proj_pt:
    sentence_tokens = nltk.word_tokenize(str(sentence))
    sentence_without_sw = [word for word in sentence_tokens if not word in stopwords_pt]
    sentences_without_sw_proj_pt.append(sentence_without_sw)


sentences_without_sw_proj_en = []
for sentence in sentences_proj_en:
    sentence_tokens = nltk.word_tokenize(str(sentence))
    sentence_without_sw = [word for word in sentence_tokens if not word in stopwords_en]
    sentences_without_sw_proj_en.append(sentence_without_sw)


skills = []
sentence = ' '.join([re.sub(r'[^a-zA-Z\s]', '', str(s)) for s in sentences_without_sw_intro_pt])
sentence = ' '.join(dict.fromkeys(sentence.split()))
firstpart, secondpart = sentence[:len(sentence)//2], sentence[len(sentence)//2:]
print(sentence)

response1 = requests.get(ESCO_API_ENDPOINT + "?text=" + firstpart + "&language=" + ESCO_API_LANG_PT +  "&type=skill&facet=type&facet=isInScheme&full=true&q=computer%20engineering")
response2 = requests.get(ESCO_API_ENDPOINT + "?text=" + secondpart + "&language=" + ESCO_API_LANG_PT +  "&type=skill&facet=type&facet=isInScheme&full=true&q=computer%20engineering")

# Check if the request was successful

if response1.status_code != 200 and response2.status_code != 200:
    print("Error fetching data from API")
else:
    # Extract the data from the response
    data1 = response1.json()
    data2 = response2.json()
    # Print the matches and their positions in the text
    #print("Sentence: " + sentence)
    for match in data1["_embedded"]["results"]:
        skill = match['preferredLabel'][ESCO_API_LANG_PT]
        skills.append(skill)
    for match in data2["_embedded"]["results"]:
        skill = match['preferredLabel'][ESCO_API_LANG_PT]
        skills.append(skill)
        #print("ESCO: ",f"{match['preferredLabel']['en']}")

#print(skills)
with open("skills_engenharia_computactional_pt/skills_introducao_pt.txt", "w") as f:
    f.write('\n'.join(skills))

f.close()

skills = []
sentence = ' '.join([re.sub(r'[^a-zA-Z\s]', '', str(s)) for s in sentences_without_sw_proj_pt])
sentence = ' '.join(dict.fromkeys(sentence.split()))
firstpart, secondpart = sentence[:len(sentence)//2], sentence[len(sentence)//2:]
print(sentence)

response1 = requests.get(ESCO_API_ENDPOINT + "?text=" + firstpart + "&language=" + ESCO_API_LANG_PT +  "&type=skill&facet=type&facet=isInScheme&full=true&q=computer%20engineering")
response2 = requests.get(ESCO_API_ENDPOINT + "?text=" + secondpart + "&language=" + ESCO_API_LANG_PT +  "&type=skill&facet=type&facet=isInScheme&full=true&q=computer%20engineering")

# Check if the request was successful

if response1.status_code != 200 and response2.status_code != 200:
    print("Error fetching data from API")
else:
    # Extract the data from the response
    data1 = response1.json()
    data2 = response2.json()
    # Print the matches and their positions in the text
    #print("Sentence: " + sentence)
    for match in data1["_embedded"]["results"]:
        skill = match['preferredLabel'][ESCO_API_LANG_PT]
        skills.append(skill)
    for match in data2["_embedded"]["results"]:
        skill = match['preferredLabel'][ESCO_API_LANG_PT]
        skills.append(skill)
        #print("ESCO: ",f"{match['preferredLabel']['en']}")

#print(skills)
with open("skills_engenharia_computactional_pt/skills_projeto_pt.txt", "w") as f:
    f.write('\n'.join(skills))

f.close()


skills = []
sentence = ' '.join([re.sub(r'[^a-zA-Z\s]', '', str(s)) for s in sentences_without_sw_intro_en])
sentence = ' '.join(dict.fromkeys(sentence.split()))
firstpart, secondpart = sentence[:len(sentence)//2], sentence[len(sentence)//2:]
#compressed_data = zlib.compress(sentence.encode())
# Get the compressed data as a string
#sentence = base64.b64encode(compressed_data).decode()
print(sentence)

response1 = requests.get(ESCO_API_ENDPOINT + "?text=" + firstpart + "&language=" + ESCO_API_LANG_EN +  "&type=skill&facet=type&facet=isInScheme&full=true&q=computer%20engineering")
response2 = requests.get(ESCO_API_ENDPOINT + "?text=" + secondpart + "&language=" + ESCO_API_LANG_EN +  "&type=skill&facet=type&facet=isInScheme&full=true&q=computer%20engineering")

# Check if the request was successful

if response1.status_code != 200 and response2.status_code != 200:
    print("Error fetching data from API")
else:
    # Extract the data from the response
    data1 = response1.json()
    data2 = response2.json()
    # Print the matches and their positions in the text
    #print("Sentence: " + sentence)
    for match in data1["_embedded"]["results"]:
        skill = match['preferredLabel'][ESCO_API_LANG_EN]
        skills.append(skill)
    for match in data2["_embedded"]["results"]:
        skill = match['preferredLabel'][ESCO_API_LANG_EN]
        skills.append(skill)
        #print("ESCO: ",f"{match['preferredLabel']['en']}")

#print(skills)   
with open("skills_engenharia_computacional_en/skills_introducao_en.txt", "w") as f:
    f.write('\n'.join(skills))

f.close()

skills = []
sentence = ' '.join([re.sub(r'[^a-zA-Z\s]', '', str(s)) for s in sentences_without_sw_proj_en])
sentence = ' '.join(dict.fromkeys(sentence.split()))
firstpart, secondpart = sentence[:len(sentence)//2], sentence[len(sentence)//2:]
#compressed_data = zlib.compress(sentence.encode())
# Get the compressed data as a string
#sentence = base64.b64encode(compressed_data).decode()
print(sentence)

response1 = requests.get(ESCO_API_ENDPOINT + "?text=" + firstpart + "&language=" + ESCO_API_LANG_EN +  "&type=skill&facet=type&facet=isInScheme&full=true&q=computer%20engineering")
response2 = requests.get(ESCO_API_ENDPOINT + "?text=" + secondpart + "&language=" + ESCO_API_LANG_EN +  "&type=skill&facet=type&facet=isInScheme&full=true&q=computer%20engineering")

# Check if the request was successful

if response1.status_code != 200 and response2.status_code != 200:
    print("Error fetching data from API")
else:
    # Extract the data from the response
    data1 = response1.json()
    data2 = response2.json()
    # Print the matches and their positions in the text
    #print("Sentence: " + sentence)
    for match in data1["_embedded"]["results"]:
        skill = match['preferredLabel'][ESCO_API_LANG_EN]
        skills.append(skill)
    for match in data2["_embedded"]["results"]:
        skill = match['preferredLabel'][ESCO_API_LANG_EN]
        skills.append(skill)
        #print("ESCO: ",f"{match['preferredLabel']['en']}")

#print(skills)        
with open("skills_engenharia_computacional_en/skills_projeto_en.txt", "w") as f:
    f.write('\n'.join(skills))

f.close()


