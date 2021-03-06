# To import modules from ../
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

# Optimum: 122455319

import problems
import permu_utils as putils
from optimizers import UMDA
import numpy as np
import matplotlib.pyplot as plt

PERMU_LENGTH = 20
POP_SIZE = PERMU_LENGTH*10
SURV_RATE = .5
ITERS = 20
TIMEOUT = 4*1000
INSTANCE_NAME = 'instances/QAP/tai20b.dat'

permu_dtype = np.int8

# Initialize optimizer and problem
umda = UMDA()
qap = problems.QAP()

dist, flow = qap.load_instance(INSTANCE_NAME)

# Create population
pop = putils.random_population(PERMU_LENGTH,
                                    POP_SIZE)
n_surv = int(POP_SIZE*SURV_RATE) # Number of survivor solutions

# Init loggers
log_min = []
log_avg = []

# Evaluate the initial population
fitness = np.empty(POP_SIZE)
for indx in range(POP_SIZE):
    fitness[indx] = qap.evaluate(pop[indx], dist, flow)

### Main loop ###
for iter_ in range(ITERS):

    # For later use
    old_pop = pop
    old_f = fitness
    
    # Select best solutions
    surv = np.empty((n_surv, PERMU_LENGTH), dtype=permu_dtype)
    surv_f = np.empty(n_surv)
    for i in range(n_surv):
        bests_indx = np.argmin(fitness)
        surv[i] = pop[bests_indx]
        surv_f[i] = fitness[bests_indx]

        pop = np.delete(pop, bests_indx, axis=0)
        fitness = np.delete(fitness, bests_indx)

    worst = pop
    worst_f = fitness

    ### Print and log data ###
    print('iter ', iter_+1, '/', ITERS, 
          'mean: ', np.mean(surv_f), ' best: ', min(surv_f))
    log_min.append(min(surv_f))
    log_avg.append(np.mean(surv_f))
    
    # Learn a probability distribution from survivors
    p = umda.learn_distribution(surv,
                                shape=(PERMU_LENGTH, PERMU_LENGTH)) 
    def evaluate(permu):
        return qap.evaluate(permu, dist, flow)   

    # Sample new solutions
    try:
        new, new_f= umda.sample_population(p, 
                                           n_surv, 
                                           pop=pop, 
                                           fitness=fitness,
                                           eval_func=evaluate,
                                           permutation=True,
                                           check_repeat=True,
                                           timeout=TIMEOUT)

    # except TimeoutError as e:
    except Exception as e:
        print(e)
        # If time out occurs, plot results
        plt.plot(range(iter_+1), log_avg, label='Mean')
        plt.plot(range(iter_+1), log_min, label='Best')
        plt.title('Ad-hoc ' + INSTANCE_NAME 
                  + ' best: {:0.2f}'.format(min(log_min)))
        plt.xlabel('Iterations')
        plt.ylabel('Survivors fitness')
        plt.legend()
        plt.grid(True)
        plt.show()
        putils.fancy_matrix_plot(p, 'Last probability matrix')
        quit()

    fitness = np.hstack((old_f, new_f))
    pop = np.vstack((old_pop, new))

    # Second selection
    pop, fitness = putils.remove_from_pop(pop, fitness, n_surv, func='max')

# Plot results
plt.plot(range(ITERS), log_avg, label='Mean')
plt.plot(range(ITERS), log_min, label='Best')
plt.xlabel('Iterations')
plt.ylabel('Survivors fitness')
plt.legend()
plt.title('Ad-hoc ' + INSTANCE_NAME 
          + ' best: {:0.2f}'.format(min(log_min)))
plt.grid(True)
plt.show()

putils.fancy_matrix_plot(p, 'Last probability matrix')
