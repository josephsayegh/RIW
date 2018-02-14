import pickle
import math
import matplotlib.pyplot as plt


def open_inversed_index(inversed_index):
    with open(inversed_index, 'rb') as inversed_index:
        inversed_index = pickle.load(inversed_index)
    return inversed_index

inversed_index = open_inversed_index("CACM/inversed_index")

def nb_tokens():
    result = 0
    for term_id in inversed_index:
        result += 1
        #for doc_id in inversed_index[term_id]:
            #result += inversed_index[term_id][doc_id]
    return result

print(nb_tokens())

b = (math.log(9497/6752))/(math.log(108235/52276))
k = 6752/(52276 ** b)

print(k * (1000000 ** b))

def get_frequency():
    frequencies = []
    i = 0
    for term_id in inversed_index:
        frequencies.append(0)
        for doc_id in inversed_index[term_id]:
            frequencies[i] += inversed_index[term_id][doc_id]
        i += 1
    frequencies = sorted(frequencies, reverse=True)
    #print(frequencies)
    dico = {}
    for i in range(1, len(frequencies)):
        dico[i] = frequencies[i]
    return dico

def blabla():
    x = []
    y = []
    for i in range(1,100):
        x.append(math.log(i))
        y.append(math.log(get_frequency()[i]))
    return x, y

x, y = blabla()

plt.scatter(x,y)
plt.title("diagramme log(fréquence)-log(rang)")
plt.xlabel("log(rang)")
plt.ylabel("log(fréquence)")
plt.show()