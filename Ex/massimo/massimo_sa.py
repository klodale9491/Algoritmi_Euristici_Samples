# Import sulla directory delle librerie
import sys
sys.path.append('../../Lib')

from SimulatedAnnealing import SimulatedAnnealing
from random import uniform
from math import sin
from math import pi

# Prendo una soluzione casuale nel range continuo [-1,2]
def greedy_sol():
    # Scelgo un numero nell'intervallo [-1,2] e lo provo
    return uniform(-1.0, 2.0)

# Prendo una soluzione in un intorno stabilito eps
def perturb_sol(x1):
    eps = 0.5
    x2 = round(uniform(x1 - eps, x1 + eps),3)
    while x2 <= -1.0 or x2 >= 2.0:
        x2 = round(uniform(x1 - eps, x1 + eps),3)
    return x2

# Funzione che calcola l'energia del sistema
def energy(x):
    return -(1.0 + x * sin(10*pi*x))

# Funzione obiettivo da massimizzare
def obj_function(x):
    return 1.0 + x * sin(10*pi*x)

x0 = greedy_sol()
SA = SimulatedAnnealing(x0, 100.0, 0.01, 50, obj_function, energy, perturb_sol)
SA.run(debug=True)
SA.plot_performance('temperature', 'score')