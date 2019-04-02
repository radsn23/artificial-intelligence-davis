import numpy as np
import os

"""
This file performs the actual DPLL (Davis–Putnam–Logemann–Loveland)
algorithm on the processed input and provides the output, which is fed
back into the interface file and processed as per output specifications.

"""
def obviousAssign(L, V):
    if L > 0:
        V[L] = 1
    else:
        V[-L] = -1
    return V

def propagate(A, S, V):
    i = 0
    while i < len(S):
        if A in S[i]:
            #Remove S[i] since it is satisfied
            S.pop(i)
            i-=1
        elif -A in S[i]:
            S[i].remove(-A)
        i+=1
    return S

def hasLiteral(atoms, S):
    for i in range(atoms):
        b = None
        for j in range(len(S)):
            if i in S[j]:
                if not b:
                    b=i
                elif b==i:
                    continue
                elif b!=i:
                    b=None
                    break

            elif -i in S[j]:
                if b==None:
                    b = -i
                elif b==-i:
                    continue
                elif b!= -i:
                    b=None
                    break
        if b:
            return b
    return None

def dpll(atoms, S, V):
    base = True
    while(base):
      #Base
      base=False
      if len(S)==0:
          return V
      else:
          for i in range(len(S)):
              if len(S[i])==0:
                  return None

      #Simple Case

      #Literal Elimination
      lit = hasLiteral(atoms, S)
      if lit:
          base=True
          V = obviousAssign(lit, V)
          j=0
          while j < len(S):
              if lit in S[j]:
                  S.pop(j)
                  j-=1
              j+=1
          continue

      #Forced Assignment
      for i in range(len(S)):
          if len(S[i]) == 1:
              obviousAssign(S[i][0], V)
              S = propagate(S[i][0], S, V)
              base=True
              break

    V1 = list(V)
    i=0
    while(V1[i]!=0):
        i+=1
    V1[i]=1

    S1 = S.copy()
    S1 = propagate(i, S1, V1)
    V1 = dpll(atoms, S1, V1)
    if V1:
        return V1
    V[i]= -1
    S= propagate(-i,S,V)
    return dpll(atoms, S, V)

def DavisPutnam(atoms, S):
    V = [0]*(atoms)
    return dpll(atoms, S, V)

