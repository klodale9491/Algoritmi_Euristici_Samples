# Import sulla directory delle librerie
import sys
sys.path.append('../../Lib')

from GeneticAlgorithm import GeneticAlgorithm
from math import sin
from math import pi

def fitness(sol):
    mystr = ''
    for i in range(len(sol)):
        mystr += str(sol[i])
    x = remap(float(int(mystr,2)),0.,4095.,-1.,2.)
    return 1.0 + x * sin(10*pi*x)

def fitness_cmp(val_1,val_2):
    return 1 if val_1 > val_2 else 0

def remap(value,low1,high1,low2,high2):
    return low2 + (value - low1) * (high2 - low2) / (high1 - low1)

GA = GeneticAlgorithm(fitness,fitness_cmp,0,1,100,12)
max,sol = GA.run(gen=100, pc=0.8, pm=0.01, debug = True)
GA.plot_performance('generations', 'avg fitness')
print(['max = ', max])
print(['sol = ', sol])