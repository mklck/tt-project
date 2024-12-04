import math

from dataclasses	import dataclass
from sympy		import mod_inverse, randprime
from typing		import Tuple

@dataclass
class RSAKey:
	length		: int
	public		: int
	exponent	: int
	private		: int
	modulus         : int

class RSAKeyGenerator:
	def __init__(self, keyLength = 1024):
		self.keyLength = keyLength

	def generateKeys(self) -> RSAKey:
		p, q = self.generatePQ()
		self.n = p * q
		self.totient = (p - 1) * (q - 1)
		self.exponent = self.getExponent()
		self.d = mod_inverse(self.exponent, self.totient)

		return RSAKey(
			length = self.keyLength,
			public = self.n,
			exponent = self.exponent,
			private = self.d,
                        modulus = self.n
		)
		
	def generatePQ(self) -> Tuple[int, int]:
		p = self.getRandomPrime()
		cond = True
		while cond:
			q = self.getRandomPrime()
			cond = (p == q)
		return p, q

	def getExponent(self) -> int:
		for e in range(2**16 + 1, self.totient):
			if math.gcd(e, self.totient) == 1:
				return e
		raise ValueError("Can't find exponent")

				
	def getRandomPrime(self) -> int:
		min_ = 2 ** ((self.keyLength/2) - 1)
		max_ = (2 ** (self.keyLength/2)) - 1
		return randprime(min_, max_)


class RSA:
	def __init__(self, key : RSAKey):
		self.key = key
		
	def encrypt(self, msg : bytes) -> bytes:
		return  (pow(int.from_bytes(msg),self.key.exponent,self.key.modulus)).to_bytes(math.ceil(self.key.length/8));

	def decrypt(self, msg : bytes) -> bytes:
                return  (pow(int.from_bytes(msg),self.key.private,self.key.modulus)).to_bytes(math.ceil(self.key.length/8));
		

