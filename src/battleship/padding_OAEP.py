import hashlib
import random
from datetime import datetime

def random_seed(length = 64) -> bytes:
    random.seed(datetime.now().timestamp());
    return random.randbytes(length)

def mgf1(seed: bytes, length = 191, hash_func=hashlib.sha3_512) -> bytes:
    """Mask generation function."""
    hLen = hash_func().digest_size
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
        T += hash_func(seed + C).digest()
        counter += 1
    # 4. Output the leading l octets of T as the octet string mask.
    return T[:length];
    
def XOR(a: bytes, b: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(a, b))

def padding_OAEP(seed: bytes, M: bytes, modulusLength = 256, label="", hash_func=hashlib.sha3_512 ) -> bytes:
    # 256B modulus = 1B + 64B( Hash(seed) ) + 191B MGF{ 64B Hash(L)  + 1B + 30B Padding + 96B Message }

    psLength = modulusLength - 2*hash_func().digest_size - 2 - len(M);

    prefix = (0).to_bytes();
    mgfSeed = mgf1(seed);
    
    hashLabel = hashlib.sha3_512(label.encode()).digest();
    zeroPadding = bytearray(psLength);
    insider = (1).to_bytes();
    DB = hashLabel + zeroPadding + insider + M;

    
    maskedDB = XOR(DB,mgfSeed);
    maskedSeed = XOR( seed , mgf1(maskedDB,64) );

    return (prefix + maskedSeed + maskedDB);

def encode_OAEP(paddedMessage: bytes, messageLength = 96 , modulusLength = 256, hash_func=hashlib.sha3_512 ) -> bytes:
    maskedSeed = paddedMessage[1:65];
    maskedDB = paddedMessage[65:];

    seedMask = mgf1(maskedDB,64);
    seed = XOR(maskedSeed,seedMask);

    dbMask = mgf1(seed);
    DB = XOR(maskedDB,dbMask);

    return DB[messageLength-1:];
    

### n = 256B , hLen = 64B, M=96B, PS = 256 - 96 - 128 - 2 = 30B

if __name__=="__main__":
    for x in range(0, 10):
        message = random_seed(96);     
        paddedMessage = padding_OAEP(  random_seed() , message );
        encoded = encode_OAEP(paddedMessage);
        
        if encoded == message:
            print("Passed");
        else:
            print("Failed");

