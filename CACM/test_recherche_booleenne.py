import boolean_research as br
import time
# request = recherche_booleenne.clean_request("research_study algebra !analysis harvard_mit !cambridge")
# print(request)

requete = input("Tappez votre requete: ")

requete = requete.lower()
cleaned_request = br.clean_request(requete)
print(cleaned_request)
#requete_en_liste = requete.split(" ")
start_time = time.time()
#dico = br.recherche(requete_en_liste)
result = br.recherche_dans_cleaned_request(cleaned_request)
#liste = br.pre_intersect(dico)
#result = br.intersect_many(liste)
print(result)
end_time = time.time()
total_time = end_time - start_time
print(total_time)