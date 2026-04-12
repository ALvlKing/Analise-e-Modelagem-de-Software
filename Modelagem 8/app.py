import streamlit as st
import pandas as pd
from datetime import datetime

# --- MODELO DE DADOS (Baseado no Diagrama de Classe) ---
class CD:
    def __init__(self, cod, artista, titulo, ano, preco):
        self.cod = cod
        self.artista = artista
        self.titulo = titulo
        self.ano = ano
        self.preco = preco

# --- FUNÇÕES DE APOIO ---
def validar_ano(ano):
    # RNF002 - Validação de 4 dígitos e proibição de datas futuras
    ano_atual = datetime.now().year
    return 1000 <= ano <= ano_atual

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="Acervo de CDs", layout="wide", page_icon="💿")

if 'acervo' not in st.session_state:
    st.session_state.acervo = []

st.title("💿 Gerenciador de Acervo: Coleção de CDs")

# --- NAVEGAÇÃO LATERAL ---
menu = st.sidebar.radio("Navegação", ["Cadastrar CD", "Ver Acervo / Pesquisar", "Gerenciar Itens"])

# --- RF001 - CADASTRAR CD ---
if menu == "Cadastrar CD":
    st.header("➕ Adicionar Novo CD")
    with st.form("form_cadastro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            artista = st.text_input("Artista/Banda")
            titulo = st.text_input("Título do Álbum")
        with col2:
            ano = st.number_input("Ano de Lançamento", min_value=0, max_value=2100, step=1, value=2024)
            preco = st.number_input("Preço de Aquisição (R$)", min_value=0.0, step=0.01)
        
        if st.form_submit_button("Salvar no Acervo"):
            if not artista or not titulo:
                st.error("Preencha o Artista e o Título.")
            elif not validar_ano(ano):
                st.error(f"Ano inválido! Insira um ano entre 1000 e {datetime.now().year}.")
            else:
                novo_cod = len(st.session_state.acervo) + 1
                novo_cd = CD(novo_cod, artista, titulo, ano, preco)
                st.session_state.acervo.append(novo_cd)
                st.success(f"'{titulo}' de {artista} adicionado com sucesso!")

# --- RF002 e RF003 - PESQUISAR E LISTAR ---
elif menu == "Ver Acervo / Pesquisar":
    st.header("🔎 Consulta ao Acervo")
    
    # RF002 - Pesquisar por Artista (Filtro rápido para coleções grandes - RNF001)
    busca = st.text_input("Filtrar por nome do Artista", placeholder="Digite para buscar...")
    
    if st.session_state.acervo:
        # Conversão para DataFrame para visualização rápida
        dados = [vars(cd) for cd in st.session_state.acervo]
        df = pd.DataFrame(dados)
        df.columns = ["Código", "Artista", "Título", "Ano", "Preço (R$)"]
        
        if busca:
            df = df[df['Artista'].str.contains(busca, case=False
