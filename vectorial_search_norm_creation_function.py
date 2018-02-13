from vectorial_search_functions import open_inversed_index
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
    for term, term_postings in inversed_index.items():
        for doc, doc_appearances in term_postings.items():
            tf[term] = (doc, 1 + math.log10(doc_appearances))
            idf[term] = math.log10(collection_length/len(term_postings))
    for document in range(1, len(os.listdir(collection)) + 1):
        w.append(0)
        for term in get_terms_in_document(document, inversed_index):
            w[document] += (tf[term][1] * idf[term]) ** 2
        norm[document] = math.sqrt(w[document])
    return norm


if __name__ == "__main__":

    norms = norm_build('CACM/inversed_index','CACM/Collection')
    
    with open('CACM/documents_norms', 'wb') as documents_norms:
        pickle.dump(norms, documents_norms, protocol=pickle.HIGHEST_PROTOCOL)