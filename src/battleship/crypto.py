from RSA import RSAKeyGenerator, RSA
import padding_OAEP as OAEP
import random, hashlib

class cryptographic:
        def __init__(self, messageLength, modulusLength = 128, hash_func=hashlib.sha256):
            # RSA section
            keyGen = RSAKeyGenerator();
            key = keyGen.generateKeys();
            self.RSA = RSA(key);

            #Padding
            self.padding = OAEP.OAEP( messageLength,modulusLength,hash_func)
            
        def encrypt (self, msg : bytes ) -> bytes:
            paddedMessage = self.padding.padding_OAEP( self.padding.random_seed(32) , msg);
            return self.RSA.encrypt(paddedMessage);
            
        def decrypt (self, cipher : bytes ) -> bytes:
            decryptedMessage = self.RSA.decrypt(cipher);
            return self.padding.encode_OAEP(decryptedMessage);
            

#print(str(key.modulus), " ",str(key.exponent), " ",str(key.private));

if __name__== "__main__":
    crypto = cryptographic(32);
    for x in range(0, 10):

        # szyfrowanie exponent, deszyfrowanie private
        message = crypto.padding.random_seed(32);
        cipher = crypto.encrypt(message,crypto.RSA.key.exponent);
        recoverMessage = crypto.decrypt(cipher,crypto.RSA.key.private);

        if message == recoverMessage:
            print("Passed");
        else:
            print("Failed");

        # i w drugą stronę...
        message = crypto.padding.random_seed(32);
        cipher = crypto.encrypt(message,crypto.RSA.key.private);
        recoverMessage = crypto.decrypt(cipher,crypto.RSA.key.exponent);

        if message == recoverMessage:
            print("Passed");
        else:
            print("Failed");
        
        
    
