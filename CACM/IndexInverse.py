import os
import re
import filemapper as fm


def create_list_pairs(folder_name):
    """
    cree une liste de paires de (terme, doc_id)
    """
    documents = fm.load(folder_name)
    postings = []
    for document in documents:
        document_id = [int(s) for s in document.split() if s.isdigit()][0]
        for line in fm.read(document):
            for word in line.split():
                pair = (word, document_id)
                postings.append(pair)
    return postings

def tuple_sort(tuple_list):
    """
    permet de trier une liste de paires (terme, doc_id) selon le doc_id
    """
    tuple_list.sort(key=lambda tup: tup[1])
    return tuple_list

def tuple_merge(tuple_list):
    """
    permet de fusioner une liste de pares (terme, doc_id) en un dico de la forme {'terme':{'frequence': f, 'documents' = [list de doc_id]}}
    """
    dic = {}
    for word, document_id in tuple_list:
        if word not in dic.keys():
            dic[word]={'frequence':1,'documents':[document_id]}
        elif word in dic.keys(): 
            dic[word]['frequence'] +=1
            dic[word]['documents'].append(document_id)   
    return dic        


a = create_list_pairs('Collection')
#a = tuple_sort(a)
a= tuple_merge(a)
print(a)


    



