# --- IMPORT DEPENDENCIES ------------------------------------------------------+

from __future__ import division
from random import random
from random import uniform
import numpy as np

# --- MAIN ---------------------------------------------------------------------+


class Particle:
    def __init__(self, x0):
        self.position_i = []          # particle position
        self.velocity_i = []          # particle velocity
        self.pos_best_i = []          # best position individual
        self.err_best_i = -1          # best error individual
        self.err_i = -1               # error individual

        for i in range(0, num_dimensions):
            self.velocity_i.append(uniform(-1, 1))
            self.position_i.append(x0[i])

    # evaluate current fitness
    def evaluate(self, costFunc):
        self.err_i = costFunc(np.array(self.position_i), eval_gradient=False)
        # self.err_i = costFunc(np.array(self.position_i))

        # check to see if the current position is an individual best
        if self.err_i < self.err_best_i or self.err_best_i == -1:
            self.pos_best_i = self.position_i.copy()
            self.err_best_i = self.err_i

    # update new particle velocity
    def update_velocity(self, pos_best_g):
        # constant inertia weight (how much to weigh the previous velocity)
        w = 0.5
        c1 = 1        # cognative constant
        c2 = 2        # social constant

        for i in range(0, num_dimensions):
            r1 = random()
            r2 = random()

            vel_cognitive = c1*r1*(self.pos_best_i[i]-self.position_i[i])
            vel_social = c2*r2*(pos_best_g[i]-self.position_i[i])
            self.velocity_i[i] = w*self.velocity_i[i]+vel_cognitive+vel_social

    # update the particle position based off new velocity updates
    def update_position(self, bounds):
        for i in range(0, num_dimensions):
            self.position_i[i] = self.position_i[i]+self.velocity_i[i]

            # adjust maximum position if necessary
            if self.position_i[i] > bounds[i][1]:
                self.position_i[i] = bounds[i][1]

            # adjust minimum position if neseccary
            if self.position_i[i] < bounds[i][0]:
                self.position_i[i] = bounds[i][0]


class Pso:

    def pos(self, costFunc, x0, bounds):

        global num_dimensions

        num_dimensions = len(x0)
        err_best_g = -1                   # best error for group
        pos_best_g = []                   # best position for group

        # establish the swarm
        swarm = []
        for i in range(0, self.num_particles):
            swarm.append(Particle(x0))

        # begin optimization loop
        i = 0
        while i < self.maxiter:
            if self.verbose:
                print(f'iter: {i:>4d}, best solution: {err_best_g:10.6f}')

            # cycle through particles in swarm and evaluate fitness
            for j in range(0, self.num_particles):
                swarm[j].evaluate(costFunc)

                # determine if current particle is the best (globally)
                if swarm[j].err_i < err_best_g or err_best_g == -1:
                    pos_best_g = list(swarm[j].position_i)
                    err_best_g = float(swarm[j].err_i)

            # cycle through swarm and update velocities and position
            for j in range(0, self.num_particles):
                swarm[j].update_velocity(pos_best_g)
                swarm[j].update_position(bounds)
            i += 1

        return np.array(pos_best_g), err_best_g

    def optimize(self, num_particles=15, maxiter=30, verbose=False):
        self.num_particles = num_particles
        self.maxiter = maxiter
        self.verbose = verbose
        return self.pos

# --- END ----------------------------------------------------------------------+
