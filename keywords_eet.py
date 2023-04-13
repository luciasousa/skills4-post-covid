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
ESCO_API_LANG = "en"

#read all .doc files from a folder
path = "../fichas_UCs_MEET/UC_DETI_plano/"
files = os.listdir(path)

nltk.download('stopwords')

for file in files:
    if file.endswith(".doc"):
        file_name = path + file
        print(file_name)

        #read the text file and convert to a string
        try:
            text = textract.process(file_name, method='doc').decode('utf-8')
        except:
            text = textract.process(file_name, method='docx').decode('utf-8')

        #remove stopwords
        stopwords = nltk.corpus.stopwords.words('portuguese')

        text_tokens = nltk.word_tokenize(text)
        tokens_without_sw = [word for word in text_tokens if not word in stopwords]

        #print(tokens_without_sw)

        #extract the sentences from the text
        sentences = nltk.sent_tokenize(text)
        #remove stopwords from the sentences
        sentences_without_sw = []
        for sentence in sentences:
            sentence_tokens = nltk.word_tokenize(sentence)
            sentence_without_sw = [word for word in sentence_tokens if not word in stopwords]
            sentences_without_sw.append(sentence_without_sw)
            #s contains the sentences without stopwords in a list
            s = [' '.join(sentence_without_sw) for sentence_without_sw in sentences_without_sw]
            
        for sentence in s:
            # Load the English spaCy model
            #nlp = spacy.load("en_core_web_sm")

            # Process the text with spaCy
            #doc = nlp(text)
            
            response = requests.get(ESCO_API_ENDPOINT + "?text=" + sentence + "&language=" + ESCO_API_LANG + "&type=occupation&type=skill&type=concept&facet=type&facet=isInScheme&full=true")
            # Check if the request was successful
            if response.status_code != 200:
                print("Error fetching data from API")
            else:
                # Extract the data from the response
                data = response.json()
                # Print the matches and their positions in the text
                print("Sentence: " + sentence)
                for match in data["_embedded"]["results"]:
                    print("ESCO: ",f"{match['preferredLabel']['en']}")

            #wait to press a key
            input("Press Enter to continue...")
            time.sleep(1)
            



