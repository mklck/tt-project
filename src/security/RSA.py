import math

def gcd(b, a):
        r = b % a;
        if r == 0:
            return a;
        else:
            return gcd (a ,r);

def gcd_extended(a,b):
        x = 1; y = 0;
        x1 = 0; y1 = 1; a1 = a; b1 = b;     
        while b1 != 0:
                q = math.floor(a1/b1);        
                x, x1 = x1, x - q * x1;
                y, y1 = y1, y - q * y1;
                a1, b1 = b1, a1 - q * b1;
                
        return  x;
                
def totient_function(p ,q): # Only for primes
        return int((p-1)*(q-1)/gcd(p-1,q-1));

def generateRSA_Keys (p,q,e):
        totient = totient_function(p ,q);
        print("Publick keys n=",str(p*q), " e= ", str(e));
        d = gcd_extended(e,totient);
        print("Private keys d=", str(d));

def RSA_encode (m,n,e):
        return (m^e)%n;

def RSA_decode (c,n,d):
        return (c^d)%n;
