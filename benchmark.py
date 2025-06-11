import time
from memory_profiler import profile

from solve_csp import solve_sudoku_csp
from solve_dlx import DancingLinks, sudoku_to_exact_cover, decode_solution
from solve_sat import solve_sudoku_with_sat

# O mesmo puzzle para todos os testes
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

# Função wrapper para o profiler de memória e tempo
@profile
def run_csp_solver():
    puzzle_copy = [row[:] for row in puzzle]
    solve_sudoku_csp(puzzle_copy)
    return puzzle_copy

@profile
def run_dlx_solver():
    matrix = sudoku_to_exact_cover(puzzle)
    dlx = DancingLinks(matrix)
    solution = dlx.solve()
    solved_grid = decode_solution(solution, puzzle)
    return solved_grid

@profile
def run_sat_solver():
    solution = solve_sudoku_with_sat(puzzle)
    return solution

def run_benchmarks(runs=5):
    """Executa cada solver várias vezes e calcula a média de tempo."""
    
    print("Iniciando Benchmarks...")
    print("="*30)

    # --- CSP ---
    csp_times = []
    print("\nAnalisando CSP Solver...")
    for i in range(runs):
        start_time = time.perf_counter()
        run_csp_solver()
        end_time = time.perf_counter()
        csp_times.append(end_time - start_time)
    avg_csp_time = sum(csp_times) / runs
    print(f"Tempo médio CSP: {avg_csp_time:.6f} segundos")

    # --- DLX ---
    dlx_times = []
    print("\nAnalisando DLX Solver...")
    for i in range(runs):
        start_time = time.perf_counter()
        run_dlx_solver()
        end_time = time.perf_counter()
        dlx_times.append(end_time - start_time)
    avg_dlx_time = sum(dlx_times) / runs
    print(f"Tempo médio DLX: {avg_dlx_time:.6f} segundos")

    # --- SAT ---
    sat_times = []
    print("\nAnalisando SAT Solver...")
    for i in range(runs):
        start_time = time.perf_counter()
        run_sat_solver()
        end_time = time.perf_counter()
        sat_times.append(end_time - start_time)
    avg_sat_time = sum(sat_times) / runs
    print(f"Tempo médio SAT: {avg_sat_time:.6f} segundos")

    print("\n" + "="*30)
    print("Benchmark de memória será exibido separadamente.")


if __name__ == "__main__":
    # Para o benchmark de tempo, execute o script normalmente
    # Para o benchmark de memória, execute com o memory_profiler
    run_benchmarks()