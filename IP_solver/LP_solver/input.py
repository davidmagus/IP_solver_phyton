import numpy as np

def read_lp_input(filename="LP_solver/input.txt"):
    with open(filename, 'r', encoding="utf-8") as f:
        # Csak a nem üres sorokat olvassuk be, levágva a whitespace-t
        lines = [line.strip() for line in f if line.strip()]

    n = int(lines[0])
    m = int(lines[1])
    c = list(map(float, lines[2].split()))

    A = []
    b = []
    for i in range(m):
        parts = list(map(float, lines[3 + i].split()))
        # Az utolsó elem a jobb oldali érték (b vektor)
        A.append(parts[:-1])
        b.append(parts[-1])
    
    A = np.array(A)
    b = np.array(b)
    c = np.array(c)
    return A, b, c
