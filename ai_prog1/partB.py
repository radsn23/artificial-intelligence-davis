import numpy as np
import argparse
import os
from collections import defaultdict

def random_restart(length, num):
    return np.random.randint(0, num, length)

def get_neighbours(state, num):
    neighbours = []
    for s in range(len(state)):
        state_changed = state.copy()
        for n in range(num):
            state_changed[s] = n
            neighbours.append((state_changed.copy()))
    return np.unique(neighbours,axis=0)

def get_value_time(lengths, speeds, state):
    value_init = (np.array(lengths)*\
            np.array([float(bool(s)) for s in state]))
    time_init = [value_init[t]/speeds[state[t]-1] for t in range(len(value_init))]
    total_value_init, total_time_init = np.sum(value_init), np.max(time_init)
    return total_value_init, total_time_init

def get_best_neighbour(lengths, speeds, state, neighbours, targets):
    state_value, state_time = get_value_time(lengths, speeds,state)
    cost = (targets[1] - state_value + state_time - targets[0])
    #print(cost)
    res = state
    extras = [state_time, state_value]
    for n in neighbours:
        #print(n)
        n_value, n_time = get_value_time(lengths, speeds, n)
        value_shortfall = targets[1] - n_value
        time_overflow = n_time - targets[0]
        new_cost = (value_shortfall + time_overflow)
        if abs(cost) > abs(new_cost):
            cost = new_cost
            res = n
            extras = [n_time, n_value]
    return cost,res, extras


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file','-f', type=str,\
            required=True, help='add plaintext input \
            file for scheduling in the right format')
    args = parser.parse_args()
    with open(args.file,'r') as inputfile:
        data = inputfile.read().splitlines()


    [length_of_tasks, speed_of_tasks, targets] =\
            [[float(numeric_d) for numeric_d in d.split()]\
            for d in data]
    print('lengths, speeds, targets')
    print(length_of_tasks, speed_of_tasks, targets)
    print('------------------------')
    min_cost, final_state, final_params = np.inf,[],[]

    T, S = len(length_of_tasks), len(speed_of_tasks)
    for r in range(10):
        print('\n-----------------'+str(r+1)+'th random restart'+'--------------------\n')
        state = random_restart(T,S+1)
        #print(state)
        neighbours = get_neighbours(state, S+1)
        init = get_value_time(length_of_tasks, speed_of_tasks, state)
        #print(neighbours)
        cost,res, params = (get_best_neighbour(length_of_tasks, speed_of_tasks,\
                state, neighbours,targets))
        print('Initial state:{0}, Target: {1}'.format(state, targets))
        print('Initial time: {1}, Initial value: {0}\n'
                .format(init[0], init[1]))
        print('cost, final state, time, value')
        while cost!=0 and (res-state).any():
            #print(state, res)
            state = res
            neighbours = get_neighbours(state, S+1)
            cost, res, params = (get_best_neighbour(length_of_tasks, speed_of_tasks,\
                state, neighbours,targets))
            print(cost, res, params)
        if (params[0]<=targets[0] and params[1]>= targets[1]) or abs(cost)<=abs(min_cost):
            min_cost,final_state, final_params = cost, res, params
    """
    print('\n---------------------------------------------------------------------------------\n')
    print('Target time:{0}, Target value: {1}'.format(targets[0], targets[1]))
    print('BEST STATE:', final_state)
    print('Cost:{0}, Time: {1}, Value: {2}'.format(min_cost, final_params[0],\
            final_params[1]))
    print('\n---------------------------------------------------------------------------------\n')
    """


