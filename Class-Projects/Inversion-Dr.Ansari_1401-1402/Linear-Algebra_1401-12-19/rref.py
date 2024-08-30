from sympy import Matrix

M = Matrix([[1, 2, 3, 14],
            [1, 2, 2, 11],
            [1, 3, 4, 19]])

rref, pivot = M.rref()

print(pivot)
print(rref)
