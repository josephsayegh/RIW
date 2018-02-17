import os
import pickle
import math
from nltk.tokenize import RegexpTokenizer
import time
import ast
from boolean_research_functions_stanford import find_document_from_docid


class NotInDictionaryError(Exception):
    pass
class NotInCollectionError(Exception):
    pass

def open_inversed_index(inversed_index):
    with open(inversed_index, 'rb') as inversed_index:
        index = inversed_index
    return index

def open_norms():
    with open("Stanford/documents_norms", 'rb') as norms:
        norms = pickle.load(norms)
    return norms

norms = open_norms()
inversed_index = open_inversed_index("Stanford_indexes/final_index")
collection_length = 99004

def get_posting_stanford(term_id):
    """
    fonction qui prend en entrée un mot
    et qui donne un dictionaire des {doc_id: occurences}
    """
    term_posting = dict({})
    line = "line"
    with open("Stanford_indexes/final_index", 'r') as inversed_index:
        line = inversed_index.readline().strip()
        while term_posting == {} and line != "":
            posting_list = line.split("|")
            if posting_list[0] == term_id:
                term_posting = ast.literal_eval(posting_list[1])
            else:
                line = inversed_index.readline().strip()
    return term_posting

def query_indexation(query):
    """fonction qui transforme la requête en un index, comme les documents"""
    result = {}
    tokenizer = RegexpTokenizer(r'\w+')
    query = tokenizer.tokenize(query.lower())
    id = 1
    for word in query:
        try:
            result[word] += 1
        except KeyError:
            result[word] = 1
        id += 1
    return result


def vectorial_search(query, nb_of_results):
    """fonction qui sort la liste des 5 documents les plus similaires à une requête
    c'est l'algo du cours. Il est un peu compliqué à lire en conséquence."""
    nq = 0         #c'est le nq du cours, qui va être égal à la norme au carré du vecteur requête
    w = []         #liste w contenant les poids de chaque terme de la requête
    i = 0          #indice pour repérer le terme de la requête
    scores = []    #liste des scores de chaque doc de la collection
    sorted_scores = {}      #ce qu'il faudra retourner: la liste des 5 résultats les plus pertinents
    scores_tuples = []      #liste des tuples (doc_id, score), de la taille de scores
    refined_query = query_indexation(query)   #requête retraitée comme un index
    for j in range(1, collection_length + 2):
        scores.append(0)                 #on met tous les scores à zéro
    for term in refined_query:
        w.append(weight_term_frequency_in_collection(term) * (1 + math.log10(refined_query[term])))   # création du poids du ième terme de la requête
        nq += w[i] * w[i]
        L = get_posting_stanford(term)
        for j in L:
            if len(L) > 0:
                scores[j] += (1 + math.log10(int(L[j]))) * (math.log10(collection_length/len(L)))
        i += 1
    for j in range(1, collection_length):
        if (norms[j] != 0) & (nq != 0):
            scores[j] = scores[j] / (math.sqrt(nq) * norms[j])
            scores_tuples.append((j, scores[j]))
    if max(scores) == 0:
        return {}
    scores_tuples = sorted(scores_tuples, key=lambda colonnes: colonnes[1], reverse=True)
    for k in range(nb_of_results):
        sorted_scores[k] = (find_document_from_docid([scores_tuples[k][0]],'Stanford_indexes/doc_id_dictionary')[0], round(scores_tuples[k][1],2))
    return sorted_scores


def weight_term_frequency_in_doc(term_id, doc_id):
    """fonction qui calcule le poids d'un terme dans un doc"""
    result = 0
    try:
        L = get_posting_stanford(term_id)
    except KeyError:
        L = ""
    if doc_id in L:
        result = 1 + math.log10(int(L[doc_id]))
    return result

def weight_term_frequency_in_collection(term_id):
    """fonction qui calcule le poids d'un terme dans la collection"""
    try:
        L = get_posting_stanford(term_id)
    except KeyError:
        L = ""
    docs_containing_term = len(L)
    if docs_containing_term > 0:
        return math.log10(collection_length/docs_containing_term)
    else:
        return 0

def total_weight(term_id, doc_id):
    """fonction qui calcule le poids total en multipliant les deux poids précédents"""
    return (weight_term_frequency_in_doc(term_id, doc_id) * weight_term_frequency_in_collection(term_id))


#print(query_indexation("analysis"))

if __name__ == "__main__":
    requete = input("Tappez votre requete: ")
    start_time = time.time()
    result = vectorial_search(requete, 5)
    print(result)
    end_time = time.time()
    total_time = end_time - start_time
    print(total_time)