import numpy as np

""" Reads the content of the given file (set as "input.txt" as default) and returns a generator object which yields a tuple with (id_value:int, A:array, b:array, k_value:int) values

Expected Format:
id:
id
A:
A_1 #Each row of a
A_2
...
b:
b_1
b_2
...
k:
k
---------
...
---------
...


"""

def read_matrix_from_file(filename ="input.txt"):
    with open(filename, 'r') as f:
        lines = f.readlines()

    A_lines = []
    b_lines = []
    k_value = None
    id_value = None
    section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue  # Üres sorokat átugorjuk
        
        if line == "---------":
            # Átalakítás NumPy tömbökké
            A = np.array(A_lines)
            b = np.array(b_lines)

            # Validáció: b hossza = A sorainak száma
            if A.shape[0] != b.shape[0]:
                raise ValueError(f"Hibás méretek! A mátrix {A.shape[0]} sorból áll, de b {b.shape[0]} elemet tartalmaz.")
            

            yield id_value, A, b, k_value
            A_lines = []
            b_lines = []
            k_value = None
            id_value = None
            section = None
            continue
        elif line.startswith("id:"):
            section = "id"
            continue
        elif line.startswith("A:"):
            section = "A"
            continue
        elif line.startswith("b:"):
            section = "b"
            continue
        elif line.startswith("k:"):
            section = "k"
            continue

        if section == "A":
            A_lines.append(list(map(int, line.split(","))))
        elif section == "b":
            b_lines.append(int(line.split(",")[0]))  # Egy szám minden sorban
        elif section == "k":
            k_value = int(line)  # k egyetlen érték
        elif section == "id":
            id_value = int(line)  # k egyetlen érték

