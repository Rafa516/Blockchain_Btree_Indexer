from typing import List, Tuple, Any, Optional
import bisect


class BTreeNode:
    """Representa um nó da B-tree."""
    
    def __init__(self, leaf: bool = False):
        self.leaf = leaf
        self.keys: List[Any] = []  # Chaves armazenadas no nó
        self.values: List[Any] = []  # Valores associados às chaves
        self.children: List['BTreeNode'] = []  # Ponteiros para nós filhos
    
    def is_full(self, max_keys: int) -> bool:
        """Verifica se o nó está cheio."""
        return len(self.keys) >= max_keys
    
    def insert_key_value(self, key: Any, value: Any):
        """Insere uma chave-valor no nó mantendo a ordem."""
        index = bisect.bisect_left(self.keys, key)
        if index < len(self.keys) and self.keys[index] == key:
            # Chave já existe, atualiza o valor (ou adiciona à lista se for múltiplo)
            if isinstance(self.values[index], list):
                self.values[index].append(value)
            else:
                self.values[index] = [self.values[index], value]
        else:
            # Nova chave
            self.keys.insert(index, key)
            self.values.insert(index, value)
    
    def split(self, max_keys: int) -> Tuple['BTreeNode', Any, Any]:
        """Divide o nó em dois e retorna o nó direito e a chave/valor do meio."""
        mid_index = max_keys // 2
        
        # Criar novo nó (direito)
        new_node = BTreeNode(leaf=self.leaf)
        
        # Mover metade das chaves/valores para o novo nó
        new_node.keys = self.keys[mid_index + 1:]
        new_node.values = self.values[mid_index + 1:]
        
        # Se não for folha, mover também os filhos
        if not self.leaf:
            new_node.children = self.children[mid_index + 1:]
            self.children = self.children[:mid_index + 1]
        
        # Guardar chave/valor do meio
        mid_key = self.keys[mid_index]
        mid_value = self.values[mid_index]
        
        # Manter apenas a primeira metade no nó atual
        self.keys = self.keys[:mid_index]
        self.values = self.values[:mid_index]
        
        return new_node, mid_key, mid_value


class BTree:
    """Implementa uma B-tree para indexação eficiente."""
    
    def __init__(self, max_keys: int = 5):
        self.root = BTreeNode(leaf=True)
        self.max_keys = max_keys
        self.min_keys = max_keys // 2
    
    def insert(self, key: Any, value: Any):
        """Insere uma chave-valor na B-tree."""
        root = self.root
        
        # Se a raiz está cheia, precisa dividir
        if root.is_full(self.max_keys):
            new_root = BTreeNode(leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        
        self._insert_non_full(self.root, key, value)
    
    def _insert_non_full(self, node: BTreeNode, key: Any, value: Any):
        """Insere em um nó que não está cheio."""
        if node.leaf:
            # Nó folha: inserir diretamente
            node.insert_key_value(key, value)
        else:
            # Nó interno: encontrar filho apropriado
            child_index = 0
            while (child_index < len(node.keys) and key > node.keys[child_index]):
                child_index += 1
            
            child = node.children[child_index]
            
            # Se o filho está cheio, dividir primeiro
            if child.is_full(self.max_keys):
                self._split_child(node, child_index)
                # Após a divisão, determinar qual dos dois filhos usar
                if key > node.keys[child_index]:
                    child_index += 1
                child = node.children[child_index]
            
            self._insert_non_full(child, key, value)
    
    def _split_child(self, parent: BTreeNode, child_index: int):
        """Divide um filho cheio."""
        child = parent.children[child_index]
        new_child, mid_key, mid_value = child.split(self.max_keys)
        
        # Inserir a chave do meio no pai
        parent.keys.insert(child_index, mid_key)
        parent.values.insert(child_index, mid_value)
        parent.children.insert(child_index + 1, new_child)
    
    def search(self, key: Any) -> Optional[Any]:
        """Busca uma chave na B-tree."""
        return self._search_node(self.root, key)
    
    def _search_node(self, node: BTreeNode, key: Any) -> Optional[Any]:
        """Busca uma chave em um nó específico."""
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        # Chave encontrada
        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]
        
        # Se é folha e não encontrou, a chave não existe
        if node.leaf:
            return None
        
        # Buscar no filho apropriado
        return self._search_node(node.children[i], key)
    
    def range_search(self, min_key: Any, max_key: Any) -> List[Tuple[Any, Any]]:
        """Busca todas as chaves-valores em um intervalo."""
        results = []
        self._range_search_node(self.root, min_key, max_key, results)
        return results
    
    def _range_search_node(self, node: BTreeNode, min_key: Any, max_key: Any, results: List[Tuple[Any, Any]]):
        """Busca em intervalo em um nó específico."""
        i = 0
        
        # Percorrer as chaves do nó
        while i < len(node.keys):
            # Se não é folha, buscar no filho à esquerda
            if not node.leaf:
                self._range_search_node(node.children[i], min_key, max_key, results)
            
            # Se a chave está no intervalo, adicionar aos resultados
            if min_key <= node.keys[i] <= max_key:
                results.append((node.keys[i], node.values[i]))
            
            # Se a chave é maior que max_key, parar
            if node.keys[i] > max_key:
                return
            
            i += 1
        
        # Se não é folha, buscar no último filho
        if not node.leaf:
            self._range_search_node(node.children[i], min_key, max_key, results)
    
    def get_all_items(self) -> List[Tuple[Any, Any]]:
        """Retorna todas as chaves-valores da B-tree em ordem."""
        results = []
        self._inorder_traversal(self.root, results)
        return results
    
    def _inorder_traversal(self, node: BTreeNode, results: List[Tuple[Any, Any]]):
        """Percorre a árvore em ordem."""
        i = 0
        while i < len(node.keys):
            # Se não é folha, visitar filho à esquerda
            if not node.leaf:
                self._inorder_traversal(node.children[i], results)
            
            # Visitar a chave atual
            results.append((node.keys[i], node.values[i]))
            i += 1
        
        # Se não é folha, visitar o último filho
        if not node.leaf:
            self._inorder_traversal(node.children[i], results)
    
    def print_tree(self):
        """Imprime a estrutura da árvore (para debug)."""
        self._print_node(self.root, 0)
    
    def _print_node(self, node: BTreeNode, lAntôniol: int):
        """Imprime um nó específico."""
        indent = "  " * lAntôniol
        print(f"{indent}Nível {lAntôniol}: {node.keys}")
        
        if not node.leaf:
            for child in node.children:
                self._print_node(child, lAntôniol + 1)

