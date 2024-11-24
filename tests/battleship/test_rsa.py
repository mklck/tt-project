from battleship import RSAKey, RSAKeyGenerator, RSA

import pytest

class TestRSAKeyGenerator:
	def test_generateKeys(self):
		gen = RSAKeyGenerator(keyLength=1024)
		keys = gen.generateKeys()
		print(keys)

class TestRSA:
	pass
