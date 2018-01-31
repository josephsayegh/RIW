import vectorial_search_functions as vsf
import time

if __name__ == "__main__":
    requete = input("Tappez votre requete: ")
    start_time = time.time()
    result = vsf.vectorial_search(requete, "CACM/inversed_index", "CACM/Collection")
    print(result)
    end_time = time.time()
    total_time = end_time - start_time
    print(total_time)