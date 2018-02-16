import pickle
import math
import matplotlib.pyplot as plt
import filemapper as fm
from vectorial_search_functions_cacm import vectorial_search


def parse_qrels():
    """
    fonction qui parse le document qrel.text sous format {query_id: [doc_ids]}
    """
    with open("qrels.text", 'r') as answers:
        docs = {}
        for i in range(1, 65):
                docs[i] = []
        for line in answers:
            line = line.split()
            docs[int(line[0])].append(int(line[1]))
    return docs

def get_query_index(requete):
    """
    fonction qui prend une requête écrite en entrée et donne son indice parmi les 64 requêtes proposées.
    """
    index = 0
    queries = fm.load("Requetes")
    for query in queries:
        for line in fm.read(query):
            if line == requete:
                index = query.split()[1]
    return index

def data_courbe(requete):
    """
    fonction qui prend en entrée une requête
    et qui donne une liste rappel de longueur 101 et de pas 1/100
    ainsi qu'une liste precision de même longueur avec les précisions associées à chaque rappel pour la requête.

    Méthode: on fait une requête sur tous les documents (3204 résultats) et on liste les résultats dans l'ordre (liste my_answers)
    le rappel est alors à 1 et la précision à nb_de_bons_documents/3204. On note result = lentgh_answer.
    On regarde my_answers sans le dernier doc. Si ce dernier doc est dans les bons résultats (qrels.text), alors on enlève 1 à result
    et on modifie le rappel et la précision en conséquence, sinon seule la précision est modifiée.
    On continue ainsi jusqu'à arriver à une liste my_answers de taille 1. La précision vaudra 1 si result vaut 1, 0 sinon.
    Ensuite on discrétise les résultats pour obtenir deux listes de taille 101 dont celle de rappel qui a un pas de 1/100.

    Cette méthode est très économe en calculs car on n'a pas à compter à chaque fois le nombre de bons résultats contenus dans
    le résultat de taille k de la requête. Le parcours à l'envers de la liste des 3204 résultats permet une complexité linéaire.
    """
    requete_index = get_query_index(requete)
    answers = parse_qrels()[int(requete_index)]    #liste contenant les résultats de qrels.text associés à la requête
    rappel = []                  #liste sui contiendra les rappels associés aux 3204 rangs possibles
    precision = []               #liste des précisions associées
    rappel_discretise = []       #liste rappel discrétisée pour faciliter le calcul d'une moyenne. taille 101
    precision_discretise = []    #liste precision discrétisée. taille 101
    length_answer = len(answers)     #nombre de documents contenus dans answers
    result = length_answer           #indice qui va partir de length_answer et finir à 1 si le premier document renvoyé est dans answers, 0 sinon
    my_answers = []                  #liste contenant, dans l'ordre, les 3204 documents renvoyés par la recherche vectorielle
    result_requete = vectorial_search(requete, 3203)
    for j in range(3203):
        #on ajoute les 3204 résultats de la requête dans my_answers
        my_answers.append(result_requete[j][0])
    for i in range(100 + 1):
        rappel_discretise.append(i/100)
        precision_discretise.append(0)
    for k in range(3203, 0, -1):
        rappel.append(0)
        precision.append(0)
        if length_answer > 0:
            #on crée la liste des rappels arrondis au centième et multipliés par 100 (c'est un peu une tambouille ça, j'ai eu du mal à discrétiser)
            rappel[3203-k] = int(round(result / length_answer,2)*100)
        else:
            rappel[3203-k] = int(round(100*k/3203,0))
        precision[3203-k] = round(result / k,3)
        if k < 3203:
            if precision[3203-k] < precision[3203-k-1]:
                #on ne garde que les valeurs les plus grandes, en partant de la droite
                precision[3203-k] = precision[3203-k-1]
        if my_answers[k-1] in answers:
            #si le k-1ème doc est dans les réponses, il ne sera pas dans la liste de résultats de taille k-1, donc on décrémente result
            result += -1
    for i in range(101):
        #discrétisation
        if i in rappel:
            #si i est dans rappel, on prend la valeur de precision correspondante
            precision_discretise[i] = precision[rappel.index(i)]
        else:
            #sinon on prend la plus proche à droite
            m = min(rappel_value - i for rappel_value in rappel if rappel_value - i > 0)
            precision_discretise[i] = precision[rappel.index(int(round(i + m,0)))]
    return rappel_discretise, precision_discretise


def moyenne_precisions():
    """
    fonction qui ne prend rien en entrée
    et qui fait la moyenne des précisions pour les 64 requêtes de query.text
    """
    queries = fm.load("Requetes")
    written_queries = []
    precisions = []
    rappel = [0]*(101)
    precision = [0]*(101)
    for query in queries:
        for line in fm.read(query):
            written_queries.append(line)
    for i in range(64):
        precisions.append(data_courbe(written_queries[i])[1])
    for i in range(101):
        rappel[i] = i/100
        for j in range(64):
            precision[i] += precisions[j][i]/64
    return rappel, precision


x = moyenne_precisions()[0]
y = moyenne_precisions()[1]
plt.scatter(x,y)
plt.title("courbe rappel-précision")
plt.xlabel("rappel")
plt.ylabel("précision")
plt.show()
