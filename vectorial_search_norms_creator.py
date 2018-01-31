import vectorial_search_functions as vsf
import pickle

if __name__ == "__main__":

    norms = vsf.norm_build('CACM/inversed_index','CACM/Collection')
    
    with open('CACM/documents_norms', 'wb') as documents_norms:
        pickle.dump(norms, documents_norms, protocol=pickle.HIGHEST_PROTOCOL)