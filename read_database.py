import pandas

file = "../DPUC_2021_2022.xlsx"

cols = ['CodUC', 'NomeUC', 'Ano', 'Semestre', 'Estado', 'Campo', 'TextoPT', 'TextoEN']

db = pandas.read_excel(file, usecols=cols)


