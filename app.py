import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime
from blockchain_indexer import BlockchainIndexer

# Configuração da página
st.set_page_config(
    page_title="Blockchain B-tree Indexer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Webysther_20160322_-_Logo_UnB_%28sem_texto%29.svg/1920px-Webysther_20160322_-_Logo_UnB_%28sem_texto%29.svg.png", width=100) 
st.markdown("##### Projeto e Complexidade de Algoritmos - Estrutura de Dados baseadas em árvores ") # Título adicionado
st.markdown("---")
# Inicializar o indexador na sessão
if 'indexer' not in st.session_state:
    st.session_state.indexer = BlockchainIndexer()

indexer = st.session_state.indexer

# Título principal
st.title(" Blockchain B-tree Indexer")

st.markdown("**Demonstração de indexação de blockchain usando B-trees para consultas eficientes**")

# Sidebar para navegação
st.sidebar.title(" Menu")
page = st.sidebar.selectbox(
    "Escolha uma funcionalidade:",
    [
        "Dashboard",
        "Adicionar Transação",
        "Minerar Bloco",
        "Consultar por ID",
        "Consultar por Remetente",
        "Consultar por Destinatário",
        "Consultar por Período",
        "Consultar Saldo",
        "Dados de Demonstração",
        "Visualizar Blockchain"
    ]
)

# Função para formatar timestamp
def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")

# Função para exibir transação
def display_transaction(tx_data):
    if isinstance(tx_data, dict) and 'transaction' in tx_data:
        tx = tx_data['transaction']
        st.write(f"**ID:** {tx['transaction_id']}")
        st.write(f"**Remetente:** {tx['sender']}")
        st.write(f"**Destinatário:** {tx['receiver']}")
        st.write(f"**Valor:** {tx['amount']}")
        st.write(f"**Timestamp:** {format_timestamp(tx['timestamp'])}")
        st.write(f"**Bloco:** {tx_data['block_index']}")
    else:
        st.write(tx_data)

# Dashboard
if page == "Dashboard":
    st.header(" Estatísticas do Blockchain")
    
    # Botão para atualizar estatísticas
    # if st.button("🔄 Atualizar Estatísticas"):
    #    pass
    
    # Obter estatísticas
    stats = indexer.get_blockchain_stats()
    
    # Exibir métricas em colunas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Blocos", stats['total_blocks'])
        st.metric("Dificuldade", stats['difficulty'])
    
    with col2:
        st.metric("Total de Transações", stats['total_transactions'])
        st.metric("Recompensa de Mineração", stats['mining_reward'])
    
    with col3:
        st.metric("Transações Pendentes", stats['pending_transactions'])
        st.metric("Blockchain Válido", "✅" if stats['is_valid'] else "❌")
    
    # Gráfico de transações por bloco (se houver dados)
    if stats['total_blocks'] > 1:
        st.subheader("Transações por Bloco")
        blockchain_data = indexer.get_full_blockchain()
        
        block_data = []
        for block in blockchain_data['chain']:
            block_data.append({
                'Bloco': block['index'],
                'Transações': len(block['transactions']),
                'Timestamp': format_timestamp(block['timestamp'])
            })
        
        df = pd.DataFrame(block_data)
        st.bar_chart(df.set_index('Bloco')['Transações'])

# Adicionar Transação
elif page == "Adicionar Transação":
    st.header("Adicionar Nova Transação")
    
    with st.form("add_transaction"):
        col1, col2 = st.columns(2)
        
        with col1:
            sender = st.text_input("Remetente", placeholder="Ex: Luiza")
        
        with col2:
            receiver = st.text_input("Destinatário", placeholder="Ex: Matheus")
        
        amount = st.number_input("Valor", min_value=0.01, step=0.01, format="%.2f")
        
        submitted = st.form_submit_button("➕ Adicionar Transação")
        
        if submitted:
            if sender and receiver and amount > 0:
                try:
                    tx_id = indexer.add_transaction(sender, receiver, amount)
                    st.success(f"✅ Transação adicionada com sucesso!")
                    st.info(f"**ID da Transação:** {tx_id}")
                except Exception as e:
                    st.error(f"❌ Erro ao adicionar transação: {str(e)}")
            else:
                st.error("❌ Por favor, preencha todos os campos corretamente.")

# Minerar Bloco
elif page == "Minerar Bloco":
    st.header("Minerar Novo Bloco")
    
    # Verificar se há transações pendentes
    stats = indexer.get_blockchain_stats()
    
    if stats['pending_transactions'] == 0:
        st.warning(" Não há transações pendentes para minerar.")
        st.info(" Adicione algumas transações primeiro na seção 'Adicionar Transação'.")
    else:
        st.info(f" Há {stats['pending_transactions']} transação(ões) pendente(s) para minerar.")
        
        miner_address = st.text_input("Endereço do Minerador", value="Miner1", placeholder="Ex: Miner1")
        
        if st.button("Minerar Bloco"):
            if miner_address:
                try:
                    with st.spinner("⛏️ Minerando bloco..."):
                        block_info = indexer.mine_block(miner_address)
                    
                    st.success("Bloco minerado com sucesso!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Índice do Bloco:** {block_info['block_index']}")
                        st.write(f"**Hash do Bloco:** {block_info['block_hash'][:16]}...")
                    
                    with col2:
                        st.write(f"**Transações:** {block_info['transactions_count']}")
                        st.write(f"**Timestamp:** {format_timestamp(block_info['timestamp'])}")
                    
                except Exception as e:
                    st.error(f"Erro ao minerar bloco: {str(e)}")
            else:
                st.error(" Por favor, informe o endereço do minerador.")

# Consultar por ID
elif page == "Consultar por ID":
    st.header(" Buscar Transação por ID")
    
    transaction_id = st.text_input("ID da Transação", placeholder="Ex: abc123def456")
    
    if st.button(" Buscar"):
        if transaction_id:
            try:
                result = indexer.get_transaction_by_id(transaction_id)
                
                if result:
                    st.success("✅ Transação encontrada!")
                    with st.expander(" Detalhes da Transação", expanded=True):
                        display_transaction(result)
                else:
                    st.warning(" Transação não encontrada.")
            except Exception as e:
                st.error(f" Erro na busca: {str(e)}")
        else:
            st.error(" Por favor, informe o ID da transação.")

# Consultar por Remetente
elif page == "Consultar por Remetente":
    st.header("Buscar Transações por Remetente")
    
    sender = st.text_input("Remetente", placeholder="Ex: Luiza")
    
    if st.button("🔍 Buscar"):
        if sender:
            try:
                results = indexer.get_transactions_by_sender(sender)
                
                if results:
                    st.success(f"✅ Encontradas {len(results)} transação(ões)!")
                    
                    for i, result in enumerate(results):
                        with st.expander(f" Transação {i+1}", expanded=False):
                            display_transaction(result)
                else:
                    st.warning(" Nenhuma transação encontrada para este remetente.")
            except Exception as e:
                st.error(f"❌ Erro na busca: {str(e)}")
        else:
            st.error("❌ Por favor, informe o remetente.")

# Consultar por Destinatário
elif page == "Consultar por Destinatário":
    st.header("Buscar Transações por Destinatário")
    
    receiver = st.text_input("Destinatário", placeholder="Ex: Matheus")
    
    if st.button("🔍 Buscar"):
        if receiver:
            try:
                results = indexer.get_transactions_by_receiver(receiver)
                
                if results:
                    st.success(f"✅ Encontradas {len(results)} transação(ões)!")
                    
                    for i, result in enumerate(results):
                        with st.expander(f" Transação {i+1}", expanded=False):
                            display_transaction(result)
                else:
                    st.warning(" Nenhuma transação encontrada para este destinatário.")
            except Exception as e:
                st.error(f" Erro na busca: {str(e)}")
        else:
            st.error(" Por favor, informe o destinatário.")

# Consultar por Período
elif page == "Consultar por Período":
    st.header("Buscar Transações por Período")
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Data Inicial")
        start_time = st.time_input("Hora Inicial")
    
    with col2:
        end_date = st.date_input("Data Final")
        end_time = st.time_input("Hora Final")
    
    if st.button("Buscar"):
        try:
            # Converter para timestamp
            start_datetime = datetime.combine(start_date, start_time)
            end_datetime = datetime.combine(end_date, end_time)
            
            start_timestamp = start_datetime.timestamp()
            end_timestamp = end_datetime.timestamp()
            
            if start_timestamp >= end_timestamp:
                st.error("❌ A data/hora inicial dAntônio ser anterior à final.")
            else:
                results = indexer.get_transactions_by_time_range(start_timestamp, end_timestamp)
                
                if results:
                    st.success(f"✅ Encontradas {len(results)} transação(ões) no período!")
                    
                    for i, result in enumerate(results):
                        with st.expander(f" Transação {i+1}", expanded=False):
                            display_transaction(result)
                else:
                    st.warning("⚠️ Nenhuma transação encontrada no período especificado.")
        except Exception as e:
            st.error(f"❌ Erro na busca: {str(e)}")

# Consultar Saldo
elif page == "Consultar Saldo":
    st.header("Consultar Saldo de Endereço")
    
    address = st.text_input("Endereço", placeholder="Ex: Luiza")
    
    if st.button("Consultar Saldo"):
        if address:
            try:
                balance = indexer.get_balance(address)
                
                if balance >= 0:
                    st.success(f"✅ Saldo de **{address}**: **{balance:.2f}**")
                else:
                    st.warning(f" Saldo de **{address}**: **{balance:.2f}** (negativo)")
                
                # Mostrar histórico de transações
                st.subheader(" Histórico de Transações")
                
                sent_transactions = indexer.get_transactions_by_sender(address)
                received_transactions = indexer.get_transactions_by_receiver(address)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("** Transações Enviadas:**")
                    if sent_transactions:
                        for tx in sent_transactions:
                            if isinstance(tx, dict) and 'transaction' in tx:
                                t = tx['transaction']
                                st.write(f"- {t['amount']:.2f} para {t['receiver']}")
                    else:
                        st.write("Nenhuma transação enviada.")
                
                with col2:
                    st.write("** Transações Recebidas:**")
                    if received_transactions:
                        for tx in received_transactions:
                            if isinstance(tx, dict) and 'transaction' in tx:
                                t = tx['transaction']
                                st.write(f"+ {t['amount']:.2f} de {t['sender'] or 'Sistema'}")
                    else:
                        st.write("Nenhuma transação recebida.")
                
            except Exception as e:
                st.error(f" Erro ao consultar saldo: {str(e)}")
        else:
            st.error(" Por favor, informe o endereço.")

# Dados de Demonstração
elif page == "Dados de Demonstração":
    st.header("Dados de Demonstração")
    
    st.info("Clique no botão abaixo para popular o blockchain com dados de exemplo para testes.")
    
    if st.button("Criar Dados de Demonstração"):
        try:
            with st.spinner(" Criando dados de demonstração..."):
                result = indexer.populate_demo_data()
            
            st.success("Dados de demonstração criados com sucesso!")
            
            with st.expander(" Detalhes", expanded=True):
                st.write(f"**Transações criadas:** {len(result['transaction_ids'])}")
                st.write(f"**Blocos minerados:** {len(result['blocks_mined'])}")
                
                st.subheader(" IDs das Transações:")
                for i, tx_id in enumerate(result['transaction_ids']):
                    st.write(f"{i+1}. {tx_id}")
                
                st.subheader(" Estatísticas Atualizadas:")
                stats = result['stats']
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total de Blocos", stats['total_blocks'])
                
                with col2:
                    st.metric("Total de Transações", stats['total_transactions'])
                
                with col3:
                    st.metric("Transações Pendentes", stats['pending_transactions'])
            
        except Exception as e:
            st.error(f"❌ Erro ao criar dados de demonstração: {str(e)}")

# Visualizar Blockchain
elif page == " Visualizar Blockchain":
    st.header(" Visualizar Blockchain Completo")
    
    # if st.button("🔄 Atualizar Visualização"):
    #     pass
  
    
    try:
        blockchain_data = indexer.get_full_blockchain()
        
        st.subheader("Informações Gerais")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Dificuldade:** {blockchain_data['difficulty']}")
            st.write(f"**Recompensa de Mineração:** {blockchain_data['mining_reward']}")
        
        with col2:
            st.write(f"**Total de Blocos:** {len(blockchain_data['chain'])}")
            st.write(f"**Transações Pendentes:** {len(blockchain_data['pending_transactions'])}")
        
        st.subheader(" Cadeia de Blocos")
        
        for block in blockchain_data['chain']:
            with st.expander(f" Bloco {block['index']} - {block['hash'][:16]}...", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Índice:** {block['index']}")
                    st.write(f"**Timestamp:** {format_timestamp(block['timestamp'])}")
                    st.write(f"**Hash Anterior:** {block['previous_hash'][:16]}...")
                
                with col2:
                    st.write(f"**Hash:** {block['hash'][:16]}...")
                    st.write(f"**Nonce:** {block['nonce']}")
                    st.write(f"**Transações:** {len(block['transactions'])}")
                
                if block['transactions']:
                    st.write("** Transações:**")
                    for i, tx in enumerate(block['transactions']):
                        st.write(f"{i+1}. {tx['transaction_id']}: {tx['sender']} → {tx['receiver']} ({tx['amount']})")
        
        # Transações pendentes
        if blockchain_data['pending_transactions']:
            st.subheader(" Transações Pendentes")
            for i, tx in enumerate(blockchain_data['pending_transactions']):
                st.write(f"{i+1}. {tx['transaction_id']}: {tx['sender']} → {tx['receiver']} ({tx['amount']})")
    
    except Exception as e:
        st.error(f" Erro ao visualizar blockchain: {str(e)}")

# Footer
st.markdown("---")
st.markdown("*Desenvolvido por: Rafael, João, Matheus e Luiza*")

