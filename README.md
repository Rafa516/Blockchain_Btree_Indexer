![Logo da UnB](https://repositorio-imagens.netlify.app/logounb.png)
### Mestrado PPGI - Programa de Pós-Graduação em Informática 
#### Projeto e Complexidade de Algoritmos - 1ª 2025 
##### Estrutura de Dados baseadas em árvores
###### Discentes
*   João Lucas Pinto
*   Luiza de Araújo Nunes Gomes
*   Matheus Bezerra
*   Rafael da Silva Oliveira

---
# Projeto Blockchain B-tree Indexer (Streamlit)
🔗 **URL do Projeto:** ([https://blockchain-btree-indexer.streamlit.app/](https://blockchain-btree-indexer.streamlit.app/))

📄 **Documentação:** ([Documentação do Projeto - Blockchain B-tree Indexer](https://github.com/Rafa516/Blockchain_Btree_Indexer/blob/main/Documentos/Documenta%C3%A7%C3%A3o%20do%20Projeto%20-%20Blockchain%20B-tree%20Indexer.md))
## 1. Introdução

Este projeto tem como objetivo demonstrar a aplicação de B-trees para indexação eficiente de dados em um ambiente de simulação de blockchain, utilizando o Streamlit para a interface de usuário. A ideia é criar um blockchain simplificado e, em seguida, desenvolver um módulo de indexação baseado em B-tree para permitir consultas rápidas e complexas sobre os dados armazenados nos blocos. Isso ilustrará como as B-trees podem otimizar o acesso a dados em sistemas que, por natureza, são sequenciais e otimizados para anexação.

## 2. Arquitetura do Projeto

O projeto será dividido nos seguintes componentes principais:

### 2.1. Blockchain Simplificado

Este módulo será responsável por simular a funcionalidade básica de um blockchain. Ele incluirá:

*   **Classe `Block`**: Representará um bloco individual, contendo um índice, um timestamp, uma lista de transações, um hash do bloco anterior e seu próprio hash.
*   **Classe `Blockchain`**: Gerenciará a cadeia de blocos, incluindo a criação do bloco gênese, a adição de novos blocos e a validação da cadeia.
*   **Transações**: Objetos simples que representam dados a serem armazenados nos blocos (e.g., `sender`, `receiver`, `amount`, `transaction_id`).

### 2.2. Módulo de Indexação B-tree

Este será o coração do projeto, implementando uma B-tree para indexar as transações do blockchain. A B-tree será otimizada para buscas por chave e por intervalo.

*   **Classe `BTreeNode`**: Representará um nó da B-tree, contendo chaves, dados associados e ponteiros para nós filhos.
*   **Classe `BTree`**: Implementará a lógica da B-tree, incluindo operações de inserção, busca por chave e busca por intervalo.
*   **Estratégia de Indexação**: As transações serão indexadas com base em um ou mais atributos (e.g., `transaction_id` para buscas exatas, `timestamp` para buscas de intervalo).

### 2.3. Aplicação Streamlit

Uma aplicação Streamlit será desenvolvida para interagir com uma simulação de blockchain e o índice B-tree. Ela permitirá que os usuários:

*   Adicionem novas transações ao blockchain.
*   Consultem transações por `transaction_id`.
*   Consultem transações dentro de um intervalo de `timestamp`.
*   Visualizem a cadeia de blocos completa.
*   Visualizem estatísticas do blockchain.

### 2.4. Estrutura de Diretórios

A estrutura de diretórios do projeto será organizada da seguinte forma:

```
Blockchain_Btree_Indexer/
├── Documentos/           # Documentos
│   └── Documentação do Projeto - Blockchain B-tree Indexer.md   # Documentação do projeto
├── app.py                # Aplicação Streamlit
├── blockchain.py         # Implementação do Blockchain Simplificado
├── btree.py              # Implementação da B-tree
├── blockchain_indexer.py # Módulo que integra blockchain e B-tree
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação do projeto
```

## 3. Requisitos do Sistema

O projeto requer **Python 3.11 ou superior** e as seguintes bibliotecas Python, que podem ser instaladas via pip:

*   `streamlit`: Para a interface web interativa.
*   `pandas`: Utilizado para manipulação de dados e para o gráfico de barras no dashboard do Streamlit.

Todas as outras funcionalidades do projeto utilizam bibliotecas padrão do Python, minimizando dependências externas.

## 4. Processo de Instalação

Para instalar e executar o projeto, siga os passos abaixo:

1.  **Clone ou Baixe o Projeto:**
    Primeiro, obtenha os arquivos do projeto. Se você tem Git instalado, pode clonar o repositório:
    ```bash
    git clone <URL_DO_REPOSITORIO> # Substitua pela URL real do repositório, se aplicável
    cd Blockchain_Btree_Indexer
    ```
    Caso contrário, baixe o arquivo compactado (`Blockchain_Btree_Indexer.tar.gz`) fornecido anteriormente e extraia-o para um diretório de sua escolha.

2.  **Instale as Dependências:**
    Navegue até o diretório raiz do projeto (onde se encontram `app.py`, `blockchain.py`, etc.) no seu terminal. Em seguida, instale as dependências listadas no `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
    Se você não tiver o `requirements.txt` (por exemplo, se baixou os arquivos individualmente), pode instalar as dependências manualmente:
    ```bash
    pip install streamlit pandas
    ```

## 5. Execução da Aplicação

Após a instalação das dependências, você pode iniciar a aplicação Streamlit:

1.  **Navegue até o Diretório do Projeto:**
    Certifique-se de que seu terminal esteja no diretório onde o arquivo `app.py` está localizado.

2.  **Execute o Streamlit:**
    Execute o seguinte comando:
    ```bash
    streamlit run app.py
    ```
    O Streamlit iniciará automaticamente um servidor local e abrirá a aplicação no seu navegador padrão. Por padrão, a aplicação estará disponível em `http://localhost:8501`. Se esta porta já estiver em uso, o Streamlit automaticamente selecionará a próxima porta disponível e informará a URL correta no terminal.

## 6. Uso da Interface

A interface da aplicação é organizada em seções acessíveis através de um menu lateral. Siga estas sugestões para explorar as funcionalidades:

1.  **Dashboard:** Ao iniciar, você verá o Dashboard com estatísticas iniciais do blockchain, que incluirá apenas o bloco gênese (o primeiro bloco da cadeia).

2.  **Criar Dados de Demonstração:** Para experimentar as funcionalidades de indexação e consulta, é altamente recomendável utilizar a seção "🎯 Dados de Demonstração". Clique no botão "🎯 Criar Dados de Demonstração" para popular o blockchain com um conjunto de transações e blocos de exemplo. Isso criará um conjunto de dados realista para testar as funcionalidades de consulta e observar o impacto das B-trees.

3.  **Adicionar Transação:** Na seção "💸 Adicionar Transação", você pode criar novas transações manualmente, especificando remetente, destinatário e valor. Essas transações serão adicionadas à lista de transações pendentes.

4.  **Minerar Bloco:** Após adicionar transações, vá para a seção "⛏️ Minerar Bloco". Informe um endereço de minerador e clique em "⛏️ Minerar Bloco". As transações pendentes serão processadas em um novo bloco, que será adicionado à cadeia e, crucialmente, suas transações serão indexadas pelas B-trees.

5.  **Consultas Indexadas:** Explore as diferentes seções de consulta (🔍 Consultar por ID, 👤 Consultar por Remetente, 📨 Consultar por Destinatário, ⏰ Consultar por Período). Insira os critérios de busca e observe a rapidez com que os resultados são retornados, demonstrando a eficiência dos índices B-tree.

6.  **Consultar Saldo:** Na seção "💰 Consultar Saldo", você pode verificar o saldo de qualquer endereço, e o histórico de transações enviadas e recebidas por ele.

7.  **Visualizar Blockchain:** A seção "🔗 Visualizar Blockchain" permite inspecionar a cadeia de blocos completa, bloco por bloco, e ver as transações contidas em cada um.
