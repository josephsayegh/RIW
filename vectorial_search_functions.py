import os
import pickle
import math
from nltk.tokenize import RegexpTokenizer
from boolean_research_functions_cacm import find_term_id
import time


class NotInDictionaryError(Exception):
    pass
class NotInCollectionError(Exception):
    pass

def open_inversed_index(inversed_index):
    with open(inversed_index, 'rb') as inversed_index:
        inversed_index = pickle.load(inversed_index)
    return inversed_index

inversed_index = open_inversed_index("CACM/inversed_index")

collection_length = len(os.listdir("CACM/Collection"))

def query_indexation(query):
    """fonction qui transforme la requête en un index, comme les documents"""
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


def vectorial_search(query, nb_of_results):
    """fonction qui sort la liste des 5 documents les plus similaires à une requête
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
        for j in range(1, collection_length + 2):
            scores.append(0)                 #on met tous les scores à zéro
        for term in refined_query:
            w.append(weight_term_frequency_in_collection(term) * (1 + math.log10(refined_query[term])))   # création du poids du ième terme de la requête
            nq += w[i] * w[i]
            if term in inversed_index:
                L = inversed_index[term]
            else:
                L = ""
            for j in L:
                scores[j] += total_weight(term, j) * w[i]
            i += 1
        for j in range(1, collection_length):
            if (norms[j] != 0) & (nq != 0):
                scores[j] = scores[j] / (math.sqrt(nq) * norms[j])
                scores_tuples.append((j, scores[j]))
        if max(scores) == 0:
            return "Sorry, no document matches your query"
        scores_tuples = sorted(scores_tuples, key=lambda colonnes: colonnes[1], reverse=True)
        for k in range(nb_of_results):
            sorted_scores[k] = (scores_tuples[k][0], round(scores_tuples[k][1],2))
    return sorted_scores


def weight_term_frequency_in_doc(term_id, doc_id):
    """fonction qui calcule le poids d'un terme dans un doc"""
    result = 0
    try:
        L = inversed_index[term_id]
    except KeyError:
        L = ""
    if doc_id in L:
        result = 1 + math.log10(int(L[doc_id]))
    return result

def weight_term_frequency_in_collection(term_id):
    """fonction qui calcule le poids d'un terme dans la collection"""
    try:
        L = inversed_index[term_id]
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




if __name__ == "__main__":
    requete = input("Tappez votre requete: ")
    start_time = time.time()
    result = vectorial_search(requete, 5)
    print(result)
    end_time = time.time()
    total_time = end_time - start_time
    print(total_time)