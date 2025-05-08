import numpy as np
from scipy.optimize import linprog
from output import SmartWriter

def solveable(A,b, NoSolution:list,checkeq = True, checkLP = True):
    NoSolution[2] +=1
    if checkeq:
        x, s, q, d = np.linalg.lstsq(A,b)
        is_exact = np.allclose(A @ x, b)
        if not is_exact:
            NoSolution[1] += "\n Ax = b egyenlőség rendszer nemmegoldható"
            return False
    
    if checkLP:
        bounds = [(0, None)] * len(A[0])  # x >= 0 constraints
        result = linprog(c=[0] * len(A[0]), A_eq=A, b_eq=b, bounds=bounds, method='highs')
        if not result.success:
            NoSolution[1] += "\n LP relaxáció hiba \n"
            return False

    return True

def IP_solver(A:np.array, b:np.array, k:int,checkeq = True, checkLP = True):
    
    # x inicializálása -1 értékekkel, oszlopszám szerint
    x = np.full(A.shape[1], -1)
    NoSolution = [True, "", 0, 0]  # Adatok a feladatról [0]: van-e megoldtás(fordítva) [1]: Dokumentáció [2]: Hány részfeladatot végeztem el
    w = SmartWriter("log.txt")  # A lépések rögzitésére szolgáló eszköz


    def __IP_solver__(A:np.array, CurrentA, b:np.array, k:int, x:np.array, b_original: np.array, NoSolution:list,checkeq = True, checkLP = True):
        stuff_to_do = []
        if -1 in x:
            #w.write_to_file(f"{x}")
            if solveable(CurrentA,b,NoSolution, checkeq= checkeq, checkLP= checkLP):
                #w.append_to_last_written_line(" Y")
                i = 0
                while x[i] != -1:
                    i += 1

                for z in range(0,k):
                    newA = np.delete(CurrentA,0,axis= 1)
                    newb = b.copy() - (A[:,i] * z)
                    newx = x.copy()
                    newx[i] = z
                    stuff_to_do.append([newA, newb, newx.copy()])

                while stuff_to_do and NoSolution[0]:
                    nextone = stuff_to_do.pop()
                    __IP_solver__(A,nextone[0],nextone[1],k,nextone[2], b_original, NoSolution, checkeq= checkeq, checkLP= checkLP)


            else:
                NoSolution[1] += ": Az \n  A=" + str(CurrentA) + "\n b=" + str(b) + "\n feladat nem oldható meg \n \n"

        else:
            NoSolution[3] +=1
            if np.allclose(A @ x, b_original):
                NoSolution[0] = False
                NoSolution[1] = str(x) + "\n Megoldja a rendszert \n"
            else:
                NoSolution[1] += " " + str(x) + "\n nem megoldás \n"
        
    __IP_solver__(A, A, b, k, x, b,NoSolution, checkeq= checkeq, checkLP= checkLP)
    NoSolution[1] = f" Elvégzett részfeledatok: {NoSolution[2]}; Feladat megoldható: {not NoSolution[0]}; " + NoSolution[1]
    #w.write_end()
    return NoSolution[1], not NoSolution[0], NoSolution[2], NoSolution[3]


