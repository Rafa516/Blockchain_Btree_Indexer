import hashlib
import json
import time
from typing import List, Dict, Any, Optional


class Transaction:
    """Representa uma transação no blockchain."""
    
    def __init__(self, sender: str, receiver: str, amount: float, transaction_id: str = None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()
        self.transaction_id = transaction_id or self._generate_transaction_id()
    
    def _generate_transaction_id(self) -> str:
        """Gera um ID único para a transação."""
        data = f"{self.sender}{self.receiver}{self.amount}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a transação para um dicionário."""
        return {
            'transaction_id': self.transaction_id,
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
    
    def __str__(self):
        return f"Transaction({self.transaction_id}: {self.sender} -> {self.receiver}, {self.amount})"


class Block:
    """Representa um bloco no blockchain."""
    
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self._calculate_hash()
    
    def _calculate_hash(self) -> str:
        """Calcula o hash do bloco."""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 4):
        """Simula a mineração do bloco (Proof of Work simples)."""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self._calculate_hash()
        print(f"Bloco minerado: {self.hash}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o bloco para um dicionário."""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }


class Blockchain:
    """Implementa um blockchain simplificado."""
    
    def __init__(self):
        self.difficulty = 2
        self.pending_transactions: List[Transaction] = []
        self.mining_reward = 100
        self.chain: List[Block] = [self._create_genesis_block()]
    
    def _create_genesis_block(self) -> Block:
        """Cria o bloco gênese."""
        genesis_transaction = Transaction("genesis", "genesis", 0, "genesis")
        genesis_block = Block(0, [genesis_transaction], "0")
        genesis_block.mine_block(self.difficulty)
        return genesis_block
    
    def get_latest_block(self) -> Block:
        """Retorna o último bloco da cadeia."""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction):
        """Adiciona uma transação à lista de transações pendentes."""
        self.pending_transactions.append(transaction)
    
    def mine_pending_transactions(self, mining_reward_address: str):
        """Minera as transações pendentes e cria um novo bloco."""
        # Adiciona a recompensa de mineração
        reward_transaction = Transaction(None, mining_reward_address, self.mining_reward)
        self.pending_transactions.append(reward_transaction)
        
        # Cria um novo bloco
        block = Block(
            len(self.chain),
            self.pending_transactions,
            self.get_latest_block().hash
        )
        block.mine_block(self.difficulty)
        
        # Adiciona o bloco à cadeia
        self.chain.append(block)
        
        # Limpa as transações pendentes
        self.pending_transactions = []
        
        return block
    
    def get_balance(self, address: str) -> float:
        """Calcula o saldo de um endereço."""
        balance = 0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.receiver == address:
                    balance += transaction.amount
        
        return balance
    
    def is_chain_valid(self) -> bool:
        """Valida a integridade da cadeia de blocos."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block.hash != current_block._calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_all_transactions(self) -> List[Transaction]:
        """Retorna todas as transações da cadeia."""
        all_transactions = []
        for block in self.chain:
            all_transactions.extend(block.transactions)
        return all_transactions
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o blockchain para um dicionário."""
        return {
            'chain': [block.to_dict() for block in self.chain],
            'difficulty': self.difficulty,
            'pending_transactions': [tx.to_dict() for tx in self.pending_transactions],
            'mining_reward': self.mining_reward
        }

