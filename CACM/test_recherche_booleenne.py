import boolean_research as br
import time
# request = recherche_booleenne.clean_request("research_study algebra !analysis harvard_mit !cambridge")
# print(request)

requete = input("Tappez votre requete: ")

requete = requete.lower()
cleaned_request = br.clean_request(requete)
print(cleaned_request)
start_time = time.time()
result = br.recherche_dans_cleaned_request(cleaned_request)
print(result)
end_time = time.time()
total_time = end_time - start_time
print(total_time)