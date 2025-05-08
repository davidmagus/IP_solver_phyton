import numpy as np
from fractions import Fraction as fr


def Primal_simplex(A, b, c, indicesofBase, phaseone=False):
    # Konvertálás Fraction típusra
    A = to_fraction_matrix(A)
    b = to_fraction_vector(b)
    c = to_fraction_vector(c)
    
    #Megengedetségi variáns:
    if phaseone:
        A, c, indicesofBase = add_artificial_variables(A)
    
#1) inicializálás: Kiindulunk egy Prímál megengedett bázisból
    B = Base(A, b, c, indicesofBase)
    
    while True:

#2) Legyen y duál megoldás B-hez
        #Ez már ki van számolva self.y-ban
    
#3) Ha yA >= c azaz B duál megendedett => STOP B optimális bázis visszadjuk az Optimum helyét, majd az x, y megoldásokat.
        if np.all(B.y @ A >= c):
            if phaseone: 
                if B.x @ c >= 0: #Megengedetség esetén az optimum értékéből következtünk
                    return B.indices, B.x, False
                else:
                    return B.x @ c, B.x, True
            else: #Optamalitási eset
                return B.x @ c, B.x, B.y
        
#4) Ha nem áltunk meg létezik egy j index ahol ya_j < c_j. Bland-szabályt követve válasszuk az első ilyet.
        j = 0
        while not (B.y @ A[:, j] < c[j]):
            j += 1
        
#5) Csináljunk javító írányt: x'_j := - B_inv a_j,  x' := [0, ..., 0, x'_j ,0, ... ,0,1 <- j ,0, ...,0]
        x = np.array([fr(0)] * len(c), dtype=object)
        x[j] = fr(1)
        for idx, val in zip(B.indices, -B.inv @ A[:, j]):
            x[idx] = val
        
#6) Nézzük meg, hogy az írány véges-e? Ha nem adjuk vissza, mint bizonyiték a nem végességre, Ha igen keressük meg az i oszlopot amit kicserélünk
        theta = [(B.x[i] / -x[i], i) for i in B.indices if x[i] < 0] #lambda az valami más így lett theta
        if not theta:
            return None, x, None
        i = min(theta)[1]
        
#7)Cseréljük ki a bázisban az a_j és a_i oszlopokat
        B.switch(j, i)



# Konverziós segédfüggvények, hogy minden szám Fraction típusú legyen.
def to_fraction_matrix(matrix):
    return np.array([[fr(val) for val in row] for row in matrix], dtype=object)

def to_fraction_vector(vector):
    return np.array([fr(val) for val in vector], dtype=object)

# Törtek alapú Gauss-Jordan inverzió
def inverse(matrix):
    n = matrix.shape[0]
    A = matrix.copy()
    I = np.identity(n, dtype=object)
    I = np.array([[fr(val) for val in row] for row in I], dtype=object)
    
    for i in range(n):
        # Ha a pivot nulla, keresünk másik sort
        if A[i][i] == 0:
            for r in range(i+1, n):
                if A[r][i] != 0:
                    A[[i, r]] = A[[r, i]]
                    I[[i, r]] = I[[r, i]]
                    break
            else:
                raise ValueError("A mátrix nem invertálható – nincs megfelelő pivot elem.")
        
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
            I[i][j] /= pivot
        
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                    I[k][j] -= factor * I[i][j]
    
    return I

class Base:
    """Az aktuális bázist és kapcsolódó értékeket kezelő osztály."""
    def __init__(self, A_, b_, c_, indices_):
        self._A = to_fraction_matrix(A_)
        self._b = to_fraction_vector(b_)
        self._c = to_fraction_vector(c_)
        self.indices = indices_.copy()
        
        self.B = self._A[:, self.indices]
        self.c = self._c[self.indices]
        self.inv = inverse(self.B)
        
        self.x_B = self.inv @ self._b
        self.x = np.array([fr(0)] * len(self._c), dtype=object)
        for idx, val in zip(self.indices, self.x_B):
            self.x[idx] = val
        
        self.y = self.c @ self.inv

    def switch(self, j, i):
        """Csere: a j-edik oszlopot betesszük a bázisba, míg az i-ediket kivesszük."""
        for k in range(len(self.indices)):
            if self.indices[k] == i:
                self.indices[k] = j
                self.B[:, k] = self._A[:, j]
                self.c[k] = self._c[j]
                self.inv = inverse(self.B)
                self.x_B = self.inv @ self._b
                self.x = np.array([fr(0)] * len(self._c), dtype=object)
                for idx, val in zip(self.indices, self.x_B):
                    self.x[idx] = val
                self.y = self.c @ self.inv
                break


def remove_dependent_rows(A, b, tol=1e-10):
    """
    Eltávolítja az A mátrixból a lineárisan függő sorokat, és szinkronizálja a b vektort.
    """
    A = np.array(A)
    b = np.array(b)
    Ab = np.hstack((A, b.reshape(-1, 1)))
    
    # A QR-felbontás segítségével meghatározzuk az független sorokat
    _, r = np.linalg.qr(Ab.T)
    independent_rows = np.abs(np.diag(r)) > tol
    
    A_indep = A[independent_rows]
    b_indep = b[independent_rows]
    
    return A_indep, b_indep

def add_artificial_variables(A):
    """
    Fokozatosan bővíti az A mátrixot mesterséges változókkal.
    Visszatér: az augmentált A, az új célfüggvény, és a mesterséges változók indexeinek listája.
    """
    m, n = A.shape
    I = np.eye(m)
    A_augmented = np.hstack((A, I))
    c_phase1 = np.array([0] * n + [-1] * m, dtype=float)
    artificial_indices = list(range(n, n + m))
    return A_augmented, c_phase1, artificial_indices
