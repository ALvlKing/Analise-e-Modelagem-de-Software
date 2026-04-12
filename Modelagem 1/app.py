import streamlit as st
import pandas as pd
from datetime import datetime

# --- CLASSE DO MODELO (Baseada no Diagrama UML) ---
class ContaLuz:
    def __init__(self, dt_leitura, n_leitura, kw_gasto, valor_pg, dt_pag):
        self._dt_leitura = dt_leitura  # [cite: 2, 4]
        self._n_leitura = n_leitura    # [cite: 2]
        self._kw_gasto = kw_gasto      # [cite: 2]
        self._valor_pg = valor_pg      # [cite: 2]
        self._dt_pag = dt_pag          # [cite: 2]
        self._media = 0.0              # [cite: 2]

    def to_dict(self):
        return {
            "Data Leitura": self._dt_leitura,
            "Nº Leitura": self._n_leitura,
            "KW Gasto": self._kw_gasto,
            "Valor Pago (R$)": self._valor_pg,
            "Data Pagamento": self._dt_pag
        }

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão de Conta de Luz", layout="wide")
st.title("⚡ Gerenciador de Consumo de Energia")

# Inicialização do Histórico (RF005)
if 'historico' not in st.session_state:
    st.session_state.historico = []

# --- FORMULÁRIO DE CADASTRO (RF001) ---
st.header("Cadastrar Nova Conta")
with st.form("form_conta"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dt_leitura = st.date_input("Data da Leitura")
        n_leitura = st.number_input("Número da Leitura", min_value=0, step=1)
    
    with col2:
        kw_gasto = st.number_input("KW Gasto", min_value=0, step=1)
        valor_pg = st.number_input("Valor a Pagar (R$)", min_value=0.0, format="%.2f")
        
    with col3:
        dt_pag = st.date_input("Data do Pagamento")
    
    submit = st.form_submit_button("Salvar Conta")

    if submit:
        # Validação de Confiabilidade (RNF003)
        if dt_pag < dt_leitura:
            st.error("Erro: A Data de Pagamento não pode ser anterior à Data de Leitura! [RNF003]") [cite: 8]
        else:
            nova_conta = ContaLuz(dt_leitura, n_leitura, kw_gasto, valor_pg, dt_pag)
            st.session_state.historico.append(nova_conta.to_dict())
            st.success("Conta cadastrada com sucesso!")

# --- GERENCIAMENTO E VISUALIZAÇÃO (RF002, RF003, RF005) ---
if st.session_state.historico:
    df = pd.DataFrame(st.session_state.historico)
    
    # Cálculos de Média e Extremos (gas.maior / gas.menor) [cite: 3]
    media_consumo = df["KW Gasto"].mean()
    maior_consumo = df["KW Gasto"].max()
    menor_consumo = df["KW Gasto"].min()

    # Exibição de Métricas (RF003)
    st.divider()
    st.header("Análise de Consumo")
    m1, m2, m3 = st.columns(3)
    m1.metric("Média de Consumo", f"{media_consumo:.2f} KW")
    m2.metric("Maior Gasto", f"{maior_consumo} KW")
    m3.metric("Menor Gasto", f"{menor_consumo} KW")

    # Formatação Condicional (RNF002) 
    def destacar_extremos(s):
        is_max = s == maior_consumo
        is_min = s == menor_consumo
        styles = []
        for v_max, v_min in zip(is_max, is_min):
            if v_max:
                styles.append('background-color: #ff4b4b; color: white') # Vermelho para maior
            elif v_min:
                styles.append('background-color: #2e7d32; color: white') # Verde para menor
            else:
                styles.append('')
        return styles

    # Listagem de Histórico (RF005) com bloqueio de edição (RNF001) 
    st.subheader("Histórico de Contas")
    st.dataframe(
        df.style.apply(destarcar_extremos, subset=["KW Gasto"]),
        use_container_width=True
    )
    
    st.info("💡 Legenda: Vermelho = Maior Consumo | Verde = Menor Consumo")
else:
    st.info("Nenhuma conta cadastrada ainda.")
