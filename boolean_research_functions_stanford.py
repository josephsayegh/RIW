import ast
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

def recherche_dans_cleaned_request(cleaned_request, inversed_index):
    """
    fonction qui prends en entrée le dictionnaire de la fonction d'avant 
    et qui donne la liste de docs qui correspondent
    """
    # pour avoir une liste de tous les documents qui contiennent les termes en "and"
    and_list = cleaned_request['and_list']
    and_dic = recherche_stanford(and_list, inversed_index)
    and_result = pre_intersect(and_dic)
    and_result = intersect_many(and_result)
    and_result.sort()
    # pour avoir une liste de tous les documents qui contiennent au moins un des termes en "not"
    not_list = cleaned_request['not_list']
    not_dic = recherche_stanford(not_list, inversed_index)
    not_result = pre_intersect(not_dic)
    not_result = union_many(not_result)
    not_result.sort()
    # pour avoir une liste de tous les documents qui contiennent au moins un des termes en "or"
    or_list = cleaned_request['or_list']
    or_dic = recherche_stanford(or_list, inversed_index)
    or_result = pre_intersect(or_dic)
    or_result = union_many(or_result)
    or_result.sort()
    if or_result == []:
        joined = and_result
    else:
        joined = intersect(and_result, or_result)
    joined.sort()
    cleaned = list(set(joined) - set(not_result))
    cleaned.sort()
    return cleaned

def find_term_id(term, terms_dictionary):
    """
    fonction qui prend en entrée un term et la localisation du terms_dictionary
     et rend son term_id dans la collection
    """
    with open(terms_dictionary, 'rb') as terms_dictionary:
        terms_dictionary = pickle.load(terms_dictionary)
        try:
            term_id = terms_dictionary[term]
        except KeyError:
            term_id = ""
    return term_id


def get_posting_stanford(term_id, inversed_index):
    """
    fonction qui prends en entrée un mot et la localisation de inversed_index
    et qui donne un dictionaire des {doc_id: occurences}
    """
    term_posting = dict({})
    line = "line"
    with open(inversed_index, 'r') as inversed_index:
        line = inversed_index.readline().strip()
        while term_posting == {} and line != "":
            posting_list = line.split("|")
            if posting_list[0] == term_id:
                term_posting = ast.literal_eval(posting_list[1])
            else:
                line = inversed_index.readline().strip()
    return term_posting


def intersect(list_1, list_2):
    """
    fonction qui prend en entrée 2 listes triées et qui donne une liste représentant 
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
    fonction qui prend en entrée un dictionnaire de {mot:[doc_ids qui le contiennent]}
    et qui donne les listes de docs_ids
    """
    doc_ids = []
    for word, posting in words_postings_dic.items():
        doc_ids.append(posting)
    return doc_ids

def intersect_many(list_of_lists):
    """
    fonction qui applique intersect à une liste de liste, 2 à 2
    """
    while len(list_of_lists) > 1:
        list_of_lists[1] = intersect(list_of_lists[0], list_of_lists[1])
        list_of_lists.pop(0)
    try:
        return list_of_lists[0]
    except IndexError:
        return []

def union(a, b):
    """ fonction qui retourne l'union de deux listes """
    return list(set(a) | set(b)) 

def union_many(list_of_lists):
    """
    fonction qui applique union à une liste de liste, 2 à 2
    """
    while len(list_of_lists) > 1:
        list_of_lists[1] = union(list_of_lists[0], list_of_lists[1])
        list_of_lists.pop(0)
    try:
        return list_of_lists[0]
    except IndexError:
        return []


def recherche_stanford(words_list, inversed_index):
    """
    fonction qui prend en entrée une liste de mots et qui
    donne un dictionnaire {mot: [doc_ids qui le contiennent]}
    """
    result = {}
    for word in words_list:
        posting = get_posting_stanford(word, inversed_index)
        doc_ids = []
        try:
            for doc_id in posting.keys():
                doc_ids.append(doc_id)
            result[word] = doc_ids
        except AttributeError:
            pass
    for word in result:
        result[word].sort()
    return result

def find_document_from_docid(list_of_docids, docid_dict_path):
    doc_list = []
    with open(docid_dict_path, 'rb') as docid_dictionary:
        docid_dictionary = pickle.load(docid_dictionary)
        for docid in list_of_docids:
            doc_list.append(docid_dictionary[docid])
    return doc_list
