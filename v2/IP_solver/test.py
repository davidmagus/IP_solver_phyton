from main import Program
from visual import visual

"""Parameters:
    model:string                            #Which solver should run, can be "legacy", "both" (runs one the other on teh same task), or "smart" by deafult
    long:bool                               #The style of description in the output.txt file
    Samplecreation:bool                     #If set True the program wipes the input.txt and fills it with a randomly generated sample of exercies according to the Sample
    Sample:iterable                         #n, m, k, size = 10, Percentage_of_wrong = 50. Extra parameters can be set with rewriting the function call in row 44
    checkeq:bool                            #Applies to legacy only. Determines if it should check The Linear equation: {x:Ax=b} != <Emptyset> at subtasks
    checkLP:bool                            #Determines if it should check the LP: {x:Ax=b, x >= 0} != <Emptyset> at subtasks
"""


with open("data.txt", "a") as f:
    for n in [1,2,3,4,5,6,7,8,9]:
        for k in [9]:
            L, _, S, _ = Program("both",False,True, [n, 5 ,k, 1, 50], True, True)
            eff1 = L      # Példa: egyszerű szorzat
            eff2 = S      # Példa: egyszerű összeg
            f.write(f"{n} {k} {eff1} {eff2}\n")

visual()