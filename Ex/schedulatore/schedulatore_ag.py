# Import sulla directory delle librerie
import sys
import csv


sys.path.append('../../Lib')
from GeneticAlgorithm import GeneticAlgorithm

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

def fitness(sol):
    return sum([float(dataset[sol[j]][j]) for j in range(len(sol)-1)])

def fitness_cmp(fit1,fit2):
    return 1 if fit1 < fit2 else 0

dataset = leggi_dati()
GA = GeneticAlgorithm(fitness, fitness_cmp, min_val_gene=0, max_val_gene=39, pop_len=100, sol_len=800, srv_prc=0.5)
time,sol = GA.run(gen=100, pc=0.5, pm=0.05, debug = True)
GA.plot_performance('generations','total time')
print(['time = ',time])
print(['sol = ' ,sol])
