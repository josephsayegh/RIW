import pickle
import math
import matplotlib.pyplot as plt


def open_inversed_index(inversed_index):
    """
    fonction qui ouvre l'index inversé. Pratique pour éviter d'ouvrir un index déjà ouvert dans une méthode.
    """
    with open(inversed_index, 'rb') as inversed_index:
        inversed_index = pickle.load(inversed_index)
    return inversed_index

inversed_index = open_inversed_index("CACM/inversed_index")

def nb_tokens_collection():
    """
    fonction qui renvoie le nombre de tokens dans la collection
    """
    result = 0
    for term_id in inversed_index:
        for doc_id in inversed_index[term_id]:
            result += inversed_index[term_id][doc_id]
    return result

def vocabulary_heigth():
    """
    fonction qui renvoie le nombre de tokens dans la collection
    """
    result = 0
    for term_id in inversed_index:
        result += 1
    return result


def get_frequency():
    """
    fonction qui donne la fréquence de chaque terme dans la collection sous forme d'un dictionnaire {terme: fréquence}
    """
    frequencies = []
    i = 0
    for term_id in inversed_index:
        frequencies.append(0)
        for doc_id in inversed_index[term_id]:
            frequencies[i] += inversed_index[term_id][doc_id]
        i += 1
    frequencies = sorted(frequencies, reverse=True)
    dico = {}
    for i in range(1, len(frequencies)):
        dico[i] = frequencies[i]
    return dico

def get_log_frequencies():
    """
    fonction qui transforme les fréquences précédentes en log-fréquences
    """
    x = []
    y = []
    for i in range(1,100):
        x.append(math.log(i))
        y.append(math.log(get_frequency()[i]))
    return x, y

x, y = get_log_frequencies()

plt.scatter(x,y)
plt.title("diagramme log(fréquence)-log(rang)")
plt.xlabel("log(rang)")
plt.ylabel("log(fréquence)")
plt.show()