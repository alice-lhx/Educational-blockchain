# Educational-blockchain
A Python implementation of a simplified blockchain cryptocurrency demonstrating the mathematical principles of asymmetric cryptography (RSA), distributed ledgers and consensus mechanism.

## Project overview
This repository bridges the gap between abstract mathematical theories - specifically **Number Theory** and **Modular Arithmetic** - and practical Computer Science applications. 
Unlike production cryptocurrencies optimized for speed, this project is optimized for **readability and educational value**. It explicitly visualizes how:
1. RSA key pairs are generated
2. Digital signatures authticate transactions
3. Proof of Work (PoW) secures the history of the ledger

## Scientific concepts
### 1. RSA & digital signatures (asymmetric cryptography)
The security of user funds relies on the RSA algorithm. 
*   **Theory:** security is based on the computational difficulty of factoring large integers (the product of two large primes $p$ and $q$).
*   **Implementation:** 
    *   Users generate a public/private key pair
    *   Transactions are signed using the private key
    *   The network verifies the signature using the public key
### 2. The Immutable Ledger (Hashing)
The blockchain is a linked list where every block contains the **SHA-256 hash** of the previous block.
*   **Theory:** a hash function maps data of arbitrary size to fixed-size values. It is deterministic but irreversible (One-way function).
*   **Implementation:** any alteration to a past transaction changes the block's hash, invalidating all subsequent blocks and alerting the network to tampering.
### 3. Consensus (Proof of Work)
To synchronize the network without a central authority, we use a simplified Proof of Work algorithm.
*   **Mechanism:** miners must find a number called a `nonce` such that the hash of the block starts with a specific number of zeros (difficulty).
*   **Purpose:** This proves computational resources were expended, preventing spam and attacks.
