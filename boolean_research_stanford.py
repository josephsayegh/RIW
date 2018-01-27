import boolean_research_functions_stanford as br
import time

if __name__ == "__main__":
    requete = input("Tappez votre requete: ")
    requete = requete.lower()
    cleaned_request = br.clean_request(requete)
    print(cleaned_request)
    start_time = time.time()
    docids = br.recherche_dans_cleaned_request(cleaned_request, "Stanford_indexes/final_index")
    result = br.find_document_from_docid(docids,'Stanford_indexes/doc_id_dictionary')
    print(result)
    end_time = time.time()
    total_time = end_time - start_time
    print(total_time)