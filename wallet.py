from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64 # ASCII encoding of binary signatures
import time
import json # Structured data serialization

class Wallet:
    def __init__(self, name):
        self.name = name # Identifier for the wallet owner
        self.private_key = None
        self.public_key = None
        self.balance = 100  # Initial balance for testing purposes
        
    def generate_keys(self):
        """Generates RSA key pair (2048 bit)"""
        key = RSA.generate(2048)
        self.private_key = key
        self.public_key = key.publickey()
        print(f"{self.name}: Keys generated successfully!")
        return self.public_key
        
    def sign_transaction(self, transaction_data, timestamp=None):
        """Digitally signs a transaction using the wallet's private key"""
        if not self.private_key:
            print("Please generate keys first!")
            return None
            
        # Timestamp for non-repudiation
        if timestamp is None:
            timestamp = time.time()
            
        # Structured the transaction data
        data_to_sign = {
            'sender': transaction_data['sender'],
            'receiver': transaction_data['receiver'],
            'amount': transaction_data['amount'],
            'timestamp': timestamp
        }
        # Serialize to deterministic JSON string
        data_str = json.dumps(data_to_sign, sort_keys=True)
        # Create SHA-256 hash
        h = SHA256.new(data_str.encode('utf-8'))
        # Sign the hash with private key
        signature = pkcs1_15.new(self.private_key).sign(h)
        # Encode to ASCII-friendly format
        return base64.b64encode(signature).decode('ascii')
    
    def get_public_key_pem(self):
        """Returns the public key in PEM format for sharing"""
        if self.public_key:
            return self.public_key.export_key().decode('ascii')

        return None
