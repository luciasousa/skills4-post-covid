#./catalina.sh run

import time
from pprint import pprint
import nltk
nltk.download('punkt')
import spacy
from sklearn.feature_extraction.text import CountVectorizer
import requests
import json
import textract

url = "http://localhost:8080/resource/taxonomy?uri=http://data.europa.eu/esco/concept-scheme/isco&language=pt"
url = "http://localhost:8080/search?text=manager&language=pt&type=occupation&type=skill&type=concept&facet=type&facet=isInScheme&limit=2&offset=2&full=true"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error fetching data from API")

file_name = "../fichas_UCs_MEET/Uc_DEGEIT/DPUC_47121_2017-2018_v1_pt.pdf"

# read the pdf file and extract the text from it
text = textract.process(file_name, method='pdfminer').decode('utf-8')
print(text)

# split the text into sentences
tokens = nltk.sent_tokenize(text)

# search text for keywords in esco taxonomy and return the results
url = "http://localhost:8080/search?text="+ str(tokens[15]) +"&language=pt&type=occupation&type=skill&type=concept&facet=type&facet=isInScheme&limit=2&offset=2&full=true"
print("WORD: ",tokens[15])
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error fetching data from API")

