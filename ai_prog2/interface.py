import argparse, os
import numpy as np
from dpll import *

"""
This provides the interface-- both the front-end and the back-end
for the Davis-Putnam code.
This file takes text files as input, and processes them as given
in the problem statement specifications.
"""

def frontend(f):
    """Converts given input to input for DPLL"""

    with open(f, 'r') as inputfile:
        data = inputfile.read().splitlines()
    for l in range(len(data)):
        data[l] = data[l].split()

    #Problem statement
    start_state = [data[0][v] for v in range(1, len(data[0]), 2)]
    num_registers = int(len(data[0])/2)
    goal_state = [-1]*(int(len(data[0])/2))
    for s in range(int(len(data[1])/2)):
        goal_state[int(data[1][2*s])-1] = data[1][2*s+1]
    #print(goal_state)
    k = int(data[2][0])

    vals = []
    for s in range(len(start_state)):
        if start_state[s] not in vals:
            vals.append(start_state[s])

    print('Assigning atoms')
    #Initialise atoms
    atoms = []
    val_len = 0
    for t in range(0,k+1):
        for r in range(1,num_registers+1):
            for v in vals:
                tup = (r,v,t)
                atoms.append(tup)
                val_len+=1
    #atoms = []
    for t in range(0,k):
        for ra in range(1,num_registers+1):
            for rb in range(1, num_registers+1):
                if ra != rb:
                    tup = (ra, rb, t)
                    atoms.append(tup)

    #Clauses start here
    print('Assigning clauses')
    clauses = []


    #Unique value
    #If Value(R,VX,I) and VY is any value not equal to VX
    #then not Value(R,VY,I)

    for t in range(0, k+1):
        for v in vals:
            for r in range(1,num_registers+1):
                tup = (r,v,t)
                in1 = atoms.index(tup)
                for vv in vals:
                    if v != vv:
                        tup1 = (r,vv,t)
                        in2 = atoms.index(tup1)
                        c = [-in1, -in2]
                        clauses.append(c)


    #Positive effects of actions
    #If Assign(RA,RB,I) and Value(RB,V,I) then Value(RA,V,I+1)

    for t in range(0, k):
        for v in vals:
            for ra in range(1, num_registers+1):
                tup1 = (ra, v, t+1)
                index = atoms.index(tup1)
                for rb in range(1, num_registers+1):
                    if ra != rb:
                        tup2 = (ra,rb,t)
                        in1 = atoms.index(tup2)
                        tup3 = (rb, v, t)
                        in2 = atoms.index(tup3)
                        c = [-in1, -in2, index]
                        clauses.append(c)


    #Frame axiom (no change if no assignment)
    #If Value(R,VX,I) and not Assign(R,R1,I) and
    #not Assign(R,R2,I) and ... and not Assign(R,Rn,I)
    #then Value(R,VX,I+1)
    for t in range(0,k):
        for ra in range(1, num_registers+1):
            for v in vals:
                tup = (ra,v,t)
                in1 = atoms.index(tup)
                tup = (ra, v, t+1)
                in2 = atoms.index(tup)
                c = [-in1, in2]
                for rb in range(1, num_registers+1):
                    if ra != rb:
                        tup = (ra, rb, t)
                        c.append(atoms.index(tup))
                clauses.append(c)


    #Incompatible assignments For any three distinct registers
    #RA, RB, RC, if Assign(RA,RB,I) then not Assign(RB,RA,I);
    #not Assign(RA,RC,I); and not Assign(RB,RC,I).

    for t in range(0,k):
        for ra in range(1, num_registers+1):
            for rb in range(1, num_registers+1):
                for rc in range(1, num_registers+1):
                    if ra!=rb and ra!=rc and rb!=rc:
                        tup = (ra, rb, t)
                        index = atoms.index(tup)
                        tup = (rb, ra, t)
                        in1 = atoms.index(tup)
                        tup = (ra, rc, t)
                        in2 = atoms.index(tup)
                        tup = (rb, rc, t)
                        in3 = atoms.index(tup)
                        c = [-index, -in1]
                        clauses.append(c)
                        c = [-index, -in2]
                        clauses.append(c)
                        c = [-index, -in3]
                        clauses.append(c)


    #Start state
    for r in range(1, num_registers+1):
        tup = (r,start_state[r-1], 0)
        in1 = atoms.index(tup)
        c1 = [in1]
        clauses.append(c1)
        if goal_state[r-1] != -1:
            tup = (r, goal_state[r-1], k)
            in2 = atoms.index(tup)
            c2 = [in2]
            clauses.append(c2)

    #print(clauses)
    #print(len(atoms + atoms))
    #print(atoms)
    sol = DavisPutnam(len(atoms), clauses)
    print('Davis Putnam done. ')
    #print(val_len, len(atoms))
    #print((sol))
    if not sol:
        print('No solution')
        text_file=open("output.txt", "w")
        text_file.write('No solution')
        text_file.close()
    else:
        backend(sol, atoms, k, val_len)


def backend(sol, atoms, k, val_len):
    """Converts output from DPLL to the desired output"""
    value_out = []
    assign_out = []
    for i in range(len(sol)):
        if sol[i] > 0:
            if i < val_len:
                value_out.append(atoms[i])
            else:
                assign_out.append(atoms[i])
    output=''
    #print(value_out)
    #print(len(sol),len(atoms))
    print(atoms)
    print(sol)
    i,j = 0,0
    value_out.pop(0)
    for t in range(0,k):
        output += ('\nCycle '+str(t)+': ')
        while i < len(value_out) and value_out[i][2] == t:
            output += ('Value('+str(value_out[i][0])+','+\
                    str(value_out[i][1]) + ','+str(t)+') ')
            i+=1
        output +=('\n')
        while j < len(assign_out) and assign_out[j][2] == t:
            output += ('Assign('+str(assign_out[j][0])+',' \
                    +str(assign_out[j][1])+','+str(t) + ') ')
            j+=1
    output+= '\n Cycle ' +str(k) + ': '
    while i < len(value_out):
        output += ('Value('+str(value_out[i][0])+','+\
                str(value_out[i][1]) + ','+str(t) +') ')
        i+=1
    text_file = open('output.txt',"w")
    text_file.write(output)
    text_file.close()


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file','-f', type=str, required=True,\
            help='add .txt file to frontend')
    args = parser.parse_args()
    """Pipeline comes here"""
    """print here"""
    frontend(args.file)

