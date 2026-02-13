from wallet import Wallet 
from blockchain import SimpleBlockchain, Transaction

def main():
    print("=== EDUCATIONAL VIRTUAL CURRENCY WITH RSA ===\n")
    
    # 1. Create blockchain instance
    blockchain = SimpleBlockchain()
    
    # 2. Create two users wallets
    print("1. Creating wallets...")
    alice = Wallet("Alice")
    bob = Wallet("Bob")
    
    # 3. Generate RSA key pairs for both users
    # These keys are used to sign transactions and verify identity
    alice.generate_keys()
    bob.generate_keys()
    
    print(f"\n2. Alice has: {alice.balance} coin")
    print(f"   Bob has: {bob.balance} coin")
    
    # 4. Alice mines a block and receives a mining reward
    # In a real blockchain, mining confirms pending transactions
    print("\n3. Alice mines a block...")
    blockchain.mine_pending_transactions(alice.get_public_key_pem())
    alice.balance += 10 # Simplified mining reaward simulation
    
    # 5. Alice sends coins to Bob
    print("\n4. Alice sends 5 coin to Bob...")

    # Create transaction object
    transaction = Transaction(
        alice.get_public_key_pem(),
        bob.get_public_key_pem(),
        5
    )
    
    # Prepare transaction data for signing
    tx_data = {
        'sender': alice.get_public_key_pem(),
        'receiver': bob.get_public_key_pem(), 
        'amount': 5
    }
    # Alice signs the transaction with her private key
    signature = alice.sign_transaction(tx_data, transaction.timestamp)
    
    # Attach the signature to the transaction 
    transaction.signature = signature

    print(f"Signature created: {signature[:50]}...")
    print(f"Is transaction valid? {transaction.is_valid()}")
    
    # Add the transaction to the blockchain
    if blockchain.add_transaction(transaction):
        # Update balances (simplified logic for demonstration)
        alice.balance -= 5
        bob.balance += 5
        print("Transaction accepted!")
    else:
        print("Transaction rejected!")
    
    # 6. Bob mines a new block to process the transaction
    print("\n5. Bob mines a block...")
    blockchain.mine_pending_transactions(bob.get_public_key_pem())
    bob.balance += 10 # Simplified mining reward
    
    # 7. Show final balances
    print(f"\n6. Final balances:")
    print(f"   Alice: {alice.balance} coin")
    print(f"   Bob: {bob.balance} coin")
    
    # 8. Verify blockchain integrity
    # Checks if hashes link correctly and if data has been tampered
    print("\n7. Verifying blockchain integrity...")
    blockchain.is_chain_valid()
    
    # 9. Display the entire blockchain structure
    print("\n8. Blockchain created:")
    blockchain.display_chain()

if __name__ == "__main__":

    main()
