import pandas as pd
import nltk
from bs4 import BeautifulSoup
import requests
import re

# Read the Excel file into a DataFrame
file = "ucs_projeto_en.xlsx"
df = pd.read_excel(file)

# Get the column names from the DataFrame
column_names = df.columns.tolist()

# Define the ESCO API endpoint and language
ESCO_API_ENDPOINT = "http://localhost:8080/search"
ESCO_API_LANG = "en"

db = pd.read_excel(file)

# Get table with UC Names and Skills
# 'Nome_EN', 'Objetivos_EN', 'Conteudos_EN', 'Avaliacao_EN', 'Requisitos_EN', 'Metodologia_EN', 'BibliografiaBase_EN', 'Bibliografia_EN', 'Competencias_EN', 'Caraterizacao_EN'

stopwords_en = nltk.corpus.stopwords.words('english')

# Remove HTLM tags and extract text content
columns_to_extract = ['Nome_EN', 'Objetivos_EN', 'Conteudos_EN', 'Avaliacao_EN', 'Requisitos_EN', 'Metodologia_EN', 'Competencias_EN', 'Caraterizacao_EN']

# Define a function to remove HTML tags from a cell
def remove_html_tags(text):
    if isinstance(text, str):
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text()
    else:
        return text
    

# Apply the remove_html_tags function to the specified columns
for col in columns_to_extract:
    df[col] = df[col].apply(remove_html_tags)

# Create a list of tokenized words for each row
tokenized_texts = []

for index, row in df.iterrows():
    # Convert all column values to strings and then join
    row_text = ' '.join(map(str, row[columns_to_extract]))
    tokenized_text = nltk.word_tokenize(row_text)  # Tokenize the combined text
    tokenized_texts.append((row['Nome_EN'], tokenized_text))  # Store Nome_EN and tokenized text

# Print Nome_EN and corresponding tokenized text for each row
for nome, tokenized_text in tokenized_texts:
    skills = []
    sentence = ' '.join([re.sub(r'[^a-zA-Z\s]', '', str(s)) for s in tokenized_text])
    sentence = ' '.join(dict.fromkeys(sentence.split()))
    print(f"{nome}: {sentence}\n")

    response = requests.get(ESCO_API_ENDPOINT + "?text=" + sentence + "&language=" + ESCO_API_LANG +  "&type=skill&facet=type&facet=isInScheme&full=true&q=computer%20engineering")

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching data from API for {nome}")
    else:
        # Extract the data from the response
        data = response.json()
        # Print the matches and their positions in the text
        for match in data["_embedded"]["results"]:
            skill = match['preferredLabel'][ESCO_API_LANG]
            skills.append(skill)

        # Save skills to a file with a name corresponding to the Nome_EN
        with open(f"{nome}_skills.txt", "w") as f:
            f.write('\n'.join(skills))
