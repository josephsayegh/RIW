import os
import filemapper as fm
import indexes
import pickle

def terms_terms_id(path):
    terms = {}
    block_list = os.listdir(path)
    for block in block_list:
        url = os.path.join(path, block)
        terms = indexes.create_terms_pairs(url)
        return terms
    return terms


        
def bsbi(path):
    term_docid = []
    block_list = os.listdir(path)
    docid = 1
    for block in block_list:
        url = os.path.join(path, block)
        documents = os.listdir(url)
        terms_pairs = {}
        dic_to_string = ""
        for document in documents:
            fullpath = os.path.join(url, document)
            with open(fullpath,'r') as document:
                print("fetching document {}".format(document))
                for line in document.readlines():
                    for word in line.split():
                        term_docid.append((word,docid))
                docid += 1
        sorted = indexes.tuple_sort(term_docid)
        merged = indexes.tuple_merge(sorted)
        with open(block,'w') as opened_doc:
            for key, value in merged.items():
                opened_doc.write('{},{}\n'.format(key, value))
            # pickle.dump(merged, opened_doc, protocol=pickle.HIGHEST_PROTOCOL)
        term_docid = []

def merge(first_index, second_index):
    first_buffer_lower = 0
    first_buffer_upper = 5000
    second_buffer_lower = 0
    second_buffer_upper = 5000
    first_memory = ""
    second_memory = ""
    with open(first_index,'r') as first_index:
        with open(second_index, 'r') as second_index:
            for index, line in enumerate(first_index):
                if index >= first_buffer_lower and index <= first_buffer_upper:
                    first_memory = line

def read_document(document, lower_line, upper_line):
    with open(document, 'r') as document:
        for index, line in enumerate(document):
            if index>= lower_line and index <= upper_line:
                return line







        #reste a faire la partie merge entre les fichiers

#a = bsbi('Stanford/pa1-data')   
a = read_document('0', 1, 10)
print(a)
# b = test('2')
# print(b)