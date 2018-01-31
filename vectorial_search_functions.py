import re
import os
import pickle
import itertools
import math
from nltk.tokenize import RegexpTokenizer
import filemapper as fm
import ast
from boolean_research_functions_cacm import find_term_id, get_posting


class NotInDictionaryError(Exception):
    pass
class NotInCollectionError(Exception):
    pass



def query_indexation(query):
    """fonction qui transforme la requête en un indexe, comme les documents"""
    result = {}
    result2 = {}
    tokenizer = RegexpTokenizer(r'\w+')
    query = tokenizer.tokenize(query.lower())
    id = 1
    for word in query:
        try:
            result[word] += 1
        except KeyError:
            result[word] = 1
        id += 1
    for word in result:
        word2 = word
        word = find_term_id(word, 'CACM/terms_dictionary')
        result2[word] = result[word2]
    return result2



def vectorial_search(query, inversed_index, collection):
    """fonction qui sort la liste des 10 documents les plus similaires à une requête
    c'est l'algo du cours. Il est un peu compliqué à lire en conséquence."""
    with open("CACM/documents_norms", 'rb') as norms:
        norms = pickle.load(norms)       #liste des normes de chaque doc de la collection
        nq = 0         #c'est le nq du cours, qui va être égal à la norme au carré du vecteur requête
        w = []         #liste w contenant les poids de chaque terme de la requête
        i = 0          #indice pour repérer le terme de la requête
        scores = []    #liste des scores de chaque doc de la collection
        sorted_scores = {}      #ce qu'il faudra retourner: la liste des 5 résultats les plus pertinents
        scores_tuples = []      #liste des tuples (doc_id, score), de la taille de scores
        refined_query = query_indexation(query)   #requête retraitée comme un index
        for j in range(1, len(os.listdir(collection)) + 2):
            scores.append(0)                 #on met tous les scores à zéro
        for term in refined_query:
            w.append(weight_term_frequency_in_collection(term, inversed_index, collection) * (1 + math.log10(refined_query[term])))   # création du poids du ième terme de la requête
            nq += w[i] * w[i]
            if term in open_inversed_index(inversed_index):
                L = open_inversed_index(inversed_index)[term]
            else:
                L = ""
            for j in L:
                scores[j] += total_weight(term, j, inversed_index, collection) * w[i]
            i += 1
        for j in range(1, len(os.listdir(collection))):
            if norms[j] != 0:
                scores[j] = scores[j] / (math.sqrt(nq) * math.sqrt(norms[j]))
                scores_tuples.append((j, scores[j]))
        if max(scores) == 0:
            return "Sorry, no document matches your query"
        scores_tuples = sorted(scores_tuples, key=lambda colonnes: colonnes[1], reverse=True)
        for k in range(5):
            sorted_scores[k] = (scores_tuples[k][0], round(scores_tuples[k][1],2))
    return sorted_scores


def open_inversed_index(inversed_index):
    with open(inversed_index, 'rb') as inversed_index:
        inversed_index = pickle.load(inversed_index)
    return inversed_index


def weight_term_frequency_in_doc(term_id, doc_id, inversed_index):
    """fonction qui calcule le poids d'un terme dans un doc"""
    result = 0
    try:
        L = get_posting(term_id, inversed_index)
    except KeyError:
        L = ""
    if doc_id in L:
        result = 1 + math.log10(int(L[doc_id]))
    return result

def weight_term_frequency_in_collection(term_id, inversed_index, collection):
    """fonction qui calcule le poids d'un terme dans la collection"""
    collection_length = len(os.listdir(collection))
    try:
        L = get_posting(term_id, inversed_index)
    except KeyError:
        L = ""
    docs_containing_term = len(L)
    if docs_containing_term > 0:
        return math.log10(collection_length/docs_containing_term)
    else:
        return 0

def total_weight(term, doc_id, inversed_index, collection):
    """fonction qui calcule le poids total en multipliant les deux poids précédents"""
    return (weight_term_frequency_in_doc(term, doc_id, inversed_index) * weight_term_frequency_in_collection(term, inversed_index, collection))


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
