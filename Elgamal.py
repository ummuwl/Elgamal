INF_POINT = None

class Elgamal:

    def __init__(self, nilai_a, nilai_b, p, P):
        self.nilai_a = nilai_a
        self.nilai_b = nilai_b
        self.p = p
        self.P = P
        

    def reduceModp(self, x):
        return x % self.p

    def equalModp(self, x, y):
        return self.reduceModp(x-y) == 0

    def inversModp(self,x):
        for y in range(self.p):
            if self.equalModp(x * y, 1):
                return y
        return None


    def jumlah(self, P1, P2):
        if P1 == INF_POINT:
            return P2
        if P2 == INF_POINT:
            return P1

        x1 = P1[0]
        y1 = P1[1]
        x2 = P2[0]
        y2 = P2[1]

        if self.equalModp(x1, x2) and self.equalModp(y1, -y2):
            return INF_POINT

        if self.equalModp(x1, x2) and self.equalModp(y1, y2):
            u = self.reduceModp((3 * x1 * x1 + self.nilai_a) * self.inversModp (2 * y1))  
        else:
            u = self.reduceModp((y1 - y2) * self.inversModp(x1 - x2)) 

    
        v = self.reduceModp(y1 - u * x1)
        x3 = self.reduceModp(u * u - x1 - x2)
        y3 = self.reduceModp(-u * x3 - v )

        return(x3, y3)

    def ganda(self, P, n):
        L,N = P, INF_POINT
        while n > 0:
            if n%2 == 1: 
                N = self.jumlah(N,L)
            L = self.jumlah(L,L)
            n = n//2
        return N

    def neg(self, A):
        x, y = A
        return (x, -y % self.p)
    
    def pubKey(self, privKey):
        return self.ganda(self.P, privKey)
    
    def enc(self, M, pubKey, k):
        return (self.ganda(self.P, k), self.jumlah(M, self.ganda(pubKey,k)))

    def dec(self, C1, C2, d): 
        return self.jumlah(C2, self.neg(self.ganda(C1,d)))
