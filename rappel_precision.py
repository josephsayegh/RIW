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

def data_courbe(requete, nb_points):
    """
    fonction qui prend en entrée une requête et un nombre de points voulus (si on prend 100, la courbe sera précise au pourcent près)
    et qui donne une liste rappel de longueur nb_points + 1 et de pas 1/nb_points
    ainsi qu'une liste precision de même longueur avec les précisions associées à chaque rappel pour la requête.
    """
    answers = parse_qrels()[10]
    rappel = []
    precision = []
    rappel_discretise = []
    precision_discretise = []
    length_answer = len(parse_qrels()[10])
    result = length_answer
    my_answers = []
    result_requete = vectorial_search(requete, 3203)
    for j in range(3203):
        my_answers.append(result_requete[j][0])
    for i in range(nb_points + 1):
        rappel_discretise.append(i/nb_points)
        precision_discretise.append(0)
    for k in range(3203, 0, -1):
        rappel.append(0)
        precision.append(0)
        rappel[3203-k] = round(result / length_answer,2)
        precision[3203-k] = round(result / k,2)
        if k < 3203:
            if precision[3203-k] <= precision[3203-k-1]:
                precision[3203-k] = precision[3203-k-1]
        if my_answers[k-1] in answers:
            result += -1
    for i in range(nb_points + 1):
        if i/nb_points in rappel:
            precision_discretise[i] = precision[rappel.index(i/nb_points)]
        else:
            m = min(rappel_value - i/nb_points for rappel_value in rappel if rappel_value - i/nb_points > 0)
            precision_discretise[i] = precision[rappel.index(i/nb_points + m)]
    return rappel_discretise, precision_discretise


def moyenne_toutes(nb_points):
    """
    fonction qui prend à nouveau en entrée un nombre de points (précision voulue)
    et qui fait la moyenne des précisions pour les 64 requêtes de query.text
    """
    queries = fm.load("Requetes")
    precisions = []
    rappel = [0]*(nb_points + 1)
    precision = [0]*(nb_points + 1)
    for query in queries:
        for line in fm.read(query):
            precisions.append(data_courbe(line,nb_points)[1])
    for i in range(nb_points + 1):
        rappel[i] = i/nb_points
        for j in range(64):
            precision[i] += precisions[j][i]/64
    return rappel, precision


x = moyenne_toutes(100)[0]
y = moyenne_toutes(100)[1]
plt.scatter(x,y)
plt.title("courbe rappel-précision")
plt.xlabel("rappel")
plt.ylabel("précision")
plt.show()