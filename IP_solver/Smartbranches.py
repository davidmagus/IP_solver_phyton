import numpy as np
from scipy.optimize import linprog
import copy
import math


def write_to_file(text):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(text)

def convert_to_vector(data):   #Ha a tartomány [[1, 1], [2, 2], [2, 2], [1, 1], [1, 1]] alakú abból egy np.array jó alakú megoldsát csinál
    return np.array([row[0] for row in data])



def solveable(A,b,k,xbounds, NoSolution:list,checkeq = True, checkLP = True):
    NoSolution[2] +=1
    write_to_file(f"{xbounds}")  
    if checkLP:
        bounds = []
        for i in xbounds:
            bounds.append((i[0],i[1]))

        result = linprog(c=[0] * len(A[0]), A_eq=A, b_eq=b, bounds=bounds, method='highs')
        if not result.success:
            NoSolution[1] += "\n LP relaxáció hiba \n"
            write_to_file(" N \n")
            return False
        write_to_file(" Y \n")
    return True

def Smart_solver(A:np.array, b:np.array, k:int,checkeq = True, checkLP = True):
    
    # x inicializálása -1 értékekkel, oszlopszám szerint
    x = []
    for i in range(A.shape[1]):
        x.append([0,k])
    NoSolution = [True, "", 0, 0]  # Adatok a feladatról [0]: van-e megoldtás(fordítva) [1]: Dokumentáció [2]: Hány részfeladatot végeztem el [3]: egy x kiértékelése

    def __IP_solver__(A:np.array, b:np.array, k:int, x, NoSolution:list, checkeq = True, checkLP = True):
        stuff_to_do = []

        if any(z[0] != z[1] for z in x):
            i = 0
            while x[i][1] == x[i][0]:
                i += 1
            x1 = copy.deepcopy(x) # a sima x.copy() parancs beágyazott listák esetén létrehoz egy új listát ami az eredeti elemire mutat. A deepcopy teljesen új objektumot csinál minden esetben
            x2 = copy.deepcopy(x)
            x1[i] = [x[i][0], x[i][0] + math.floor((x[i][1]-x[i][0])/2)]
            x2[i] = [x[i][0] + math.ceil((x[i][1]-x[i][0])/2),x[i][1]]
            if any(z[0] != z[1] for z in x1):
                if solveable(A,b,k,x1,NoSolution, checkeq= checkeq, checkLP= checkLP):
                        stuff_to_do.append((A, b, k, x1, NoSolution, checkeq, checkLP))
                        while stuff_to_do and NoSolution[0]:
                                nextone = stuff_to_do.pop()
                                __IP_solver__(*nextone)
                else:
                        NoSolution[1] += f": A {x1} tartomány nem tartalmaz törtmegoldást"                        
            else:
                NoSolution[3] +=1
                x0 = convert_to_vector(x1)
                if np.allclose(A @ x0, b):
                    NoSolution[0] = False
                    stuff_to_do = []
                    write_to_file(f"{x0} Y\n")
                    NoSolution[1] = str(x0) + "\n Megoldja a rendszert \n"
                else:
                    write_to_file(f"{x0} N\n")
                    NoSolution[1] += " " + str(x0) + "\n nem megoldás \n"
            
            if NoSolution[0]:
                if any(z[0] != z[1] for z in x2):
                    if solveable(A,b,k,x2,NoSolution, checkeq= checkeq, checkLP= checkLP):
                            stuff_to_do.append((A, b, k, x2, NoSolution, checkeq, checkLP))
                            while stuff_to_do and NoSolution[0]:
                                    nextone = stuff_to_do.pop()
                                    __IP_solver__(*nextone)
                    else:
                            NoSolution[1] += f": A {x2} tartomány nem tartalmaz törtmegoldást"                        
                else:
                    NoSolution[3] +=1
                    x0 = convert_to_vector(x2)
                    if np.allclose(A @ x0, b):
                        NoSolution[0] = False
                        stuff_to_do = []
                        write_to_file(f"{x0} Y\n")
                        NoSolution[1] = str(x0) + "\n Megoldja a rendszert \n"
                    else:
                        write_to_file(f"{x0} N\n")
                        NoSolution[1] += " " + str(x0) + "\n nem megoldás \n"
        else:
            NoSolution[3] +=1
            x = convert_to_vector(x)
            if np.allclose(A @ x, b):
                NoSolution[0] = False
                stuff_to_do = []
                NoSolution[1] = str(x) + "\n Megoldja a rendszert \n"
            else:
                NoSolution[1] += " " + str(x) + "\n nem megoldás \n"
        
    __IP_solver__(A, b, k, x,NoSolution, checkeq= checkeq, checkLP= checkLP)
    NoSolution[1] = f" Elvégzett részfeledatok: {NoSolution[2]}; Feladat megoldható: {not NoSolution[0]}; " + NoSolution[1]
    write_to_file("END\n\n")
    return NoSolution[1], not NoSolution[0], NoSolution[2], NoSolution[3]


