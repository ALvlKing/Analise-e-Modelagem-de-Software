import streamlit as st
import pandas as pd

# --- MODELO DE DADOS (Diagrama de Classe) ---

class Musico:
    def __init__(self, cod, nome, instrumento):
        self.cod = cod
        self.nome = nome
        self.instrumento = instrumento

class Musica:
    def __init__(self, cod, nome, duracao, musico):
        self.cod = cod
        self.nome = nome
        self.duracao = duracao
        self.musico = musico  # Associação com Musico

class Coletanea:
    def __init__(self, cod, titulo, ano):
        self.cod = cod
        self.titulo = titulo
        self.ano = ano
        self.faixas = []  # RF003 - Gerenciar Faixas

    def adicionar_faixa(self, musica):
        self.faixas.append(musica)

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="Gestor de Coletâneas", layout="wide", page_icon="🎼")

# Inicialização do Estado (Simulando Banco de Dados)
if 'musicos' not in st.session_state:
    st.session_state.musicos = [
        Musico(1, "Gilberto Gil", "Violão"),
        Musico(2, "Tom Jobim", "Piano")
    ]
if 'coletaneas' not in st.session_state:
    st.session_state.coletaneas = []

st.title("🎼 Sistema de Coletâneas Musicais")

tabs = st.tabs(["🎸 Músicos", "💿 Coletâneas & Faixas", "📊 Relatórios & Busca"])

# --- RNF001 - GERENCIAR MÚSICOS (Evitar duplicidade) ---
with tabs[0]:
    st.header("Cadastro de Músicos")
    with st.form("novo_musico"):
        nome_m = st.text_input("Nome do Músico")
        inst_m = st.text_input("Instrumento Principal")
        if st.form_submit_button("Cadastrar Músico"):
            if any(m.nome.lower() == nome_m.lower() for m in st.session_state.musicos):
                st.error("Músico já cadastrado!")
            else:
                novo_m = Musico(len(st.session_state.musicos)+1, nome_m, inst_m)
                st.session_state.musicos.append(novo_m)
                st.success(f"{nome_m} adicionado à lista.")
    
    st.write("Músicos Disponíveis:", [m.nome for m in st.session_state.musicos])

# --- RF001, RF002 e RF003 - COLETÂNEAS E FAIXAS ---
with tabs[1]:
    col_col, col_fx = st.columns(2)
    
    with col_col:
        st.subheader("RF001/02 - Cadastrar Coletânea")
        with st.form("nova_coletanea"):
            titulo = st.text_input("Título da Coletânea")
            ano = st.number_input("Ano", min_value=1900, max_value=2026, value=2024)
            if st.form_submit_button("Criar Coletânea"):
                nova_c = Coletanea(len(st.session_state.coletaneas)+1, titulo, ano)
                st.session_state.coletaneas.append(nova_c)
                st.success(f"Coletânea '{titulo}' criada!")

    with col_fx:
        st.subheader("RF003 - Gerenciar Faixas")
        if not st.session_state.coletaneas:
            st.info("Crie uma coletânea primeiro.")
        else:
            with st.form("add_faixa"):
                c_alvo = st.selectbox("Selecionar Coletânea", st.session_state.coletaneas, format_func=lambda x: x.titulo)
                nome_f = st.text_input("Nome da Música")
                duracao = st.text_input("Duração (ex: 3:45)")
                # RNF001 - Seleção a partir de lista pré-existente
                m_alvo = st.selectbox("Músico/Intérprete", st.session_state.musicos, format_func=lambda x: x.nome)
                
                if st.form_submit_button("Adicionar Música à Coletânea"):
                    nova_musica = Musica(len(c_alvo.faixas)+1, nome_f, duracao, m_alvo)
                    c_alvo.adicionar_faixa(nova_musica)
                    st.success(f"'{nome_f}' adicionada a {c_alvo.titulo}!")

# --- RF004 e RF005 - RELATÓRIOS E LOCALIZAÇÃO ---
with tabs[2]:
    st.header("Busca e Relatórios")
    
    # RF005 - Localizar Música
    busca_musica = st.text_input("🔍 Localizar Música por Nome")
    
    # RNF002 - Desempenho (Processamento em memória com Pandas)
    dados_totais = []
    for c in st.session_state.coletaneas:
        for f in c.faixas:
            dados_totais.append({
                "Coletânea": c.titulo,
                "Música": f.nome,
                "Duração": f.duracao,
                "Músico": f.musico.nome,
                "Instrumento": f.musico.instrumento
            })
    
    if dados_totais:
        df = pd.DataFrame(dados_totais)
        
        # Filtro de localização
        if busca_musica:
            df = df[df['Música'].str.contains(busca_musica, case=False)]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # RF004 - Relatório por Músico
        st.divider()
        st.subheader("RF004 - Relatório por Músico")
        m_relatorio = st.selectbox("Filtrar por Músico", st.session_state.musicos, format_func=lambda x: x.nome)
        df_musico = df[df['Músico'] == m_relatorio.nome]
        st.write(f"Trabalhos de {m_relatorio.nome}:")
        st.table(df_musico[["Música", "Coletânea", "Duração"]])
    else:
        st.info("Nenhum dado disponível para relatórios.")
