from vectorial_search_functions_cacm import open_inversed_index
import re
import os
import pickle
import math


def get_terms_in_document(doc_id, inversed_index):
    """
    crée la liste des term_id contenus dans le doc relatif au doc_id
    """
    terms_in_doc = []
    for term_id in inversed_index:
        if doc_id in inversed_index[term_id]:
            terms_in_doc.append(term_id)
    return terms_in_doc



def norm_build(inversed_index, collection):
    """
    crée une liste contenant les normes de chaque document à partir de l'index inversé et de la collection.
    Celle-ci sera utile pour optimiser la recherche vectorielle.
    """
    inversed_index = open_inversed_index(inversed_index)
    collection_length = len(os.listdir(collection))
    tf = {}
    idf = {}
    w = []
    norm = {}
    for term in inversed_index.keys():
        term_postings = inversed_index[term]
        for doc in term_postings.keys():
            doc_appearances = inversed_index[term][doc]
            term_postings[doc] = 1 + math.log10(doc_appearances)
        tf[term] = term_postings
        idf[term] = math.log10(collection_length/len(term_postings))
    for document in range(1, len(os.listdir(collection))):
        w.append(0)
        for term in get_terms_in_document(document, inversed_index):
            w[document-1] += (tf[term][document] * idf[term]) ** 2
        norm[document] = math.sqrt(w[document-1])
    return norm


if __name__ == "__main__":

    norms = norm_build('CACM/inversed_index','CACM/Collection')
    
    with open('CACM/documents_norms', 'wb') as cacm_documents_norms:
        pickle.dump(norms, cacm_documents_norms, protocol=pickle.HIGHEST_PROTOCOL)