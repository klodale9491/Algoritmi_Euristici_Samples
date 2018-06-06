import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine as cosine_distance
from random import randint
from numpy import linalg as la
import numpy



def cosine_variance(space):
    vectors = len(space)
    # Calcolo le distanze coseno fra tutti i vettori
    cos_dis = []
    for i in range(vectors):
        for j in range(i + 1, vectors):
            v1 = space[i]
            v2 = space[j]
            distance = cosine_distance(v1, v2)
            cos_dis.append(distance)
    cos_avg = numpy.average(cos_dis)
    cos_var = numpy.var(cos_dis)
    return cos_avg, cos_var


def normalize(space):
    vectors = len(space)
    dimensions = len(space[0])
    # Normalizzazione ...
    for v in range(vectors):
        for d in range(dimensions):
            space[v][d] /= la.norm(space[v])
    return space


def random_space(dimensions, vectors, max):
    space = [[0 for x in range(dimensions)] for y in range(vectors)]
    # Crea vettori a caso in questo spazio
    for i in range(vectors):
        for j in range(dimensions):
            space[i][j] = randint(1, max)
    return normalize(space)


def add_dimensions(space, ndim, max):
    for i in range(len(space)):
        for j in range(ndim):
            # val = randint(0, max)
            space[i].append(0)
    return normalize(space)


if __name__ == "__main__":
    init_dim = 2
    space = random_space(dimensions=init_dim, vectors=5, max=10)
    means = []
    variances = []
    dimensions = []
    max_dimensions = 50
    # Aumento le dimensioni via via e calcolo la varianza della popolazione
    for i in range(1, max_dimensions):
        mean, variance = cosine_variance(space)
        means.append(mean)
        variances.append(variance)
        dimensions.append(init_dim + i)
        print(['dim: ', i, 'cosine_variance: ', variance, 'cosine_mean: ', mean])
        # Aggiungo delle dimensioni
        space = add_dimensions(space, i, 10)
    # Plotto i grafici
    fig = plt.figure()
    plt.subplot(2, 1, 1)
    plt.xlabel('dimensions')
    plt.ylabel('mean')
    plt.plot(dimensions, means)
    plt.grid(True)
    plt.subplot(2, 1, 2)
    plt.xlabel('dimensions')
    plt.ylabel('variance')
    plt.plot(dimensions, variances)
    plt.grid(True)
    plt.show()