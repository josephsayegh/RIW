import re
import os
from nltk.tokenize import RegexpTokenizer

def parse(file):
    """
    fonction qui parse query.text en prenant uniquement les sections
    qui nous intéressent
    """
    with open(file, 'r') as requetes:
        newpath = r'./Requetes'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        documents_pattern = re.compile("^.I[ ][0-9]{1,4}[\n]$")
        sections_pattern = re.compile("^.[A-Z]?[\n]$")
        # les sections qui nous intéressent
        interesting_sections = re.compile("^.[KWT]?[\n]$")
        collection = open('I0', 'w') # sert uniquement à fermer un fichier à la fin de la première boucle
        for line in requetes:
            if documents_pattern.match(line) is not None:
                title = re.sub('[.\n]', '', line)
                collection.close() # fermeture du fichier précedemment ouvert
                filepath = os.path.join(newpath, title)
                collection = open(filepath, 'w')
            elif sections_pattern.match(line) is not None:
                # pour savoir dans quelle section nous sommes
                line_section = line
            elif interesting_sections.match(line_section):
                # Lorsque nous somme dans une des sections intéressantes KWZ, on écrit dans le document
                # transformer la liste en phrase
                collection.write(line.replace("\n","") + " ")
        collection.close()

if __name__ == "__main__":
    parse("query.text")