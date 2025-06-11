from copy import deepcopy

# Sudoku inicial
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

def get_neighbors(row, col):
    neighbors = set()
    for i in range(9):
        if i != col:
            neighbors.add((row, i))
        if i != row:
            neighbors.add((i, col))
    # Bloco 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if (r, c) != (row, col):
                neighbors.add((r, c))
    return neighbors

# Inicializa domínios para todas as células
def init_domains(puzzle):
    domains = {}
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                domains[(row, col)] = list(range(1, 10))
            else:
                domains[(row, col)] = [puzzle[row][col]]
    return domains

def is_valid(puzzle, row, col, value):
    for i in range(9):
        if puzzle[row][i] == value or puzzle[i][col] == value:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if puzzle[r][c] == value:
                return False
    return True

# MRV: escolhe célula com menor número de opções
def select_unassigned_variable(domains):
    return min((v for v in domains if len(domains[v]) > 1), key=lambda x: len(domains[x]), default=None)

# Propagação de restrições (forward checking)
def forward_checking(domains, row, col, value):
    new_domains = deepcopy(domains)
    new_domains[(row, col)] = [value]

    for r, c in get_neighbors(row, col):
        if value in new_domains[(r, c)]:
            new_domains[(r, c)].remove(value)
            if len(new_domains[(r, c)]) == 0:
                return None  # Inconsistência
    return new_domains

def backtrack(puzzle, domains):
    if all(len(domains[cell]) == 1 for cell in domains):
        return True  # Todos os domínios têm apenas um valor

    cell = select_unassigned_variable(domains)
    if cell is None:
        return False

    row, col = cell
    for value in domains[(row, col)]:
        if is_valid(puzzle, row, col, value):
            puzzle[row][col] = value
            new_domains = forward_checking(domains, row, col, value)
            if new_domains:
                result = backtrack(puzzle, new_domains)
                if result:
                    return True
            puzzle[row][col] = 0  # Undo
    return False

def solve_sudoku_csp(puzzle):
    domains = init_domains(puzzle)
    success = backtrack(puzzle, domains)
    return success

def print_sudoku(puzzle):
    for row in puzzle:
        print(" ".join(str(num) if num != 0 else "." for num in row))


if solve_sudoku_csp(puzzle):
    print("Sudoku resolvido usando CSP:")
    print_sudoku(puzzle)
else:
    print("Não há solução.")

