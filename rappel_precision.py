import pickle
import math
import matplotlib.pyplot as plt
import filemapper as fm
from vectorial_search_functions import vectorial_search

def execution_requetes():
    queries = fm.load("Requetes")
    result = {}
    for query in queries:
        result[int(query.split()[1])] = []
        for line in fm.read(query):
            for j in range(10):
                result[int(query.split()[1])].append(vectorial_search(line, 10)[j][0])
    return result

def parse_qrels():
    with open("qrels.text", 'r') as answers:
        docs = {}
        for i in range(1, 65):
                docs[i] = []
        for line in answers:
            line = line.split()
            docs[int(line[0])].append(int(line[1]))
    return docs

def rappel_precision():
    result = []
    result1 = []
    result2 = []
    answers = parse_qrels()
    my_answers = execution_requetes()
    result.append(0)
    result1.append(0)
    result2.append(0)
    if answers[1] != []:
        for j in range(10):
            if my_answers[1][j] in answers[1]:
                result[0] += 1
        result1[0] = result[0] / len(answers[1])
        result2[0] = result[0] / 10
    return result1, result2

def data_courbe1():
    answers = parse_qrels()[10]
    result = []
    result1 = []
    result2 = []
    length_answer = len(parse_qrels()[10])
    my_answers = []
    for j in range(10):
        my_answers.append(vectorial_search(" Parallel languages; languages for parallel computation ", 10)[j][0])
    for k in range(1,10):
        result.append(0)
        result1.append(0)
        result2.append(0)
        for i in range(k):
            if my_answers[:k][i] in answers:
                result[k-1] += 1
        result1[k-1] = result[k-1] / length_answer
        result2[k-1] = result[k-1] / k
    return result1, result2
    
#print(parse_qrels()[10])
#print(vectorial_search(" Parallel languages; languages for parallel computation ", 10))
x = data_courbe1()[0]
y = data_courbe1()[1]
plt.scatter(x,y)
plt.title("courbe rappel-précision")
plt.xlabel("rappel")
plt.ylabel("précision")
plt.show()