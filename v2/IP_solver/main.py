import numpy as np
from output import Write ,Writeshort
from input import read_matrix_from_file
from Branch_andbound import IP_solver
from Smartbranches import Smart_solver
from Sample import createrndsample

"""Parameters:
    model:string                            #Which solver should run, can be "legacy", "both" (runs one the other on teh same task), or "smart" by deafult
    long:bool                               #The style of description in the output.txt file
    Samplecreation:bool                     #If set True the program wipes the input.txt and fills it with a randomly generated sample of exercies according to the Sample
    Sample:iterable                         #n, m, k, size = 10, Percentage_of_wrong = 50. Extra parameters can be set with rewriting the function call in row 44
    checkeq:bool                            #Applies to legacy only. Determines if it should check The Linear equation: {x:Ax=b} != <Emptyset> at subtasks
    checkLP:bool                            #Determines if it should check the LP: {x:Ax=b, x >= 0} != <Emptyset> at subtasks
"""


model = "both"                              #Which solver should run, can be "legacy", "both" (runs one the other on teh same task), or "smart" by deafult
long = False                                #The style of description in the output.txt file
Samplecreation = True                       #If set True the program wipes the input.txt and fills it with a randomly generated sample of exercies according to the Sample
Sample = [1, 5 ,5, 1, 50]              #n, m, k, size = 10, Percentage_of_wrong = 50. Extra parameters can be set with rewriting the function call in row 51
checkeq = True                              #Applies to legacy only. Determines if it should check The Linear equation: {x:Ax=b} != <Emptyset> at subtasks
checkLP = True                              #Determines if it should check the LP: {x:Ax=b, x >= 0} != <Emptyset> at subtasks




def Program(model, long, Samplecreation, Sample, checkeq, checkLP):
    #setting up things related to the model
    both = False
    smart = True
    if model == "both":
        both = True
        smart = False
    elif model != "legacy":
        smart = False



    if Samplecreation:
        with open("input.txt", "w", encoding="utf-8") as f: #Wiping input file
            pass
        # Sample creation (n, m, k, size, Percentage_of_wrong = 50, file = "input.txt", start = -100, end = 100)
        createrndsample(*Sample)


    #Wiping the output files:
    with open("output.txt", "w", encoding="utf-8") as f:
        pass
    with open("log.txt", "w", encoding="utf-8") as f:
        pass

    #Running the alg with the right modell
    if not both: 
        Matrices = read_matrix_from_file()
        for M in Matrices:
            id_value, A, b, k = M
            if smart:
                Solution, _, _ = Smart_solver(A, b, k,checkeq= checkeq, checkLP= checkLP)
            else:
                Solution, _, _ = IP_solver(A, b, k,checkeq= checkeq, checkLP= checkLP)
            if long:
                Write(id_value,A,b,k,Solution)
            else:
                Writeshort(Solution)
    else:
            Writeshort("Smart:")
            Problemcounter = 0
            totallsteps = 0
            goodtotallsteps = 0
            badtotallsteps = 0
            totallevals = 0
            Matrices = read_matrix_from_file()
            for M in Matrices:
                Problemcounter +=1
                id_value, A, b, k = M
                if True:
                    Solution, solvable, steps, evalx = Smart_solver(A, b, k,checkeq= checkeq, checkLP= checkLP)
                    totallsteps += steps
                    totallevals += evalx
                    if solvable:
                        goodtotallsteps += steps
                    else:
                        badtotallsteps += steps
                else:
                    Solution, solvable, steps, evalx = IP_solver(A, b, k,checkeq= checkeq)
                    totallsteps += steps
                    totallevals += evalx
                    if solvable:
                        goodtotallsteps += steps
                    else:
                        badtotallsteps += steps
                if long: #Writing to output in the right format
                    Write(id_value,A,b,k,Solution)
                else:
                    Writeshort(Solution)
            Writeshort(f"Összlépés: {totallsteps}, Lépés jó megoldásokon: {goodtotallsteps}, Lépés nem megoldhatókon: {badtotallsteps}, Kiértékelések: {totallevals}")

            Writeshort("Legacy:")
            Matrices = read_matrix_from_file()
            ProblemcounterL = 0
            totallstepsL = 0
            goodtotallstepsL = 0
            badtotallstepsL = 0
            totallevalsL = 0
            for M in Matrices:
                ProblemcounterL +=1
                id_value, A, b, k = M
                if False:
                    Solution, solvable, steps, evalx = Smart_solver(A, b, k,checkeq= checkeq)
                    totallsteps += steps
                    totallevals += evalx
                    if solvable:
                        goodtotallsteps += steps
                    else:
                        badtotallsteps += steps
                else:
                    Solution, solvable, steps, evalx = IP_solver(A, b, k,checkeq= checkeq, checkLP= checkLP)
                    totallstepsL += steps
                    totallevalsL += evalx
                    if solvable:
                        goodtotallstepsL += steps
                    else:
                        badtotallstepsL += steps
                if long: #Writing to output in the right format
                    Write(id_value,A,b,k,Solution)
                else:
                    Writeshort(Solution)
            Writeshort(f"Összlépés: {totallstepsL}, Lépés jó megoldásokon: {goodtotallstepsL}, Lépés nem megoldhatókon: {badtotallstepsL}, Kiértékelések: {totallevalsL}")
            return totallstepsL / ProblemcounterL, totallevalsL / ProblemcounterL , totallsteps / Problemcounter, totallevals / Problemcounter, 
        

Program(model, long, Samplecreation, Sample, checkeq, checkLP)