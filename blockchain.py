import json # Data serialization
import hashlib # Cryptographic hashing
import time # Timestamp generation

class Transaction:
    def __init__(self, sender, receiver, amount, signature=None):
        self.sender = sender  # Sender's public key (PEM format)
        self.receiver = receiver  # Receiver's public key (PEM format)
        self.amount = amount # Amount to transfer
        self.signature = signature # Digital signature from sender's wallet
        self.timestamp = time.time() # Temporal ordering

    def to_dict(self):
        """Converts transaction to dictionary for signature generation"""
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
        
    def is_valid(self):
        """Verifies transaction authenticity and integrity"""
        if self.amount <= 0:
            return False
            
        # Create a copy of the data without the signature for verification
        data_to_verify = self.to_dict()
        data_str = json.dumps(data_to_verify, sort_keys=True)

        # Signature verification process
        try:
            from Crypto.PublicKey import RSA
            from Crypto.Signature import pkcs1_15
            from Crypto.Hash import SHA256
            import base64
            
            # Recompute hash from transaction data
            h = SHA256.new(data_str.encode('utf-8'))
            # Import sender's public key
            public_key = RSA.import_key(self.sender)
            # Decode signature from Base64
            signature = base64.b64decode(self.signature)
            # Verify RSA signature
            pkcs1_15.new(public_key).verify(h, signature)
            return True
        except:
            return False

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index # Position in the chain
        self.timestamp = time.time() # Block creation time
        self.transactions = transactions # List of transaction objects
        self.previous_hash = previous_hash # Link to previous block
        self.nonce = 0  # Proof-of-work counter (for mining)
        self.hash = self.calculate_hash() # Self-reference

    def calculate_hash(self):
        """Cryptographic fingerprint of entire block contents"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [str(tx) for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty=2):
        """Finds a valid nonce through computational work"""
        print(f"Mining block {self.index}...")
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined! Hash: {self.hash}")

class SimpleBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()] # Immutable block history
        self.pending_transactions = [] # Unconfirmed transactions
        self.difficulty = 2 # Security parameter
        self.mining_reward = 10 # Economic incentive
    
    def create_genesis_block(self):
        """Creates the first block in the chain"""
        return Block(0, ["GENESIS_BLOCK"], "0")

    def get_latest_block(self):
        """Helper method to access current tip of chain"""
        return self.chain[-1]

    def add_transaction(self, transaction):
        """Adds validated transaction to mining queue"""
        if transaction.is_valid():
            self.pending_transactions.append(transaction)
            print("Transaction added successfully!")
            return True
        else:
            print("Invalid transaction!")
            return False
    
    def mine_pending_transactions(self, mining_reward_address):
        """Creates new block with pending transactions"""
        block = Block(
            len(self.chain), # Blockchain length
            self.pending_transactions,
            self.get_latest_block().hash
        )
        
        block.mine_block(self.difficulty)
        self.chain.append(block) # Append to chain
        
        # Reset pending transactions for next block
        self.pending_transactions = []
        print(f"Reward of {self.mining_reward} coin awarded to {mining_reward_address[:20]}...")

    def is_chain_valid(self):
        """Blockchain integrity verification"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Check 1: block hash integrity
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {i} has been tampered with!")
                return False

            # Check 2: chain linkage integrity
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {i} has broken link to previous block!")
                return False
                
        print("Blockchain is intact and valid!")
        return True
    
    def display_chain(self):
        """Human-readable blockchain output"""
        for block in self.chain:
            print(f"\n--- Block {block.index} ---")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Transactions: {len(block.transactions)}")
            

