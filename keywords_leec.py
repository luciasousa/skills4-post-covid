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
import matplotlib.pyplot as plt
import numpy as np

def get_skill_hierarchy(skill_uri):
    response = requests.get(skill_uri, headers={"Accept": "application/json"})
    if response.status_code == 200:
        skill_hierarchy = json.loads(response.text)
        return skill_hierarchy
    else:
        return None

# Define the ESCO API endpoint and language
ESCO_API_ENDPOINT = "http://localhost:8080/search"
ESCO_API_LANG = "en"

#read all .doc files from a folder
path = "../leec/en/"
files = os.listdir(path)

nltk.download('punkt')
nltk.download('stopwords')
skills = []


s = "gain acquaintance with professional activities in the field of Electrical Engineering; identify the role and mission of the Engineer, main electrical quantities; analyze simple circuits. International System of Units; properly use measuring devices and other bench equipment. know basic electronic components; read schematic drawings; assemble and test simple circuits; develop simple programs to run in a microcontroller. design simples electronic circuits. write technical and scientific texts. The activity of Engineering. Fundamental concepts of electrical circuits. Ohm's and Kirchhoff's law. nodal and mesh analysis. Voltage/current equations in the capacitor and inductor.Measures and equipment. Metrology concepts. Multimeter and oscilloscope. Voltage sources and signal generator. Simple electronic circuits with sensors and actuators. Programming simple microcontroller platforms.Writing technical and scientific texts. Technical and scientific text."
#s= "- Strengthening the ability to work as a team.- Strengthening cross-cutting skills for organizing ideas up to their presentation.- Familiarization with the basic principles of the management of electronic engineering and telecommunications projects.- Identification of problems and opportunities, requirements analysis, modelling, hypothesis formulation, solution identification and evaluation, development and implementation planning, testing and documentation.- Awareness raising for the ethical dimension of the engineering profession and for some of its social implications.- Concept of Engineering Project.- Main methodological aspects of the Engineering Project:- Identification of opportunities / needs.- Identification of possible solutions.Evaluation of solutions:- Technical evaluation; Economic evaluation.Planning the implementation of projects.Operationalization.Preparation of a group report on the proposed theme."

print("with stopwords: ",s)

#remove stopwords
stopwords = nltk.corpus.stopwords.words('english')
remove_chars = ['.', ',', '-', ';', ':', '–']

# Tokenize the text
text_tokens = nltk.word_tokenize(s)

# Remove the stopwords and characters to remove
tokens_without_sw = [word for word in text_tokens if not word in stopwords and not word in remove_chars]



# Join the tokens back into a string
sf = ' '.join(tokens_without_sw)

print("no stopwords: ",sf)
# Create an empty list to store the sentences
target_sentences = []

#target_sentences.append("Professional activities – gain acquaintance with professional activities in the field of Electrical Engineering and learn how they fit in the economic and social fabric; identify the role and mission of the Engineer in these activities")
#target_sentences.append("Operationalization")
    
'''
#para Introdução à engenharia eletrotecnica
target_sentences.append("Professional activities – gain acquaintance with professional activities in the field of Electrical Engineering and learn how they fit in the economic and social fabric; identify the role and mission of the Engineer in these activities")
target_sentences.append("Electrical circuit - know and relate to each other the main electrical quantities; analyze simple circuits.")
target_sentences.append("Measures and equipment - know and apply the concepts of metrology and International System of Units (SI); properly use measuring devices and other bench equipment.")
target_sentences.append("Electronic circuits - know basic electronic components; read schematic drawings; assemble and test simple circuits; develop simple programs to run in a microcontroller.")
target_sentences.append("Electronic projects - design simples electronic circuits.")
target_sentences.append("Writing technical and scientific texts - know how to perform an academic literature search; write technical and scientific texts; hold public presentations of technical or scientific work.")

target_sentences.append("The activity of Engineering. The role of the Engineer; specific cases.")
target_sentences.append("Fundamental concepts of electrical circuits. Ohm's and Kirchhoff's law.")
target_sentences.append("Circuit analysis: nodal and mesh analysis.")
target_sentences.append("Voltage/current equations in the capacitor and inductor")
target_sentences.append("Metrology concepts. International System of Units (SI). Error.")
target_sentences.append("Multimeter and oscilloscope. Voltage sources and signal generator.")
target_sentences.append("Simple electronic circuits with sensors and actuators.")
target_sentences.append("Programming simple microcontroller platforms.")
target_sentences.append("Sources of information and bibliographic research.")
target_sentences.append("Technical and scientific text. Citations and references.")
target_sentences.append("Presentations of works.")
'''

#target_sentences.append("Professional activities. Gain acquaintance with professional activities in the field of Electrical Engineering and learn how they fit in the economic and social fabric. Identify the role and mission of the Engineer in these activities. Electrical circuit. Know and relate to each other the main electrical quantities. Analyze simple circuits. Measures and equipment. Know and apply the concepts of metrology and International System of Units (SI). Properly use measuring devices and other bench equipment. Electronic circuits. Know basic electronic components. Read schematic drawings. Assemble and test simple circuits. Develop simple programs to run in a microcontroller. Electronic projects. Design simples electronic circuits.Writing technical and scientific texts.")
#target_sentences.append("Professional activities. The activity of Engineering. The role of the Engineer; specific cases. Electric circuit. Fundamental concepts of electrical circuits. Ohm's and Kirchhoff's law. Circuit analysis: nodal and mesh analysis. Voltage/current equations in the capacitor and inductor. Measures and equipment. Metrology concepts. International System of Units (SI). Error. Multimeter and oscilloscope. Voltage sources and signal generator. Project of electronic circuits. Simple electronic circuits with sensors and actuators. Programming simple microcontroller platforms. Writing technical and scientific texts. Sources of information and bibliographic research. Technical and scientific text. Citations and references. Presentations of works.")

'''
#para o projeto em engenharia eletrotecnica

target_sentences.append("Strengthening the ability to work as a team.")
target_sentences.append("Strengthening cross-cutting skills for organizing ideas up to their presentation")
target_sentences.append("Familiarization with the basic principles of the management of electronic engineering and telecommunications projects")
target_sentences.append("Identification of problems and opportunities, requirements analysis, modelling, hypothesis formulation, solution identification and evaluation, development and implementation planning, testing and documentation.")
target_sentences.append("Awareness raising for the ethical dimension of the engineering profession and for some of its social implications.")

target_sentences.append("Concept of Engineering Project.")
target_sentences.append("Identification of opportunities / needs.")
target_sentences.append("Identification of possible solutions.")
target_sentences.append("Technical evaluation; Economic evaluation.")
target_sentences.append("Planning the implementation of projects.")
target_sentences.append("Operationalization.")
target_sentences.append("Preparation of a group report on the proposed theme.")
'''

    
#target_sentences.append("Strengthening the ability to work as a team. Strengthening cross-cutting skills for organizing ideas up to their presentation. Familiarization with the basic principles of the management of electronic engineering and telecommunications projects. Identification of problems and opportunities, requirements analysis, modelling, hypothesis formulation, solution identification and evaluation, development and implementation planning, testing and documentation. Awareness raising for the ethical dimension of the engineering profession and for some of its social implications.")
#target_sentences.append("Overview of Engineering Project activity: Concept of Engineering Project. Main methodological aspects of the Engineering Project: Identification of opportunities / needs. Identification of possible solutions.Evaluation of solutions: Technical evaluation; Economic evaluation.Planning the implementation of projects.Operationalization.Preparation of a group report on the proposed theme.")

target_sentences.append(sf)

for sentence in target_sentences:
    # Load the English spaCy model
    #nlp = spacy.load("en_core_web_sm")

    # Process the text with spaCy
    #doc = nlp(text)
    
    #just skills
    response = requests.get(ESCO_API_ENDPOINT + "?text=" + sentence + "&language=" + ESCO_API_LANG + "&related=levels" + "&type=skill&facet=type&facet=isInScheme&full=true")
    # Check if the request was successful
    
    if response.status_code != 200:
        print("Error fetching data from API")
    else:
        # Extract the data from the response
        data = response.json()
        
        # Print the matches and their positions in the text
        print("Sentence: " + sentence)
        for match in data["_embedded"]["results"]:
            skill = match['preferredLabel'][ESCO_API_LANG]
            skills.append(skill)
            print("ESCO: ",f"{match['preferredLabel']['en']}")

   
#print("Skills for EET: ", skills)

skills =["3D animator"]

for skill in skills:
    skill_uri = ESCO_API_ENDPOINT + "?uri=" + skill + "&language=" + ESCO_API_LANG
    skill_hierarchy = get_skill_hierarchy(skill_uri)
    response = requests.get(skill_uri)

    if response.status_code != 200:
        print("Error fetching data from API")
    else:
        # Extract the data from the response
        data = response.json()
        print("skill: ", skill)
        for match in data["_embedded"]["results"]:
            broader_skills = match['preferredLabel'][ESCO_API_LANG]
            print("ESCO: ",f"{match['preferredLabel']['en']}")


#TODO 

#getSkillByConceptScheme
#Get skills - by Concept Scheme
#Get a collection of resources of class Skill by the universal identifier

#use "eletronic engineering" to filter

