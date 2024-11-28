import hashlib
import random
from datetime import datetime

class OAEP:
        def __init__(self, messageLength, modulusLength = 1024, hash_func=hashlib.sha256):
            self.modulusLength = modulusLength;
            self.hash_func = hash_func;
            self. messageLength = messageLength;
		
	# Frame = 128B, Message = 32B, Hash=32B, ZeroPadding=30B
	
        def random_seed(self, length) -> bytes:
            random.seed(datetime.now().timestamp());
            return random.randbytes(length)

        def mgf1(self, seed: bytes, length = 95) -> bytes:
            """Mask generation function."""
            hLen = self.hash_func().digest_size;
            # https://www.ietf.org/rfc/rfc2437.txt
            # 1. If l > 2^32(hLen), output "mask too long" and stop.
            if length > (hLen << 32):
                raise ValueError("mask too long")
            # 2. Let T be the empty octet string.
            T = b""
            # 3. For counter from 0 to \lceil{l / hLen}\rceil-1, do the following:
            # Note: \lceil{l / hLen}\rceil-1 is the number of iterations needed,
            #       but it's easier to check if we have reached the desired length.
            counter = 0
            while len(T) < length:
                # a. Convert counter to an octet string C of length 4 with the primitive I2OSP: C = I2OSP (counter, 4)
                C = int.to_bytes(counter, 4, "big")
                # b. Concatenate the hash of the seed Z and C to the octet string T: T = T || Hash (Z || C)
                T += self.hash_func(seed + C).digest()
                counter += 1
            # 4. Output the leading l octets of T as the octet string mask.
            return T[:length];
            
        def XOR(self, a: bytes, b: bytes) -> bytes:
            return bytes(a ^ b for a, b in zip(a, b))

        def padding_OAEP(self, seed: bytes, M: bytes, label="" ) -> bytes:
            hLen = self.hash_func().digest_size;
            psLength = self.modulusLength - 2*hLen - 2 - len(M);

            prefix = (0).to_bytes();
            mgfSeed = self.mgf1(seed, self.modulusLength -1 - hLen);
            
            hashLabel = self.hash_func(label.encode()).digest();
            zeroPadding = bytearray(psLength);
            insider = (1).to_bytes();
            DB = hashLabel + zeroPadding + insider + M;
            
            maskedDB = self.XOR(DB,mgfSeed);
            maskedSeed = self.XOR( seed , self.mgf1(maskedDB,hLen) );
            
            return (prefix + maskedSeed + maskedDB);

        def encode_OAEP(self, paddedMessage: bytes) -> bytes:
            hLen = self.hash_func().digest_size;

            maskedSeed = paddedMessage[1:hLen + 1];
            maskedDB = paddedMessage[hLen + 1:];

            seedMask = self.mgf1(maskedDB,hLen);
            seed = self.XOR(maskedSeed,seedMask);

            dbMask = self.mgf1(seed,self.modulusLength -1 - hLen);
            DB = self.XOR(maskedDB,dbMask);

            return DB[self.modulusLength-self.messageLength-hLen -1:];
    

if __name__== "__main__":
    padding = OAEP(32);
    for x in range(0, 10):
        message = padding.random_seed(32);

        paddedMessage = padding.padding_OAEP(  padding.random_seed(32) , message );
        print(len(paddedMessage));
        encoded = padding.encode_OAEP(paddedMessage);

        if encoded == message:
            print("Passed");
        else:
            print("Failed");

