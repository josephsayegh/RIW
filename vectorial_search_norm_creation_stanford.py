import re
import os
import pickle
import math
import ast
import boolean_research_functions_stanford as br


"""
Ce document permet le stockage dans un document à part de toutes les nomres de tous les documents. Ceci économise du temps
de calcul pour la recherche vectorielle.
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
        line = inversed_index.readline().strip()
        for document in range(1, 99005):
            w.append(0)
        while line != "":
            posting_list = line.split("|")
            dico = ast.literal_eval(posting_list[1])
            for doc, doc_appearances in dico.items():
                dico[doc] = 1 + math.log10(doc_appearances)
            idf[posting_list[0]] = math.log10(99004/len(dico))
            tf[posting_list[0]] = dico
            for doc, doc_appearances in dico.items():
                w[doc-1] += (tf[posting_list[0]][doc] * idf[posting_list[0]]) ** 2
            line = inversed_index.readline().strip()
        for document in range(1, 99005):
            norm[document] = math.sqrt(w[document-1])
    return norm


if __name__ == "__main__":

    norms = norm_build()
    
    with open('Stanford/documents_norms', 'wb') as stanford_documents_norms:
        pickle.dump(norms, stanford_documents_norms, protocol=pickle.HIGHEST_PROTOCOL)