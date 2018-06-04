# Import sulla directory delle librerie

import sys
import csv
sys.path.append('../../Lib')
from GeneticAlgorithm import GeneticAlgorithm

# Leggo dati dal DB
def leggi_dati():
    with open('dataset.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        dataset = []
        for row in spamreader:
            myrow = []
            for col in row:
                myrow.append(col)
            dataset.append(myrow)
    return dataset

def fitness(x):
    return sum([float(dataset[x[i]][i]) for i in range(len(x))])

def fitness2(x):
    unq_cpu = list(set(x))
    tot_time = {}
    for i in range(len(unq_cpu)):
        tot_time[unq_cpu[i]] = 0.0
    for j in range(len(x)):
        tot_time[x[j]] += float(dataset[x[j]][j])
    return max(tot_time.values())

def fitness_cmp(fit1,fit2):
    return 1 if fit1 < fit2 else 2

N_CPU = 40
N_JOBS = 800
dataset = leggi_dati()

def main():
    GA = GeneticAlgorithm(fitness, fitness_cmp, min_val_gene=0, max_val_gene=39, pop_len=50, sol_len=800)
    sol = GA.run(gen=10000, pc=0.8, pm=0.0001, debug=True)
    GA.plot_performance('fit variance', 'total time')
    print(['time = ', fitness(sol)])
    print(['sol = ', sol])

if __name__=="__main__":
    main()
