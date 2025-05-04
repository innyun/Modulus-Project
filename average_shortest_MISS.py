from itertools import permutations
import math
import numpy as np
import matplotlib.pyplot as plt
import random

stop = 20

def shortest_MISS(s):
    m_rows = []

    def recurse(s, x, row):
        nonlocal m_rows
        row[x] = 1
        greater = []
        for i in range(x + 1, len(s)):
            if s[i] > s[x] and all(s[j] > s[i] for j in greater):
                greater.append(i)
        if not greater:
            m_rows.append(row.copy())
            return
        for element in greater:
            recurse(s, element, row)
            row[element] = 0
            
    for i, element in enumerate(s):
        if all(element < x for x in s[:i]):
            recurse(s, i, np.zeros(len(s)))

    return min(sum(row) for row in m_rows)

exact = {}

for n in range(1, 9):
    s = 0
    d = 0
    for perm in permutations(range(1, n+1)):
        shortest = shortest_MISS(perm)
        s += shortest
        d += 1
    exact[n] = float(s / d)

approximate = {}

for n in range(9, stop + 1):
    s = 0
    d = 0
    for _ in range(1000):
        perm = random.sample(range(1, n+1), n)
        shortest = shortest_MISS(perm)
        s += shortest
        d += 1
    approximate[n] = float(s / d)

print(exact)
print(approximate)

plt.title(f"Average Shortest MISS of Size {1} to {stop}")
plt.xlabel("Size of Permutation")
plt.ylabel("Average Shortest MISS")
plt.scatter(approximate.keys(), approximate.values(), label="Approximate Values")
plt.scatter(exact.keys(), exact.values(), label="Exact Values")
plt.legend(loc="lower right")
plt.savefig("average_shortest_MISS.png", dpi=500)


