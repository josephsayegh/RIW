import os
import filemapper as fm
import indexes_creation_functions as indexes
import pickle
import ast
import time

        
def bsbi(path):
    """
    fonction qui prend en entree un path et qui parcours tous les documents dans tous les dossiers du path.
    chaque dossier est traite comme un block et la fonction va lire dans tous les documents et creer un fichier
    de tuples (terms, {doc_id: occurences})
    """
    term_docid = []
    block_list = os.listdir(path)
    docid = 1
    docid_dict = dict({})
    indexes_folder = 'Stanford_indexes'
    if not os.path.exists(indexes_folder):
        os.makedirs(indexes_folder)
    for block in block_list:
        url = os.path.join(path, block)
        documents = os.listdir(url)
        terms_pairs = {}
        dic_to_string = ""
        for document in documents:
            fullpath = os.path.join(url, document)
            with open(fullpath,'r') as document:
                docid_dict[docid] = fullpath
                print("fetching document {}".format(document))
                for line in document.readlines():
                    for word in line.split():
                        term_docid.append((word,docid))        
                docid += 1
        sorted = indexes.tuple_sort(term_docid)
        merged = indexes.tuple_merge(sorted)
        creation_path = os.path.join(indexes_folder, block)
        with open(creation_path,'w') as opened_doc:
            for key, value in merged.items():
                opened_doc.write('{}|{}\n'.format(key, value))
        term_docid = []
    print(docid_dict)    
    docid_dict_path = os.path.join(indexes_folder, 'doc_id_dictionary')
    with open(docid_dict_path, 'wb') as opened_docid_dict:
        pickle.dump(docid_dict, opened_docid_dict, protocol=pickle.HIGHEST_PROTOCOL)

def merge(first_index, second_index, combined_index):
    """
    fonction qui prend en entree 2 indexes a merger et un fichier dans lequel les merger et elle les merge
    """
    combined_index = open(combined_index, 'w')
    first_lower_limit = 0
    first_upper_limit = 5000
    second_lower_limit = 0
    second_upper_limit = 5000
    first_memory_buffer = read_document(first_index, first_lower_limit, first_upper_limit)
    second_memory_buffer = read_document(second_index, second_lower_limit, second_upper_limit)
    while first_memory_buffer != [] and second_memory_buffer != []:
        while first_memory_buffer != [] and second_memory_buffer != []:
            to_write = compare_memory_buffers(first_memory_buffer, second_memory_buffer)
            combined_index.write('{}|{}\n'.format(to_write[0], to_write[1]))
        first_lower_limit = first_upper_limit - len(first_memory_buffer)
        first_upper_limit = first_lower_limit + first_upper_limit
        second_lower_limit = second_upper_limit - len(second_memory_buffer)
        second_upper_limit = second_lower_limit + second_upper_limit
        first_memory_buffer = read_document(first_index, first_lower_limit, first_upper_limit)
        second_memory_buffer = read_document(second_index, second_lower_limit, second_upper_limit)
        
def compare_memory_buffers(first_memory_buffer, second_memory_buffer):  
    """
    prend deux listes de tuples (term, {doc_id: occurrence}) et les merge ensemble
    """      
    if first_memory_buffer[0][0] < second_memory_buffer[0][0]:
        to_write = first_memory_buffer[0]
        del first_memory_buffer[0]
        return to_write
    elif first_memory_buffer[0][0] > second_memory_buffer[0][0]:
        to_write = second_memory_buffer[0]
        del second_memory_buffer[0]
        return to_write
    elif first_memory_buffer[0][0] == second_memory_buffer[0][0]:
        first_posting = first_memory_buffer[0][1]
        second_posting = second_memory_buffer[0][1]
        merged_posting = first_posting.copy()
        merged_posting.update(second_posting)
        to_write = first_memory_buffer[0][0], merged_posting
        del first_memory_buffer[0]
        del second_memory_buffer[0]
        return to_write

def read_document(document, lower_line, upper_line):
    """
    prend en entree un document et les limites inferieures et superieures de lignes et retourne les lignes 
    de ce document qui sont entre ces limites
    """
    result = []
    with open(document, 'r') as document:
        for index, line in enumerate(document):
            if index>= lower_line and index <= upper_line:
                to_tuple = line.strip().split('|')
                cleaned = to_tuple[0], ast.literal_eval(to_tuple[1])
                result.append(tuple(cleaned))
        return result


def merge_all(path):
    """
    fonction qui prend un path en entree et qui va trouver les fichiers contenants uniquement des chiffres
    dans ce path. elle va les merge 2 a 2 et ensuite merge les resultats 2 a 2 jusqu'a obtenir un index final
    """
    raw_list = os.listdir(path)
    block_list = []
    for i in raw_list:
        if i.isdigit() == True:
            block_list.append(i)
    while len(block_list) > 1:
        if len(block_list) > 2:
            new_index_name = str(block_list[0]) + "+" + str(block_list[1])
        else:
            new_index_name = 'final_index'
        first_index = os.path.join(path, block_list[0])
        second_index = os.path.join(path, block_list[1])
        block_list.append(new_index_name)
        new_index = os.path.join(path, new_index_name)
        merge(first_index, second_index, new_index)
        del block_list[1]
        del block_list[0]
        print (block_list)

if __name__ == "__main__":
    start_time = time.time()
    launch_bsbi = bsbi('Stanford/pa1-data')   
    merge_indexes = merge_all('Stanford_indexes')
    print(launch_bsbi)
    end_time = time.time()
    print(end_time - start_time)