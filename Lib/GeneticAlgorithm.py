# Coder : Alessio Giorgianni

from random import randint
from random import random
import matplotlib.pyplot as plt


class GeneticAlgorithm:

    def __init__(self,
                 fitness_fnc,     # Funzione di fitness custom
                 fitness_cmp_fnc, # Permette di confrontare 2 valori di fitness. Torna 1 se la prima fit
                                  # e' migliore della seconda, 0 altrimenti.
                 min_val_gene,    # Min valore per del gene (nel caso binario, 0)
                 max_val_gene,    # Max valore per del gene (nel caso binario, 1)
                 pop_len,         # Cardinalita della popolazione iniziale
                 sol_len,         # Numero di geni(bit) del cromosoma(soluzione)
                 srv_prc          # Percentuale di individui sopravvisuti dopo la selezione naturale
                 ):
        self.fitness_fnc = fitness_fnc
        self.fitness_cmp_fnc = fitness_cmp_fnc
        self.min_val_gene = min_val_gene
        self.max_val_gene = max_val_gene
        self.pop_len = pop_len
        self.sol_len = sol_len
        self.srv_prc = srv_prc
        # Popolazione delle soluzioni
        self.solutions = []
        self.random_population()
        # Performarce algoritmo
        self.times = []
        self.scores = []

    # Plotta le performance dell'algoritmo genetico
    def plot_performance(self,xlab,ylab):
        plt.plot(self.times, self.scores)
        plt.axis([0, len(self.times), min(self.scores), max(self.scores)])
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.grid(True)
        plt.show()

    # Trova la migliore fitness tornando la soluzione
    # ed il suo valore
    def fitness_bst(self,fits):
        best_index = 0
        for i in range(1,len(fits)):
            if self.fitness_cmp_fnc(fits[i],fits[best_index]) == 1:
                best_index = i
        return fits[best_index],best_index

    # Funzione di selezione naturale in base al metodo a TORNEO
    # Permette di far sopravvivere una percentuale delle solzioni
    def natural_selection(self):
        num_surv = int(self.srv_prc * len(self.solutions))
        new_pop = []
        for i in range(num_surv):
            # Scelgo a caso due elementi della popolazione e verifico chi sia il migliore aggiunggendoli
            # alla nuova popolazione.
            sol_1 = self.solutions[randint(0, len(self.solutions)) - 1]
            sol_2 = self.solutions[randint(0, len(self.solutions)) - 1]
            new_pop.append(sol_1 if self.fitness_fnc(sol_1) > self.fitness_fnc(sol_2) else sol_2)
        return new_pop

    # Funzione che crea una popolazione random di soluzioni
    def random_population(self):
        # Creo soluzioni di taglia sol_len
        for i in range(self.pop_len):
            sol = []
            for j in range(self.sol_len):
                sol.append(randint(self.min_val_gene, self.max_val_gene))
            self.solutions.append(sol)

    # Funzione che effettua crossover a due punti della soluzione
    def crossover2(self, sol_1, sol_2, pieces=3):
        frg_len = len(sol_1) / 3
        # Scambio dei geni ...
        s1 = [sol_1[0:frg_len], sol_2[frg_len:2 * frg_len], sol_1[2 * frg_len:]]
        s2 = [sol_2[0:frg_len], sol_1[frg_len:2 * frg_len], sol_2[2 * frg_len:]]
        # Ricompongo le soluzioni
        sol_1 = []
        sol_2 = []
        for i in range(3):
            for j in range(len(s1[i])):
                sol_1.append(s1[i][j])
                sol_2.append(s2[i][j])
        return sol_1, sol_2

    # Funzione che simula una mutazione puntuale di un gene
    def mutation(self, sol, pm):
        for i in range(len(sol)):
            if random() >= pm:
                sol[i] = randint(self.min_val_gene, self.max_val_gene)
        return sol

    # Main routine dell'algoritmo genetico
    def run(self, gen, pc=0.5, pm=0.05, debug=False):
        good_sol_val = self.fitness_fnc(self.solutions[0])
        good_sol_vec = self.solutions[0]
        for g in range(gen):
            if len(self.solutions) > 1:
                fitness = [self.fitness_fnc(self.solutions[i]) for i in range(len(self.solutions))]
                # Salvo le buone soluzioni per non perderle per strada
                for j in range(len(fitness)):
                    if self.fitness_cmp_fnc(fitness[j], good_sol_val) == 1:
                        good_sol_val = fitness[j]
                        good_sol_vec = self.solutions[j]
                new_sol = self.natural_selection()
                for i in range(len(new_sol)):
                    # Faccio incrociare gli individui in base alla loro probabilita di crossover pc
                    if pc >= random():
                        sol_1 = self.solutions[i]
                        sol_2 = self.solutions[randint(0, len(self.solutions) - 1)]
                        sol_1, sol_2 = self.crossover2(sol_1, sol_2)
                        # Prendo solo una soluzione delle 2
                        new_sol.append(sol_1)
                # Avvio le mutazioni puntuali delle soluzioni
                for k in range(len(new_sol)):
                    new_sol[k] = self.mutation(new_sol[k], pm)
                # Aggiorno la popolazione
                del (self.solutions)  # Dealloca la memoria per evitare memory leak, e cali di prestazioni
                self.solutions = [x for x in new_sol]
                if (debug):
                    best_val,best_vec = self.fitness_bst([self.fitness_fnc(x) for x in self.solutions])
                    print(['iterazione #', g, 'good_sol = ', good_sol_val, 'curr_sol = ', best_val, 'pop = ', len(self.solutions)])
                    self.times.append(g)
                    self.scores.append(best_val)
        return good_sol_val,good_sol_vec