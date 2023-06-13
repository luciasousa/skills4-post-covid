import pandas as pd
from bs4 import BeautifulSoup

file = "../DPUC_2021_2022.xlsx"

cols = ['CodUC', 'NomeUC', 'Ano', 'Semestre', 'Estado', 'Campo', 'TextoPT', 'TextoEN']

db = pd.read_excel(file, usecols=cols)

filtered_db = db.loc[db['NomeUC'].isin(['INTRODUÇÃO À ENGENHARIA COMPUTACIONAL'])].copy()

# Remove HTML tags and extract text content
filtered_db.loc[:, 'TextoPT'] = filtered_db['TextoPT'].apply(lambda x: BeautifulSoup(x, 'html.parser').get_text() if isinstance(x, str) else x)
filtered_db.loc[:, 'TextoEN'] = filtered_db['TextoEN'].apply(lambda x: BeautifulSoup(x, 'html.parser').get_text() if isinstance(x, str) else x)

filtered_db.to_excel('introducao_eC.xlsx', index=False)
