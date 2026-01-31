from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import time
import json

#La classe Wallet genera le chiavi private e pubbliche utilizzando l'algoritmo RSA Python integrato.
#Tieni presente che non dovresti mai perdere la tua chiave privata. Per la conservazione dei registri, la chiave privata generata può essere copiata su un archivio esterno protetto oppure è possibile annotare semplicemente la rappresentazione ASCII su un foglio di carta.

class Wallet:
    def __init__(self, name):
        self.name = name
        self.private_key = None
        self.public_key = None
        self.balance = 100  # Saldo iniziale per testing
        
    def generate_keys(self):
        """Genera chiavi RSA"""
        key = RSA.generate(2048)
        self.private_key = key
        self.public_key = key.publickey()
        print(f"{self.name}: Chiavi generate!")
        return self.public_key

#firmeremo questo oggetto dizionario utilizzando la chiave privata del mittente. Come in precedenza, utilizziamo l'algoritmo PKI integrato con SHA. La firma generata viene decodificata per ottenere la rappresentazione ASCII per la stampa e l'archiviazione nella nostra blockchain.

    def sign_transaction(self, transaction_data, timestamp=None):
        """Firma una transazione"""
        if not self.private_key:
            print("Prima genera le chiavi!")
            return None
        
        if timestamp is None:
            timestamp = time.time()

        data_to_sign = {
            'sender': transaction_data['sender'],
            'receiver': transaction_data['receiver'],
            'amount': transaction_data['amount'],
            'timestamp': timestamp
        }
        # Converti i dati in stringa per firmare
        data_str = json.dumps(data_to_sign, sort_keys=True)
        # Crea l'hash
        h = SHA256.new(data_str.encode('utf-8'))
        # Firma con chiave privata
        signature = pkcs1_15.new(self.private_key).sign(h)
        # Converti in base64 per facilità di gestione
        return base64.b64encode(signature).decode('ascii')
    
    def get_public_key_pem(self):
        """Restituisce la chiave pubblica in formato leggibile"""
        if self.public_key:
            return self.public_key.export_key().decode('ascii')
        return None