"""
Wipes given txt file (file = "input.txt") and fills it with random IP exercises according to the parameters
    n: Number of columns in A
    m: Numbers of rows
    k: max value of x
    size: Number of IPs to be created
    Percentage_of_wrong: Percentage of IPs in the sample NOT GAURANTED to be solveable, that does not means this is the percentage of nosolvable exercises (maybe inverted) 
    file: the given file
    start, end: the intervall from which A and b can get their elements
"""

import numpy as np
def indicator(p): #an indicator probability distribution
    if np.random.randint(0,100) < p:
        x = 1
    else:
        x = 0
    return x

def createrndsample(n = 5, m = 5, k = 10, size = 10, Percentage_of_wrong = 50, file = "input.txt", start = -100, end = 100):
    with open(file, "a", encoding="utf-8") as f:
        def write_to_file(text):

                f.write(str(text) + "\n")

        def idgiver(): #id generator
            i = 0
            while True:
                i +=1
                yield i
        
        def write_record(A,b,k,id):
            write_to_file("id:")
            write_to_file(id)
            write_to_file("A:")
            for j in A:
                f.write(", ".join(map(str, j)) + "\n")
            write_to_file("b:")
            for i in b:
                for j in i:
                    write_to_file(j)
            write_to_file("k:")
            write_to_file(str(k))
            write_to_file("---------")
        
        idstore = idgiver()

        #The program generates IP-s with taking a random x vector and a random A and then we set b to Ax which means x is a solution. Then we take a sample from indicator(p) and if it returns True we distort b with a random vector making x no longer a solution.
        for j in range(size):
            A = np.random.randint(start, end, (m,n))
            x = np.random.randint(0, k, (n,1))
            b = A @ x
            if Percentage_of_wrong != 0:
                b = A @ x - (np.random.randint(-k* 0.05-1, k*0.05 +2, (m,1)) *indicator(Percentage_of_wrong))
            id = next(idstore)
            write_record(A,b,k,id)




    

