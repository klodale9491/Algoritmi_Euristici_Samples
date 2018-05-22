# Import sulla directory delle librerie
import sys
import csv
from random import randint

sys.path.append('../../Lib')
from SimulatedAnnealing import SimulatedAnnealing

N_CPU = 40
N_JOBS = 800

# Leggo dati dal DB
def leggi_dati():
    with open('dataset.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        dataset = []
        for row in spamreader:
            myrow = []
            for col in row:
                myrow.append(col)
            dataset.append(myrow)
    return dataset

# Assegno ad ogni job la cpu che ci sta il tempo minore
def greedy_sol(ds):
    x1 = [0 for i in range(N_JOBS)]
    for j in range(N_JOBS):
        v = [ds[i][j] for i in range(N_CPU)]
        x1[j] = sorted(range(len(v)), key=v.__getitem__)[0]
    return x1

def perturb_sol(x1):
    # Scelgo un job e cambio la CPU di appartenenza
    job = randint(0, N_JOBS-1)
    x2 = [x for x in x1]
    x2[job] = randint(0, N_CPU-1)
    return x2

# Funzione che calcola l'energia del sistema
def energy(x):
    return sum([float(dataset[x[i]][i]) for i in range(len(x))])

# Funzione obiettivo da massimizzare
def obj_function(x):
    return sum([float(dataset[x[i]][i]) for i in range(len(x))])

# 40 righe X 800 colonne
dataset = leggi_dati()
x0 = greedy_sol(dataset)
SA = SimulatedAnnealing(x0, 1.0, 0.0001, 300, obj_function, energy, perturb_sol)
SA.run(debug=True)
SA.plot_performance('temperature', 'total cpu time')