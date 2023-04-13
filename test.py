import time
from pprint import pprint
import nltk
nltk.download('punkt')
import spacy
from sklearn.feature_extraction.text import CountVectorizer
import requests
import json
import textract

# Define the ESCO API endpoint and language
ESCO_API_ENDPOINT = "http://localhost:8080/search"
ESCO_API_LANG = "en"

file_name = "../fichas_UCs_MEET/Uc_DEGEIT/DPUC_47121_2017-2018_v1_pt.pdf"

# Load the Portuguese spaCy model
nlp = spacy.load("en_core_web_sm")

# Read the text file and convert to a string
text = textract.process(file_name, method='pdfminer').decode('utf-8')

#print(text)

# Process the text with spaCy
doc = nlp(text)

print(doc)

# Extract the lemma for each token in the text
lemmas = [token.lemma_ for token in doc]

print(lemmas)

# Define the request parameters
params = {
    "text": text,   # The text to search for
    "language": ESCO_API_LANG,  # The language of the text
    #"type": "occupation",  # The type of concepts to search for
    "full": "true"  # Return the full concept details
}

skills = []
start = 0
stop = 0

# Send the request to the ESCO API
for i in lemmas:
    if i == "classificação":
        stop = 1
        break
    
    if i == "aprendizagem":
        start = 1
    
    if start == 1:
        skills.append(i)

for i in skills:

    response = requests.get(ESCO_API_ENDPOINT + "?text=" + i + "&language=" + ESCO_API_LANG + "&type=occupation&type=skill&type=concept&facet=type&facet=isInScheme&full=true")
    # Check if the request was successful
    if response.status_code != 200:
        print("Error fetching data from API")
    else:
        # Extract the data from the response
        data = response.json()
        # Print the matches and their positions in the text
        print("Lemma: " + i)
        for match in data["_embedded"]["results"]:
            print("ESCO: ",f"{match['preferredLabel']['pt']}")