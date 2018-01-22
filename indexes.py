import time
import filemapper as fm
import pickle

def create_document_pairs(folder_name):
    """
    cree un dictionnaire de paires de doc: doc_id a partir de la collection
    """
    documents = fm.load(folder_name)
    documents_pairs = {}
    for document in documents:
        document_id = [int(s) for s in document.split() if s.isdigit()][0]
        try:
            documents_pairs[document]
        except KeyError:
            documents_pairs[document] = document_id
    return documents_pairs

def create_terms_pairs(folder_name):
    """
    cree un dictionnaire de paires de term: term_id a partir de la collection
    """
    documents = fm.load(folder_name)
    terms_pairs = {}
    id = 1
    for document in documents:
        for line in fm.read(document):
            for word in line.split():
                try:
                    terms_pairs[word]
                except KeyError:
                    terms_pairs[word] = id
                id += 1
    return terms_pairs

def create_terms_doc_pairs(folder_name):
    """
    cree une liste de paires de (terme_id, doc_id)
    """
    documents_pairs = create_document_pairs(folder_name)
    terms_pairs = create_terms_pairs(folder_name)
    documents = fm.load(folder_name)
    terms_doc_pairs_list = []
    for document in documents:
        for line in fm.read(document):
            for word in line.split():
                term_id = terms_pairs[word]
                document_id = documents_pairs[document]
                pair = (term_id, document_id)
                terms_doc_pairs_list.append(pair)
    return terms_doc_pairs_list

def tuple_sort(tuples_list):
    """
    permet de trier une liste de paires (terme, doc_id) selon le terme
    """
    tuples_list.sort(key=lambda tup: tup[0])
    return tuples_list

def tuple_merge(tuples_list):
    """
    permet de fusioner une liste de paires (terme_id, doc_id)
    en un dico de la forme {'terme': {doc_id: nb_occurence}}
    """
    postings = {}
    for term_id, document_id in tuples_list:
        try:
            postings[term_id]
        except KeyError:
            postings[term_id] = {}
        try:
            postings[term_id][document_id] += 1
        except KeyError:
            postings[term_id][document_id] = 1
    return postings