import json#modulo json (Javascript Object notation) è una libreria standard di Python che fornisce le funzioni per codificare (convertire oggetti python in stringhe JSON) e decodificare
import hashlib#importa libreria che trasforma il testo in impronte digitali uniche (stringa di lettere e numeri)
import time#libreria che gestisce tutto ciò che riguarda tempo (legge l'ora corrente, mette in pausa il programma, misura il tempo di un'operazione, programma azioni per futuro).

#creiamo una classe Transaction in modo che un cliente sia in grado di inviare denaro a qualcuno.
#Si noti che un cliente può essere sia un mittente che un destinatario del denaro. Quando vuoi ricevere denaro, un altro mittente creerà una transazione e specificherà il tuo indirizzo pubblico in essa.
#Il metodo init accetta tre parametri: la chiave pubblica del mittente, la chiave pubblica del destinatario e l'importo da inviare. Questi vengono memorizzati nelle variabili di istanza per l'utilizzo da parte di altri metodi. Inoltre, creiamo un'altra variabile per memorizzare l'ora della transazione.

class Transaction:
    def __init__(self, sender, receiver, amount, signature=None):
        self.sender = sender  # Chiave pubblica del mittente
        self.receiver = receiver  # Chiave pubblica del destinatario
        self.amount = amount
        self.signature = signature
        self.timestamp = time.time()

#scriviamo un metodo di utilità chiamato to_dict che combina tutte e 'quattro' le variabili di istanza sopra menzionate in un oggetto dizionario. Questo serve solo a rendere accessibili tutte le informazioni sulla transazione attraverso una singola variabile

    def to_dict(self):
        """Converte la transazione in dizionario per la firma"""
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
# il primo blocco della blockchain è un blocco Genesis. Il blocco Genesis contiene la prima transazione avviata dal creatore della blockchain

    def is_valid(self):
        """Verifica se la transazione è valida"""
        if self.amount <= 0:
            return False
            
        # Crea una copia dei dati senza la firma per la verifica
        data_to_verify = self.to_dict()
        data_str = json.dumps(data_to_verify, sort_keys=True)
        
        try:
            from Crypto.PublicKey import RSA
            from Crypto.Signature import pkcs1_15
            from Crypto.Hash import SHA256
            import base64
            
            # Verifica la firma
            h = SHA256.new(data_str.encode('utf-8'))
            public_key = RSA.import_key(self.sender)
            signature = base64.b64decode(self.signature)
            pkcs1_15.new(public_key).verify(h, signature)
            return True
        except:
            return False

#definito la funzione init(), che è un metodo speciale che viene automaticamente chiamato quando viene creata una nuova istanza di una classe (=costruttore della classe)->inizializza gli attributi dell'oggetto, riceve parametri per configurare l'istanza, esegue operazioni necessarie alla creazione dell'oggetto
#self si riferisce all'istanza della classe Block, che consente di accedere ai metodi e agli attributi associati alla classe
#index tiene traccia della posizione del blocco all'interno della blockchain
#nonce è il numero prodotto durante la creazione di un nuovo blocco (chiamato mining)
#previous_hash si riferisce all'hash del blocco precedente all'interno della catena
#transactions fornisce una registrazione di tutte le transazioni completate, come la quantità acquistata
#timestamp è per le transazioni

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0  # Per il mining
        self.hash = self.calculate_hash()

#calculate_hash, genererà l'hash dei blocchi utilizzando i valori precedenti. Il modulo SHA-256 viene importato nel progetto per facilitare l'ottenimento degli hash dei blocchi.
#Dopo che i valori sono stati inseriti nell'algoritmo hash crittografico, la funzione restituirà una stringa a 256 bit che rappresenta il contenuto del blocco.
#Questo è il modo in cui si ottiene la sicurezza nelle blockchain: ogni blocco avrà un hash e quell'hash si baserà sull'hash del blocco precedente.
#Pertanto, se qualcuno tenta di compromettere qualsiasi blocco nella catena, gli altri blocchi avranno hash non validi, portando all'interruzione dell'intera rete blockchain.

    def calculate_hash(self):
        """Calcola l'hash del blocco"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [str(tx) for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

#La proof of work è un concetto che impedisce alla blockchain di abusare. Semplicemente, il suo obiettivo è identificare un numero che risolva un problema dopo che è stata eseguita una certa quantità di lavoro di calcolo.
#Se il livello di difficoltà nell'identificare il numero è alto, si scoraggia lo spamming e la manomissione della blockchain.

    def mine_block(self, difficulty=2):
        """Mini il blocco (Proof-of-Work semplificato)"""
        print(f"Minando blocco {self.index}...")
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Blocco minato! Hash: {self.hash}")

#L'idea principale di una blockchain, proprio come suggerisce il nome, prevede di "concatenare" diversi blocchi l'uno all'altro.
#self.chain: questa variabile mantiene tutti i blocchi
#self.pending_transactions: questa variabile mantiene tutte le transazioni completate nel blocco
#self.create_genesis_block(): questo metodo si occuperà della costruzione del blocco iniziale
#La blockchain richiede un metodo create_genesis_block per costruire il blocco iniziale nella catena. Nella convenzione blockchain, questo blocco è speciale perché simboleggia l'inizio della blockchain.
#(proof_no e prev_hash possono assumere qualsiasi valore, in questo caso c'è lo zero.)

class SimpleBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = 2
        self.mining_reward = 10#ricompensa mineraria
    
    def create_genesis_block(self):
        """Crea il primo blocco della catena"""
        return Block(0, ["GENESIS_BLOCK"], "0")

#il metodo del get_latest_block è un metodo di supporto che aiuta a ottenere l'ultimo blocco nella blockchain. Ricorda che l'ultimo blocco è in realtà il blocco corrente della catena.

    def get_latest_block(self):
        return self.chain[-1]

#Il metodo add_transaction utilizzato per aggiungere i dati delle transazioni a un blocco. 
#aggiunge i dati della transazione alla lista self.pending_transactions
#Ogni volta che viene creato un nuovo blocco, questo elenco viene allocato a quel blocco e reimpostato ancora una volta
#Una volta che i dati della transazione sono stati aggiunti all'elenco, viene restituito l'indice del blocco successivo da creare.
#Questo indice viene calcolato aggiungendo 1 all'indice del blocco corrente (che è l'ultimo nella blockchain). I dati aiuteranno l'utente a inviare la transazione in futuro.

    def add_transaction(self, transaction):
        """Aggiunge una transazione in attesa di essere minata"""
        if transaction.is_valid():
            self.pending_transactions.append(transaction)
            print("Transazione aggiunta con successo!")
            return True
        else:
            print("Transazione non valida!")
            return False
    
    def mine_pending_transactions(self, mining_reward_address):
        """Crea un nuovo blocco con le transazioni in sospeso"""
        block = Block(
            len(self.chain),#rappresenta la lunghezza della blockchain
            self.pending_transactions,
            self.get_latest_block().hash
        )
        
        block.mine_block(self.difficulty)
        self.chain.append(block)#Questo metodo unisce i blocchi appena costruiti alla catena
        
        # Resetta le transazioni in sospeso e aggiungi la ricompensa
        self.pending_transactions = []
        print(f"Ricompensa di {self.mining_reward} coin assegnata a {mining_reward_address[:20]}...")

#verifica della validità
#Il metodo is_chain_valid è importante per valutare l'integrità della blockchain e garantire l'assenza di anomalie.
#gli hash sono essenziali per la sicurezza della blockchain poiché anche il minimo cambiamento nell'oggetto porterà alla generazione di un hash completamente nuovo.
#Pertanto, questo metodo is_chain_valid utilizza le istruzioni if per verificare se l'hash di ogni blocco è corretto.
#Verifica anche se ogni blocco punta al blocco precedente corretto, confrontando il valore dei loro hash. Se tutto è corretto, restituisce true; In caso contrario, restituisce false.

    def is_chain_valid(self):
        """Verifica l'integrità della blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                print(f"Blocco {i} manomesso!")
                return False
                
            if current_block.previous_hash != previous_block.hash:
                print(f"Blocco {i} non collegato correttamente!")
                return False
                
        print("Blockchain integra!")
        return True
    
    def display_chain(self):
        """Mostra tutta la blockchain"""
        for block in self.chain:
            print(f"\n--- Blocco {block.index} ---")
            print(f"Hash: {block.hash}")
            print(f"Hash Precedente: {block.previous_hash}")
            print(f"Transazioni: {len(block.transactions)}")
            
