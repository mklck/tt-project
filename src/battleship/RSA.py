import math

class RSA:
        def __init__ (self,p,q,n,e): # w przypadku inicjalizacji po stronie publicznej p=q=0
                self.n = n;
                self.e = e;
                self.p = p;
                self.q = q;
                
        def gcd(self,b, a):
                r = b % a;
                if r == 0:
                        return a;
                else:
                        return self.gcd(a ,r);

        def gcd_extended(self,a,b):
                x = 1; y = 0;
                x1 = 0; y1 = 1; a1 = a; b1 = b;     
                while b1 != 0:
                        q = math.floor(a1/b1);        
                        x, x1 = x1, x - q * x1;
                        y, y1 = y1, y - q * y1;
                        a1, b1 = b1, a1 - q * b1;
                return  x;
                
        def RSA_encode (m,n,e):
                return ((m**self.e)%self.n);

        def RSA_decode (m):
                return (c**self.d)%self.n;

        def totient_function(self, p ,q): # Only for primes
                return int((p-1)*(q-1)/self.gcd(p-1,q-1));
        
        def generateKeys(self):
                print("Publick keys n=",str(self.n), " e= ", str(self.e));
                if self.p != 0:
                        totient = self.totient_function(self.p ,self.q);
                        self.private = self.gcd_extended(self.e,totient);
                        print("Private key d=", str(self.private));



p = 61; q = 53;
serwer = RSA(p,q,p*q,37);
serwer.generateKeys();

#private = generateRSA_Keys(61,53,37);



