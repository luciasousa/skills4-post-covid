import pandas as pd
import nltk
from bs4 import BeautifulSoup
import requests
import re
from deep_translator import GoogleTranslator

# Read the Excel file into a DataFrame
file = "../../DPUC_2021_2022.xlsx"
df = pd.read_excel(file)

# Define the ESCO API endpoint and language
ESCO_API_ENDPOINT = "http://localhost:8080/search"
ESCO_API_LANG = "en"

# Filter rows where NomeUC starts with specific prefixes
filtered_df = df[df['NomeUC'].str.startswith(("INTRODUÇÃO À ENGENHARIA", "PROJETO EM ENGENHARIA"))]
# Get only the rows where Campo is "Conteudos", "Metodologias", or "Objetivos"
filtered_df = filtered_df[filtered_df['Campo'].isin(["Conteudos", "Metodologias", "Objetivos"])]

stopwords_en = nltk.corpus.stopwords.words('english')

# Remove HTLM tags and extract text content
columns_to_extract = ['NomeUC', 'Campo', 'TextoEN']

# Define a function to remove HTML tags from a cell
def remove_html_tags(text):
    if isinstance(text, str):
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text()
    else:
        return text
    

# Apply the remove_html_tags function to the specified columns
for col in columns_to_extract:
    filtered_df[col] = filtered_df[col].apply(remove_html_tags)

# Create a dictionary to store tokenized texts for each NomeUC
tokenized_texts = {}

for index, row in filtered_df.iterrows():
    nome = row['NomeUC']
    campo = row['Campo']
    if nome not in tokenized_texts:
        tokenized_texts[nome] = {'Conteudos': [], 'Metodologias': [], 'Objetivos': []}
    # Convert all column values to strings and then join
    row_text = ' '.join(map(str, row[columns_to_extract]))
    tokenized_text = nltk.word_tokenize(row_text)  # Tokenize the combined text
    tokenized_texts[nome][campo].extend(tokenized_text)

# Create a DataFrame to store skills
skills_df = pd.DataFrame(columns=['Nome_UC', 'Skills'])  # Create an empty DataFrame

# Print Nome_UC and corresponding tokenized text for each row
for nome, tokenized_text_dict in tokenized_texts.items():
    #print(nome)
    skills = []
    for campo, tokenized_text in tokenized_text_dict.items():
        sentence = ' '.join([re.sub(r'[^a-zA-Z\s]', '', str(s)) for s in tokenized_text])
        sentence = ' '.join(dict.fromkeys(sentence.split()))

        # Translate the 'nome' to English
        translated_nome = GoogleTranslator(source='auto', target='en').translate(nome)
        #print(translated_nome)

        response = requests.get(ESCO_API_ENDPOINT + "?text=" + sentence + "&language=" + ESCO_API_LANG +  "&type=skill&facet=type&facet=isInScheme&full=true&q=" + translated_nome)

        # Check if the request was successful
        if response.status_code == 200:
            print(f"results for {campo}")
            # Extract the skills from the API response
            data = response.json()
            for match in data["_embedded"]["results"]:
                skill = match['preferredLabel'][ESCO_API_LANG]
                skills.append(skill)

    # Remove duplicate skills
    unique_skills = list(set(skills))

    # Append Nome_UC and skills to the DataFrame
    skills_paragraph = '\n'.join(unique_skills)  # Combine skills into paragraphs
    skills_df = skills_df.append({'Nome_UC': translated_nome, 'Skills': skills_paragraph}, ignore_index=True)

# Save skills to an Excel file
skills_df.to_excel('skills_output.xlsx', index=False)