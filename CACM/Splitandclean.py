"""
Ce fichier permet de parcourir le fichier CACM et le splitter en fichiers par document.
Nous prenons uniquement les sections qui nous intéressent.
Les mots sont comparés aux stopwords et tokenizés avant d'être stockés
"""

import re
import os
from nltk.tokenize import RegexpTokenizer

def parse(file):
    """
    fonction qui parse cacm.all en prenant uniquement les sections
    qui nous intéressent
    """
    with open(file, 'r') as cacm:
        newpath = r'./Collection'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        documents_pattern = re.compile("^.I[ ][0-9]{1,4}[\n]$")
        sections_pattern = re.compile("^.[A-Z]?[\n]$")
        # les sections qui nous intéressent
        interesting_sections = re.compile("^.[KWT]?[\n]$")
        collection = open('I0', 'w') # sert uniquement à fermer un fichier à la fin de la première boucle
        for line in cacm:
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
                line = stopwords(line)
                # transformer la liste en phrase
                collection.write(line + " ")
        collection.close()   


def stopwords(line):
    """
    fonction qui prend un entree une ligne de mots et qui
    la compare a common_words pour enlever les mots qui sont
    dans common_words de la ligne
    """
    tokenizer = RegexpTokenizer(r'\w+')
    with open("common_words", "r") as common_words:
        common_list = []
        for word in common_words:
            word = re.sub('[.\n]', '', word)
            common_list.append(word)
    line_list = tokenizer.tokenize(line)
    line_list = [word.lower() for word in line_list]
    cleaned_list = list(set(line_list)-set(common_list))
    line = " ".join(cleaned_list)
    return line

if __name__ == "__main__":
    parsed = parse("cacm.all")
