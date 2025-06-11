from pysat.formula import CNF
from pysat.solvers import Glucose3

def var_id(r, c, n):
    return 81 * (r - 1) + 9 * (c - 1) + n

def encode_sudoku(puzzle):
    cnf = CNF()

    # Regra 1: Cada célula tem pelo menos um número
    for r in range(1, 10):
        for c in range(1, 10):
            cnf.append([var_id(r, c, n) for n in range(1, 10)])

    # Regra 2: Cada célula tem no máximo um número
    for r in range(1, 10):
        for c in range(1, 10):
            for n1 in range(1, 10):
                for n2 in range(n1 + 1, 10):
                    cnf.append([-var_id(r, c, n1), -var_id(r, c, n2)])

    # Regra 3: Linhas
    for r in range(1, 10):
        for n in range(1, 10):
            cnf.append([var_id(r, c, n) for c in range(1, 10)])
            for c1 in range(1, 10):
                for c2 in range(c1 + 1, 10):
                    cnf.append([-var_id(r, c1, n), -var_id(r, c2, n)])

    # Regra 4: Colunas
    for c in range(1, 10):
        for n in range(1, 10):
            cnf.append([var_id(r, c, n) for r in range(1, 10)])
            for r1 in range(1, 10):
                for r2 in range(r1 + 1, 10):
                    cnf.append([-var_id(r1, c, n), -var_id(r2, c, n)])

    # Regra 5: Blocos 3x3
    for block_row in range(0, 3):
        for block_col in range(0, 3):
            for n in range(1, 10):
                block_cells = []
                for i in range(1, 4):
                    for j in range(1, 4):
                        r = 3 * block_row + i
                        c = 3 * block_col + j
                        block_cells.append(var_id(r, c, n))
                cnf.append(block_cells)
                for i in range(len(block_cells)):
                    for j in range(i + 1, len(block_cells)):
                        cnf.append([-block_cells[i], -block_cells[j]])

    # Regra 6: Entradas do Sudoku
    for r in range(9):
        for c in range(9):
            n = puzzle[r][c]
            if n != 0:
                cnf.append([var_id(r + 1, c + 1, n)])

    return cnf

def solve_sudoku_with_sat(puzzle):
    cnf = encode_sudoku(puzzle)
    solver = Glucose3()
    solver.append_formula(cnf)

    if solver.solve():
        model = solver.get_model()
        solution = [[0 for _ in range(9)] for _ in range(9)]
        for v in model:
            if v > 0:
                v -= 1
                n = v % 9 + 1
                c = (v // 9) % 9
                r = (v // 81)
                solution[r][c] = n
        return solution
    else:
        return None

# Teste
puzzle = [
    [0, 0, 0, 0, 6, 0, 0, 0, 5],
    [6, 2, 4, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 3, 0, 0],
    [0, 0, 8, 0, 0, 4, 0, 3, 7],
    [0, 0, 9, 1, 0, 0, 5, 0, 0],
    [0, 0, 7, 5, 0, 0, 0, 9, 0],
    [0, 8, 2, 4, 7, 0, 0, 0, 0],
    [0, 9, 0, 3, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 9, 0, 5, 3],
]

sol = solve_sudoku_with_sat(puzzle)
if sol:
    print("Sudoku resolvido usando SAT:")
    for row in sol:
        print(" ".join(map(str, row)))
else:
    print("Sem solução.")
