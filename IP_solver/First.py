import numpy as np
import io
k = 5
A = np.array([[11,12],[21,22],[31,32]])
b = np.array([0,2,4])
c = np.array([0,-1,4])

x, s, q, d = np.linalg.lstsq(A,b)
is_exact = np.allclose(A @ x, b)
print(is_exact)
#z = np.delete(b,0,axis=1)
#print(z)
print("")
Anew = A[:,0] * 3
newb = b- Anew
thing = []
thing2 = [0,0,0]
bnew = b - A[:,0] * 3

litsa = [1,2,3,4]
for i in range(2):
    print(litsa.pop())
print(Anew)
print(bnew.shape)
print(bool(thing),bool(thing2))

def s(a:int):
    return a, "b", False

x0 = s(5)
print(x0)

dolog = [True , "szöveg"]

def osztaly(dolog):
    dolog[1] += "alma"

osztaly(dolog)

print(dolog[1])
x = []
for i in range(A.shape[1]):
    x.append(list(range(k)))
print(x)