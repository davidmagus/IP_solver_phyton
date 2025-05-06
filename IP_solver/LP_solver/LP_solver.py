import input
import Simplex as Sm

def Lp_solver():
    A, b, c = input.read_lp_input()

    # Feltételezzük, hogy az A mátrix sorai függetlenek.
    A, b = Sm.remove_dependent_rows(A, b)

    # Kétfázisú szimplex:
    # Első fázis: mesterséges változókkal keressük a megengedett megoldást.
    base, x_phase1, empty = Sm.Primal_simplex(A, b, c, None, phaseone=True)
    
    if empty:
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write("A poliéder üres")
        raise Exception("A poliéder üres")

    # Második fázis: a prímál algoritmus a megtalált bázissal.
    OPT, x, y = Sm.Primal_simplex(A, b, c, base)
    return OPT, x, y

OPT, x, y = Lp_solver()

# Az eredményeket kiírjuk az output.txt fájlba.
if OPT is not None:
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("Az optimum: " + str(OPT) + "\n")
        f.write("Optimális Prímál megoldás: " + str(x) + "\n")
        f.write("Optimális Duál megoldás: " + str(y) + "\n")
else:
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("A poliéder nem korlátos, egy javító irány: " + str(x))
