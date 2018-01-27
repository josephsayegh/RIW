import boolean_research_functions_cacm as br
import time

if __name__ == "__main__":
    requete = input("Tappez votre requete: ")
    requete = requete.lower()
    cleaned_request = br.clean_request(requete)
    print(cleaned_request)
    start_time = time.time()
    result = br.recherche_dans_cleaned_request(cleaned_request, "CACM/terms_dictionary", "CACM/inversed_index")
    print(result)
    end_time = time.time()
    total_time = end_time - start_time
    print(total_time)