class Node:
    def __init__(self, row=-1, col=-1):
        self.left = self.right = self.up = self.down = self
        self.column = self
        self.row_id = row
        self.col_id = col
        self.size = 0  # For column headers

class DancingLinks:
    def __init__(self, matrix):
        self.root = Node()
        self.columns = []
        # O atributo self.nodes não é usado, pode ser removido
        self.solutions = []

        cols = len(matrix[0])
        self.columns = [Node(col=i) for i in range(cols)]

        # Link headers horizontally
        for i in range(cols):
            self.columns[i].right = self.columns[(i + 1) % cols]
            self.columns[i].left = self.columns[(i - 1 + cols) % cols]
        self.root.right = self.columns[0]
        self.root.left = self.columns[-1]
        self.columns[0].left = self.root
        self.columns[-1].right = self.root

        # Add rows
        for i, row_data in enumerate(matrix):
            prev = None
            for j, val in enumerate(row_data):
                if val:
                    col_node = self.columns[j]
                    new_node = Node(row=i, col=j)
                    new_node.column = col_node
                    col_node.size += 1

                    # Vertical links
                    new_node.down = col_node
                    new_node.up = col_node.up
                    col_node.up.down = new_node
                    col_node.up = new_node

                    if prev:
                        # Horizontal links
                        new_node.left = prev
                        new_node.right = prev.right
                        prev.right.left = new_node
                        prev.right = new_node
                    # A lógica para o primeiro nó na linha estava errada,
                    # o novo nó deve apontar para si mesmo inicialmente.
                    # Mas a ligação com 'prev' já cobre isso se o primeiro nó
                    # se torna o 'prev'. Não precisa de 'else'.
                    prev = new_node

    def cover(self, col_node):
        col_node.right.left = col_node.left
        col_node.left.right = col_node.right
        i = col_node.down
        while i != col_node:
            j = i.right
            while j != i:
                j.down.up = j.up
                j.up.down = j.down
                j.column.size -= 1
                j = j.right
            i = i.down

    def uncover(self, col_node):
        i = col_node.up
        while i != col_node:
            j = i.left
            while j != i:
                j.column.size += 1
                j.down.up = j
                j.up.down = j
                j = j.left
            i = i.up
        col_node.right.left = col_node
        col_node.left.right = col_node

    def search(self, k=0):
        if self.root.right == self.root:
            # CORREÇÃO 1: Armazenar uma cópia da lista de nós, não seus IDs.
            self.solutions.append(self.sol[:])
            return True

        col = self.root.right
        tmp = col.right
        while tmp != self.root:
            if tmp.size < col.size:
                col = tmp
            tmp = tmp.right

        self.cover(col)
        row = col.down
        
        while row != col:
            self.sol.append(row)
            j = row.right
            while j != row:
                self.cover(j.column)
                j = j.right
            
            # Limita a busca a uma solução
            if self.search(k + 1):
                return True # Para aqui se uma solução for encontrada

            # Backtrack
            j = row.left
            while j != row:
                self.uncover(j.column)
                j = j.left
            self.sol.pop()
            row = row.down
        
        self.uncover(col)
        return False


    def solve(self):
        self.sol = []
        self.search()
        return self.solutions[0] if self.solutions else []

# Gerar matriz exata de cobertura para o Sudoku (9x9)
def sudoku_to_exact_cover(grid):
    matrix = []
    # Cria as linhas da matriz de cobertura exata
    # Cada linha representa uma possibilidade: colocar um 'num' em (r, c)
    for r in range(9):
        for c in range(9):
            for num in range(1, 10):
                # Se a célula já estiver preenchida, só consideramos essa possibilidade
                if grid[r][c] == 0 or grid[r][c] == num:
                    row = [0] * 324
                    # 1. Restrição de célula: (r, c) só pode ter um número
                    row[r * 9 + c] = 1
                    # 2. Restrição de linha: na linha r, o número 'num' só pode aparecer uma vez
                    row[81 + r * 9 + (num - 1)] = 1
                    # 3. Restrição de coluna: na coluna c, o número 'num' só pode aparecer uma vez
                    row[162 + c * 9 + (num - 1)] = 1
                    # 4. Restrição de bloco: no bloco 3x3, o número 'num' só pode aparecer uma vez
                    block_index = (r // 3) * 3 + (c // 3)
                    row[243 + block_index * 9 + (num - 1)] = 1
                    matrix.append(row)
    return matrix

# CORREÇÃO 2: Decodificar a solução corretamente
def decode_solution(solution, initial_grid):
    board = [[0] * 9 for _ in range(9)]
    
    # 'solution' é uma lista de nós, cada um iniciando uma linha da matriz DLX
    for row_node in solution:
        r, c, n = -1, -1, -1
        # Itera por todos os nós na mesma "linha" da escolha
        for node in row_loop(row_node):
            col_id = node.column.col_id
            
            if col_id < 81: # Restrição de célula
                r = col_id // 9
                c = col_id % 9
            elif col_id < 162: # Restrição de linha-número
                n = (col_id - 81) % 9 + 1
        
        if r != -1 and c != -1 and n != -1:
            board[r][c] = n
            
    # Adiciona os números originais do puzzle, pois eles não estão na solução do DLX
    for r in range(9):
        for c in range(9):
            if initial_grid[r][c] != 0:
                board[r][c] = initial_grid[r][c]
                
    return board


def row_loop(start_node):
    yield start_node
    node = start_node.right
    while node != start_node:
        yield node
        node = node.right

def print_grid(grid):
    for i in range(9):
        print(" ".join(str(cell) if cell != 0 else '.' for cell in grid[i]))

# Sudoku de entrada
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

# Simplifiquei também a geração da matriz de cobertura
matrix = sudoku_to_exact_cover(puzzle)
dlx = DancingLinks(matrix)
solution = dlx.solve()

# A decodificação agora precisa do grid inicial para preencher os números fixos
solved_grid = decode_solution(solution, puzzle)

print("Sudoku resolvido usando DLX:")
print_grid(solved_grid)