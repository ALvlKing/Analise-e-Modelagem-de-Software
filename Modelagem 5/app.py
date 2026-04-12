import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime

# --- LÓGICA DE NEGÓCIO (Baseada no Diagrama de Classes) ---

class TipoGasto:
    def __init__(self, id_tipo, descricao):
        self.id_tipo = id_tipo
        self.descricao = descricao

class Gasto:
    def __init__(self, id_gasto, descricao, valor, obs, forma, tipo, data=None):
        self.id_gasto = id_gasto
        self.descricao = descricao
        self.valor = valor
        self.obs = obs
        self.forma = forma
        self.tipo = tipo
        self.data = data if data else datetime.now()

# RF003 - Listar Forma Pag (Baseado no ENUM FORMA do diagrama)
FORMAS_PAGAMENTO = ["DINHEIRO", "CARTAO CRED", "CARTAO DEBITO", "TICK ALI"]

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="Gerenciador de Gastos", layout="wide")

# Inicialização do Banco de Dados em Memória (Session State)
if 'tipos' not in st.session_state:
    st.session_state.tipos = [TipoGasto(1, "Alimentação"), TipoGasto(2, "Transporte")]
if 'gastos' not in st.session_state:
    st.session_state.gastos = []
if 'usuarios' not in st.session_state:
    # RNF001 - Simulação de senha criptografada
    senha_hash = hashlib.sha256("admin123".encode()).hexdigest()
    st.session_state.usuarios = {"admin": senha_hash}

# --- NAVEGAÇÃO ---
st.title("💰 Sistema de Controle de Gastos")
menu = ["Lançar Gasto", "Gerenciar Tipos", "Relatórios Mensais"]
escolha = st.sidebar.selectbox("Navegação", menu)

# --- RF001 - GERENCIAR TIPO GASTO ---
if escolha == "Gerenciar Tipos":
    st.header("📋 Gerenciar Tipos de Gasto")
    
    with st.form("form_tipo"):
        nova_desc = st.text_input("Descrição do Novo Tipo")
        if st.form_submit_button("Cadastrar Tipo"):
            novo_id = len(st.session_state.tipos) + 1
            st.session_state.tipos.append(TipoGasto(novo_id, nova_desc))
            st.success(f"Tipo '{nova_desc}' cadastrado!")

    st.subheader("Tipos Existentes")
    df_tipos = pd.DataFrame([{"ID": t.id_tipo, "Descrição": t.descricao} for t in st.session_state.tipos])
    st.table(df_tipos)

# --- RF002 - GERENCIAR GASTO ---
elif escolha == "Lançar Gasto":
    st.header("💸 Novo Lançamento de Gasto")
    
    with st.form("form_gasto"):
        col1, col2 = st.columns(2)
        with col1:
            desc = st.text_input("Descrição do Gasto")
            valor = st.number_input("Valor (R$)", min_value=0.01, step=0.1)
            # RF003 - Listar Forma Pag
            forma = st.selectbox("Forma de Pagamento", FORMAS_PAGAMENTO)
        with col2:
            tipo = st.selectbox("Categoria (Tipo)", st.session_state.tipos, format_func=lambda x: x.descricao)
            data_gasto = st.date_input("Data do Gasto", datetime.now())
            obs = st.text_area("Observações")
            
        if st.form_submit_button("Salvar Gasto"):
            # RNF002 - Processamento eficiente garantindo resposta rápida
            novo_gasto = Gasto(
                id_gasto=len(st.session_state.gastos) + 1,
                descricao=desc,
                valor=valor,
                obs=obs,
                forma=forma,
                tipo=tipo.descricao,
                data=data_gasto
            )
            st.session_state.gastos.append(novo_gasto)
            st.balloons()
            st.success("Gasto registrado com sucesso!")

# --- RF005 - GERAR RELATÓRIO GASTOS MENSAIS ---
elif escolha == "Relatórios Mensais":
    st.header("📊 Relatório de Gastos Mensais")
    
    if not st.session_state.gastos:
        st.warning("Nenhum gasto registrado para gerar relatório.")
    else:
        # Transformação dos dados para análise
        dados = []
        for g in st.session_state.gastos:
            dados.append({
                "Data": g.data,
                "Descrição": g.descricao,
                "Valor": g.valor,
                "Categoria": g.tipo,
                "Forma": g.forma
            })
        
        df = pd.DataFrame(dados)
        df['Mês'] = pd.to_datetime(df['Data']).dt.strftime('%m/%Y')
        
        mes_filtro = st.selectbox("Selecione o Mês", df['Mês'].unique())
        df_filtrado = df[df['Mês'] == mes_filtro]
        
        # Exibição de Métricas
        c1, c2 = st.columns(2)
        c1.metric("Total no Mês", f"R$ {df_filtrado['Valor'].sum():.2f}")
        c2.metric("Nº de Lançamentos", len(df_filtrado))
        
        st.subheader(f"Detalhamento - {mes_filtro}")
        st.dataframe(df_filtrado, use_container_width=True)
        
        # Gráfico por Categoria
        st.subheader("Gastos por Categoria")
        chart_data = df_filtrado.groupby("Categoria")["Valor"].sum()
        st.bar_chart(chart_data)
