from wallet import Wallet
from blockchain import SimpleBlockchain, Transaction

def main():
    print("=== MONETA VIRTUALE DIDATTICA CON RSA ===\n")
    
    # 1. Crea la blockchain
    blockchain = SimpleBlockchain()
    
    # 2. Crea due utenti
    print("1. Creazione portafogli...")
    alice = Wallet("Alice")
    bob = Wallet("Bob")
    
    # 3. Genera le chiavi RSA
    alice.generate_keys()
    bob.generate_keys()
    
    print(f"\n2. Alice ha: {alice.balance} coin")
    print(f"   Bob ha: {bob.balance} coin")
    
    # 4. Alice mina un blocco e riceve ricompensa
    print("\n3. Alice mina un blocco...")
    blockchain.mine_pending_transactions(alice.get_public_key_pem())
    alice.balance += 10 #Ricompensa semplificata
    
    # 5. Alice invia monete a Bob
    print("\n4. Alice invia 5 coin a Bob...")

    #Crea la transazione
    transaction = Transaction(
        alice.get_public_key_pem(),
        bob.get_public_key_pem(),
        5
    )
    
    # Prepara la transazione
    tx_data = {
        'sender': alice.get_public_key_pem(),
        'receiver': bob.get_public_key_pem(), 
        'amount': 5
    }
    signature = alice.sign_transaction(tx_data, transaction.timestamp)
    
    #Aggiungi la firma 
    transaction.signature = signature

    print(f"Firma creata: {signature[:50]}...")
    print(f"Transazione valida? {transaction.is_valid()}")
    
    #Aggiungi alla blockchain
    if blockchain.add_transaction(transaction):
        #Aggiorna i saldi (semplificato)
        alice.balance -= 5
        bob.balance += 5
        print("Transazione accettata!")
    else:
        print("Transazione rifiutata!")
    
    # 6. Bob mina un nuovo blocco
    print("\n5. Bob mina un blocco...")
    blockchain.mine_pending_transactions(bob.get_public_key_pem())
    bob.balance += 10 #Ricompensa

    # 7. Mostra risultati finali
    print(f"\n6. Saldo finale:")
    print(f"   Alice: {alice.balance} coin")
    print(f"   Bob: {bob.balance} coin")
    
    # 8. Verifica la blockchain
    print("\n7. Verifica integrità blockchain...")
    blockchain.is_chain_valid()
    
    # 9. Mostra la blockchain
    print("\n8. Blockchain creata:")
    blockchain.display_chain()

if __name__ == "__main__":
    main()