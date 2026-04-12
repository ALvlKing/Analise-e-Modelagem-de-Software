import streamlit as st
import pandas as pd

# --- MODELO DE DADOS (Baseado no Diagrama de Classe) ---
class Produto:
    def __init__(self, id_prod, descricao, qtd_prevista, qtd_efetiva, preco_estimado):
        self.id_prod = id_prod
        self.descricao = descricao
        self.qtd_prevista = qtd_prevista
        self.qtd_efetiva = qtd_efetiva
        self.preco_estimado = preco_estimado

    @property
    def total_estimado(self):
        # RF005 - Calcular Total Estimado
        return self.qtd_efetiva * self.preco_estimado

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="Planejamento Mensal de Compras", layout="wide")

# Inicialização do Estado (RNF003 - Manutenibilidade)
if 'estoque' not in st.session_state:
    st.session_state.estoque = []

st.title("🛒 Planejamento de Compras Mensal")

# --- RF001, RF002, RF004 (Cadastro e Definição) ---
with st.expander("➕ Cadastrar Novo Produto", expanded=True):
    with st.form("cadastro_produto"):
        col1, col2, col3 = st.columns([2, 1, 1])
        
        desc = col1.text_input("Descrição do Produto", placeholder="Ex: Arroz 5kg")
        # RNF004 - Integridade (Apenas valores positivos)
        prevista = col2.number_input("Previsão Mensal (Qtd)", min_value=0, step=1)
        preco = col3.number_input("Preço Estimado (R$)", min_value=0.0, step=0.5)
        
        if st.form_submit_button("Adicionar à Planilha"):
            if desc:
                novo_id = len(st.session_state.estoque) + 1
                novo_p = Produto(novo_id, desc, prevista, 0, preco)
                st.session_state.estoque.append(novo_p)
                st.success(f"{desc} adicionado!")
            else:
                st.error("A descrição é obrigatória.")

# --- EXIBIÇÃO E AJUSTES (RF003 e RNF001) ---
if st.session_state.estoque:
    st.divider()
    st.subheader("📋 Planilha de Itens")

    # Transformação para DataFrame para facilitar a visualização
    dados = []
    for p in st.session_state.estoque:
        dados.append({
            "ID": p.id_prod,
            "Descrição": p.descricao,
            "Qtd Prevista": p.qtd_prevista,
            "Qtd Efetiva": p.qtd_efetiva,
            "Preço Est. (R$)": p.preco_estimado,
            "Total (R$)": p.total_estimado
        })
    
    df = pd.DataFrame(dados)

    # RNF001 - Usabilidade (Alertas visuais para excesso de quantidade)
    def destacar_excesso(row):
        # Alerta se a Qtd Efetiva for > 20% superior à Prevista
        cor = 'background-color: #ff4b4b; color: white' if row['Qtd Efetiva'] > (row['Qtd Prevista'] * 1.2) else ''
        return [cor] * len(row)

    # Exibição com Edição em Tempo Real (RF003 e RNF002)
    edited_df = st.data_editor(
        df.style.apply(destacar_excesso, axis=1),
        column_config={
            "Qtd Efetiva": st.column_config.NumberColumn("Qtd Efetiva", min_value=0, step=1),
            "Preço Est. (R$)": st.column_config.NumberColumn("Preço Est. (R$)", min_value=0.0),
            "Total (R$)": st.column_config.NumberColumn("Total (R$)", disabled=True)
        },
        disabled=["ID", "Descrição", "Qtd Prevista", "Total (R$)"],
        use_container_width=True,
        hide_index=True
    )

    # Sincronização da edição de volta para os objetos (RNF002)
    if st.button("Salvar Alterações e Atualizar Totais"):
        for i, row in edited_df.iterrows():
            st.session_state.estoque[i].qtd_efetiva = row['Qtd Efetiva']
            st.session_state.estoque[i].preco_estimado = row['Preço Est. (R$)']
        st.rerun()

    # RF005 - Total Geral
    total_geral = edited_df["Total (R$)"].sum()
    st.metric("Total Estimado da Compra", f"R$ {total_geral:,.2f}")

else:
    st.info("Sua planilha está vazia. Comece cadastrando um produto acima!")
