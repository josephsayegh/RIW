import re
import pickle
import itertools


class NotInDictionaryError(Exception):
    pass
class NotInCollectionError(Exception):
    pass

def clean_request(request):
    """
    les operateurs sont definis tq " " = AND, "_" = OR et "!" = NOT
    cette fonction tranforme une requete en un dictionnaire selon les operateurs
    """
    cleaned_request = {"and_list":[], "or_list": [], "not_list": []}
    request = request.split(" ")
    for term in request:
        if "_" in term:
            term = term.split("_")
            cleaned_request['or_list'] += term
        elif "!" in term:
            term = re.sub('!', '', term)
            cleaned_request['not_list'].append(term)
        else:
            cleaned_request['and_list'].append(term)
    return cleaned_request

def recherche_dans_cleaned_request(cleaned_request):
    """
    fonction qui mange le dictionnaire de la fonction d'avant et qui donne la liste de docs qui correspondent
    """
    and_list = cleaned_request['and_list']
    and_dic = recherche(and_list)
    and_result = pre_intersect(and_dic)
    and_result = intersect_many(and_result)
    # pour avoir une liste de tous les documents qui contiennent les termes en "and"
    not_list = cleaned_request['not_list']
    not_dic = recherche(not_list)
    not_result = pre_intersect(not_dic)
    not_result = union_many(not_result)
    # pour avoir une liste de tous les documents qui contiennent au moins un des termes en "not"
    or_list = cleaned_request['or_list']
    or_dic = recherche(or_list)
    or_result = pre_intersect(or_dic)
    or_result = union_many(or_result)
    # pour avoir une liste de tous les documents qui contiennent au moins un des termes en "or"
    
    joined = intersect(and_result, or_result)
    joined.sort()
    cleaned = list(set(joined) - set(not_result))
    cleaned.sort()
    return cleaned

def find_term_id(term):
    """
    fonction qui mange un term et rend son term_id dans la collection
    """
    with open('terms_dictionary', 'rb') as terms_dictionary:
        terms_dictionary = pickle.load(terms_dictionary)
        try:
            term_id = terms_dictionary[term]
        except KeyError:
            #raise NotInDictionaryError('The term {} is not in our dictionary'.format(term))
            #term_id = 'not in dictionary'
            term_id = ""
    return term_id

def get_posting(term_id):
    """
    fonction qui mange un term_id et qui donne retourne un dictionaire des {doc_id: occurences}
    """
    with open('inversed_index', 'rb') as inversed_index:
        inversed_index = pickle.load(inversed_index)
        try:
            term_posting = inversed_index[term_id]
        except KeyError:
            #raise NotInCollectionError('The term {} is not in the collection'.format(term_id))
            #term_posting = 'not in collection'
            term_posting = ""
    return term_posting

def intersect(list_1, list_2):
    """
    fonction qui mange 2 listes tries et qui donne une liste representant 
    l'intersection des 2 listes
    IL FAUT TRIER LES LISTES AVANT
    """
    intersection = []
    while len(list_1) != 0 and len(list_2) != 0:
        if list_1[0] == list_2[0]:
            intersection.append(list_1[0])
            list_1 = list_1[1:]
            list_2 = list_2[1:]
        elif list_1[0] < list_2[0]:
            list_1 = list_1[1:]
        else:
            list_2 = list_2[1:]
    return intersection

def pre_intersect(words_postings_dic):
    """
    fonction qui mange un dictionnaire de {mot:[doc_ids qui le contiennent]}
    et qui donne les listes de docs_ids
    """
    doc_ids = []
    for word, posting in words_postings_dic.items():
        doc_ids.append(posting)
    return doc_ids

def intersect_many(list_of_lists):
    """
    fonction qui applique intersect a une liste de liste, 2 a 2
    """
    while len(list_of_lists) > 1:
        list_of_lists[1] = intersect(list_of_lists[0], list_of_lists[1])
        list_of_lists.pop(0)
    try:
        return list_of_lists[0]
    except IndexError:
        return []

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b)) 

def union_many(list_of_lists):
    """
    fonction qui applique union a une liste de liste, 2 a 2
    """
    while len(list_of_lists) > 1:
        list_of_lists[1] = union(list_of_lists[0], list_of_lists[1])
        list_of_lists.pop(0)
    try:
        return list_of_lists[0]
    except IndexError:
        return []

def recherche(words_list):
    """
    fonction qui mange une liste de mots et qui
    donne un dictionnaire {mot: [doc_ids qui le contiennent]}
    """
    result = {}
    for word in words_list:
        term_id = find_term_id(word)
        posting = get_posting(term_id)
        doc_ids = []
        try:
            for doc_id in posting.keys():
                doc_ids.append(doc_id)
            result[word] = doc_ids
        except AttributeError:
            pass
    return result