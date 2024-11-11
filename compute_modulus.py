import numpy as np
import math
import random
import warnings
import cvxpy as cvx

def fast_shortest_path(s, w):
    m_rows = []
    lightest = []
    lightest_value = math.inf

    def recurse(s, x, row):
        nonlocal m_rows, lightest, lightest_value
        row[x] = 1
        value = row @ w
        if value > lightest_value:
            return
        greater = []
        for i in range(x, len(s)):
            if s[i] > s[x] and all(s[j] > s[i] for j in greater):
                greater.append(i)
        if not greater:
            m_rows.append(row.copy())
            if value < lightest_value:
                lightest_value = value
                lightest = row.copy()
            return
        for element in greater:
            recurse(s, element, row)
            row[element] = 0
            
    for i, element in enumerate(s):
        if all(element < x for x in s[:i]):
            recurse(s, i, np.zeros(len(s)))

    return lightest, lightest_value

def add_constraint(N, c):
    if N is None:
        return c
    return np.vstack((N, c))

def modulus(N, p):
    n = N.shape[-1]

    rho = cvx.Variable(n)

    cons = [rho >= 0, N@rho >= 1]

    obj = cvx.Minimize(cvx.pnorm(1**(1/p)*rho, p)**p)

    prob = cvx.Problem(obj, cons)
    prob.solve(solver=cvx.ECOS)

    return obj.value, np.array(rho.value).flatten()

def fast_ssmodulus(pi, p, display=False):
    rho = np.zeros(len(pi))
    mod = 0
    tol = 1e-5
    N = None

    while True:
        gP, lv = fast_shortest_path(pi, rho)

        if lv > 1 - tol:
            return mod

        N = add_constraint(N, gP)

        mod, rho = modulus(N, p)

def compute_modulus(n):
    mods = []
    for _ in range(100):
        mods.append(fast_ssmodulus(random.sample(range(1, n + 1), n), 2))
    return sum(mods) / len(mods)