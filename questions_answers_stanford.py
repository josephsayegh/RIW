import pickle
import math
import matplotlib.pyplot as plt
from boolean_research_functions_stanford import get_posting_stanford
import ast



def nb_tokens_collection(inversed_index):
    """
    fonction qui renvoie le nombre de tokens dans la collection de Stanford
    """
    result = 0
    with open(inversed_index, 'r') as inversed_index:
        line = inversed_index.readline().strip()
        while line != "":
            result += 1
            line = inversed_index.readline().strip()
    return result

def vocabulary_height(inversed_index):
    """
    fonction qui renvoie la taille du vocabulaire la collection de Stanford
    """
    result = 0
    with open(inversed_index, 'r') as inversed_index:
        line = inversed_index.readline().strip()
        while line != "":
            posting_list = line.split("|")
            postings = ast.literal_eval(posting_list[1])
            for value in postings.values():
                result += value
            line = inversed_index.readline().strip()
            print(line)
    return result

def get_frequency(inversed_index):
    """
    fonction qui renvoie la taille du vocabulaire la collection de Stanford
    """
    frequencies = []
    with open(inversed_index, 'r') as inversed_index:
        line = inversed_index.readline().strip()
        while line != "":
            result = 0
            posting_list = line.split("|")
            token = posting_list[0]
            postings = ast.literal_eval(posting_list[1])
            for value in postings.values():
                result += value
            frequencies.append(result)
            line = inversed_index.readline().strip()
    frequencies.sort(reverse=True)
    return frequencies


def get_log_frequencies():
    """
    fonction qui transforme les fréquences précédentes en log-fréquences
    """
    x = []
    y = []
    freq = get_frequency("Stanford_indexes/final_index")
    print("vocab", sum(freq))
    print("tokens", len(freq))
    for i in range(1,100):
        x.append(math.log(i))
        y.append(math.log(freq[i]))
    return x, y

x, y = get_log_frequencies()

# nb_tokens = nb_tokens_collection("Stanford_indexes/final_index")
# vocab = vocabulary_height("Stanford_indexes/final_index")
# print(nb_tokens)
# print(vocab)

plt.scatter(x,y)
plt.title("diagramme log(fréquence)-log(rang)")
plt.xlabel("log(rang)")
plt.ylabel("log(fréquence)")
plt.show()