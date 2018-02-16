import re
import os
import pickle
import math
import ast
import boolean_research_functions_stanford as br
from nltk.tokenize import RegexpTokenizer
import filemapper as fm
from stanford_index_creator import read_document

"""
ATTENTION, script très très long à compiler.
"""


def get_terms_in_document(doc_id):
    """
    crée la liste des term_id contenus dans le doc relatif au doc_id
    """
    doc = br.find_document_from_docid([doc_id],'Stanford_indexes/doc_id_dictionary')
    terms_in_doc = []
    with open(doc[0], 'r') as document:
        terms_in_doc = document.read().split()
        terms_in_doc = list(set(terms_in_doc))
    return terms_in_doc



def norm_build():
    """
    crée une liste contenant les normes de chaque document à partir de l'index inversé.
    Celle-ci sera utile pour optimiser la recherche vectorielle.
    """
    line = "line"
    with open('Stanford_indexes/final_index', 'r') as inversed_index:
        tf = {}
        idf = {}
        w = []
        norm = {}
        vocabulary = []
        line = inversed_index.readline().strip()
        while line != "":
            posting_list = line.split("|")
            vocabulary.append(posting_list[0])
            for doc, doc_appearances in ast.literal_eval(posting_list[1]).items():
                tf[posting_list[0]] = (doc, 1 + math.log10(doc_appearances))
                idf[posting_list[0]] = math.log10(99004/len(posting_list[1]))
            line = inversed_index.readline().strip()
        for document in range(1, 99005):
            w.append(0)
            for term in get_terms_in_document(document):
                if term in vocabulary:
                    w[document-1] += (tf[term][1] * idf[term]) ** 2
            norm[document] = math.sqrt(w[document-1])
    return norm


if __name__ == "__main__":

    norms2 = norm_build()
    
    with open('Stanford/documents_norms', 'wb') as stanford_documents_norms:
        pickle.dump(norms2, stanford_documents_norms, protocol=pickle.HIGHEST_PROTOCOL)