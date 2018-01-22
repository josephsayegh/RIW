import indexes
import pickle

terms = indexes.create_terms_pairs('CACM/Collection')
documents = indexes.create_document_pairs('CACM/Collection')
list_pairs = indexes.create_terms_doc_pairs('CACM/Collection')
postings = indexes.tuple_merge(list_pairs)

"""
a voir comment enregistrer des dictionnaires dans des fichiers
"""

with open('CACM/inversed_index', 'wb') as inversed_index:
    pickle.dump(postings, inversed_index, protocol=pickle.HIGHEST_PROTOCOL)
with open('CACM/terms_dictionary', 'wb') as terms_dictionary:
    pickle.dump(terms, terms_dictionary, protocol=pickle.HIGHEST_PROTOCOL)
with open('CACM/documents_dictionary', 'wb') as documents_dictionary:
    pickle.dump(documents, documents_dictionary, protocol=pickle.HIGHEST_PROTOCOL)
    