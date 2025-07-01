from blockchain import Blockchain, Transaction
from btree import BTree
from typing import List, Dict, Any, Optional
import time


class BlockchainIndexer:
    """Integra o blockchain com indexação B-tree."""
    
    def __init__(self):
        self.blockchain = Blockchain()
        
        # Índices B-tree para diferentes tipos de consulta
        self.transaction_id_index = BTree(max_keys=10)  # Índice por ID de transação
        self.timestamp_index = BTree(max_keys=10)       # Índice por timestamp
        self.sender_index = BTree(max_keys=10)          # Índice por remetente
        self.receiver_index = BTree(max_keys=10)        # Índice por destinatário
        
        # Indexar o bloco gênese
        self._index_block(self.blockchain.chain[0])
    
    def add_transaction(self, sender: str, receiver: str, amount: float) -> str:
        """Adiciona uma nova transação ao blockchain."""
        transaction = Transaction(sender, receiver, amount)
        self.blockchain.add_transaction(transaction)
        return transaction.transaction_id
    
    def mine_block(self, miner_address: str, miner_name: str = "") -> Dict[str, Any]:
        """Minera um novo bloco e atualiza os índices. miner_name é opcional."""
        # Minerar o bloco
        block = self.blockchain.mine_pending_transactions(miner_address)
        
        # Indexar o novo bloco
        self._index_block(block)
        
        result = {
            'block_index': block.index,
            'block_hash': block.hash,
            'transactions_count': len(block.transactions),
            'timestamp': block.timestamp
        }
        if miner_name:
            result['miner_name'] = miner_name
        return result
    
    def _index_block(self, block):
        """Indexa todas as transações de um bloco."""
        for transaction in block.transactions:
            # Indexar por ID de transação
            self.transaction_id_index.insert(
                transaction.transaction_id, 
                {
                    'block_index': block.index,
                    'transaction': transaction.to_dict()
                }
            )
            
            # Indexar por timestamp
            self.timestamp_index.insert(
                transaction.timestamp,
                {
                    'block_index': block.index,
                    'transaction': transaction.to_dict()
                }
            )
            
            # Indexar por remetente (se não for None)
            if transaction.sender:
                self.sender_index.insert(
                    transaction.sender,
                    {
                        'block_index': block.index,
                        'transaction': transaction.to_dict()
                    }
                )
            
            # Indexar por destinatário
            if transaction.receiver:
                self.receiver_index.insert(
                    transaction.receiver,
                    {
                        'block_index': block.index,
                        'transaction': transaction.to_dict()
                    }
                )
    
    def get_transaction_by_id(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """Busca uma transação por ID usando o índice B-tree."""
        result = self.transaction_id_index.search(transaction_id)
        return result
    
    def get_transactions_by_sender(self, sender: str) -> List[Dict[str, Any]]:
        """Busca todas as transações de um remetente específico."""
        result = self.sender_index.search(sender)
        if result is None:
            return []
        
        # Se há múltiplas transações do mesmo remetente
        if isinstance(result, list):
            return result
        else:
            return [result]
    
    def get_transactions_by_receiver(self, receiver: str) -> List[Dict[str, Any]]:
        """Busca todas as transações para um destinatário específico."""
        result = self.receiver_index.search(receiver)
        if result is None:
            return []
        
        # Se há múltiplas transações para o mesmo destinatário
        if isinstance(result, list):
            return result
        else:
            return [result]
    
    def get_transactions_by_time_range(self, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        """Busca transações em um intervalo de tempo usando o índice B-tree."""
        results = self.timestamp_index.range_search(start_time, end_time)
        return [result[1] for result in results]  # result[1] contém o valor
    
    def get_blockchain_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do blockchain."""
        all_transactions = self.blockchain.get_all_transactions()
        
        return {
            'total_blocks': len(self.blockchain.chain),
            'total_transactions': len(all_transactions),
            'pending_transactions': len(self.blockchain.pending_transactions),
            'is_valid': self.blockchain.is_chain_valid(),
            'difficulty': self.blockchain.difficulty,
            'mining_reward': self.blockchain.mining_reward
        }
    
    def get_balance(self, address: str) -> float:
        """Retorna o saldo de um endereço."""
        return self.blockchain.get_balance(address)
    
    def get_full_blockchain(self) -> Dict[str, Any]:
        """Retorna o blockchain completo."""
        return self.blockchain.to_dict()
    
    def populate_demo_data(self) -> Dict[str, Any]:
        """Popula o blockchain com dados de demonstração de forma intuitiva e compatível com validação de saldo."""
        transaction_ids = []
        blocks_mined = []
        self.mine_block('Luiza')
        blocks_mined.append('Luiza')
        txs1 = [
            ('Luiza', 'Matheus', 10.0),
            ('Matheus', 'João', 5.0),
            ('João', 'Rafael', 2.0),
            ('Luiza', 'Rafael', 1.0),
            ('Matheus', 'Luiza', 2.0),
        ]
        for sender, receiver, amount in txs1:
            try:
                tx_id = self.add_transaction(sender, receiver, amount)
                transaction_ids.append(tx_id)
            except Exception:
                pass
        blocks_mined.append(self.mine_block('Matheus'))
        txs2 = [
            ('Rafael', 'Luiza', 1.0),
            ('Luiza', 'João', 3.0),
            ('João', 'Matheus', 2.0),
            ('Matheus', 'Rafael', 1.0),
            ('Rafael', 'Matheus', 2.0),
        ]
        for sender, receiver, amount in txs2:
            try:
                tx_id = self.add_transaction(sender, receiver, amount)
                transaction_ids.append(tx_id)
            except Exception:
                pass
        blocks_mined.append(self.mine_block('João'))
        txs3 = [
            ('João', 'Matheus', 2.0),
            ('Matheus', 'Rafael', 1.0),
            ('Rafael', 'Luiza', 2.0),
            ('Luiza', 'Matheus', 1.0),
        ]
        for sender, receiver, amount in txs3:
            try:
                tx_id = self.add_transaction(sender, receiver, amount)
                transaction_ids.append(tx_id)
            except Exception:
                pass
        blocks_mined.append(self.mine_block('Rafael'))
        txs4 = [
            ('Luiza', 'João', 2.0),
            ('João', 'Rafael', 1.0),
            ('Rafael', 'Matheus', 2.0),
        ]
        for sender, receiver, amount in txs4:
            try:
                tx_id = self.add_transaction(sender, receiver, amount)
                transaction_ids.append(tx_id)
            except Exception:
                pass
        blocks_mined.append(self.mine_block('Luiza'))

        return {
            'message': 'Dados de demonstração criados com sucesso',
            'transaction_ids': transaction_ids,
            'blocks_mined': blocks_mined,
            'stats': self.get_blockchain_stats()
        }

