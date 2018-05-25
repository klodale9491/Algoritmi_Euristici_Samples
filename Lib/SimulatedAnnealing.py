# Classe per la realizzazione di algoritmi di simulated annealing
from random import random
from math import pow
from math import e
import matplotlib.pyplot as plt


class SimulatedAnnealing:

    def __init__(self,
                 init_sol,   # Soluzione iniziale
                 init_tmp,   # Temperatura iniziale alta
                 min_tmp,    # Temperatura minima del sistema da raggiungere
                 thr_eqb,    # Numero iterazioni per il test dell'equilibrio termico
                 obj_fnc,    # Funzione obiettivo da ottimizzare
                 energy_fnc, # Funzione per il calcolo dell'energia
                 perturb_fnc # Funzione di perturbazione della soluzione corrente
                 ):
        self.curr_sol = init_sol
        self.curr_tmp = init_tmp
        self.min_tmp = min_tmp
        self.thr_eqb = thr_eqb
        self.energy = energy_fnc
        self.perturb = perturb_fnc
        self.objective = obj_fnc
        self.boltz_const = 8.61673324 * pow(10, -5)
        self.cooling_schedule = 0.9
        # Valori delle soluzioni che vado trovando
        self.scores = []
        self.temps = []


    # Plotta le performance dell'algoritmo di simulated annealing
    def plot_performance(self, xlab, ylab, scale=1):
        plt.plot([self.temps[i] for i in range(len(self.temps)) if i % scale == 0], [self.scores[i] for i in range(len(self.scores)) if i % scale == 0])
        plt.axis([min(self.temps), max(self.temps), min(self.scores), max(self.scores)])
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.grid(True)
        plt.show()

    # Esegue il simulated annealing
    def run(self, debug=False):
        good_sol_vec = self.curr_sol
        good_sol_val = self.objective(self.curr_sol)
        # Eseguo fin tanto che non sono arrivato alla configurazione
        # di minima energia per il sistema
        while self.curr_tmp > self.min_tmp:
            for i in range(self.thr_eqb):
                new_sol = self.perturb(self.curr_sol)
                diff_energy = self.energy(new_sol) - self.energy(self.curr_sol)
                if diff_energy < 0:
                    good_sol_val = self.objective(new_sol)
                    good_sol_vec = new_sol
                    self.curr_sol = new_sol  # Accetto la nuova soluzione se e' stata migliorativa
                else:
                    diff_energy_prob = pow(e, -(diff_energy/self.curr_tmp))
                    if random() < diff_energy_prob:
                        self.curr_sol = new_sol
            # Salvo punteggi e temperature
            self.scores.append(self.objective(self.curr_sol))
            self.temps.append(self.curr_tmp)
            # Abbasso la temperatura ad ogni passo di un fatto moltiplicativo
            self.curr_tmp = self.curr_tmp * self.cooling_schedule
            # Stampo lo stato della soluzione corrente
            if debug:
                print(['curr_val :', self.objective(self.curr_sol), 'curr_tmp: ', self.curr_tmp, 'best_sol :', good_sol_val])
        return good_sol_vec,good_sol_val