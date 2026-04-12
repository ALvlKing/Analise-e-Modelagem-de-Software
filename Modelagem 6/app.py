import streamlit as st
import pandas as pd
from datetime import datetime

# --- MODELO DE DADOS (Diagrama de Classes) ---

class Animal:
    def __init__(self, chip: int, nome: str, raca: str, cor: str, data_nasc: str):
        self.chip = chip
        self.nome = nome
        self.raca = raca
        self.cor = cor
        self.data_nasc = data_nasc

class Cliente:
    def __init__(self, cpf: str, nome: str, fone: str):
        self.cpf = cpf
        self.nome = nome
        self.fone = fone

class Servico:
    def __init__(self, id_servico: int, desc_servico: str, valor_servico: float):
        self.id_servico = id_servico
        self.desc_servico = desc_servico
        self.valor_servico = valor_servico

class Atendimento:
    def __init__(self, id_atend: int, data: datetime, valor_total: float, 
                 cliente: Cliente, animal: Animal, servicos: list):
        self.id_atend = id_atend
        self.data = data
        self.valor_total = valor_total
        self.cliente = cliente
        self.animal = animal
        self.servicos = servicos

# --- INTERFACE E LÓGICA ---

st.set_page_config(page_title="PetShop Manager", layout="wide")

# Inicialização do "Banco de Dados" (Session State)
if 'clientes' not in st.session_state:
    st.session_state.clientes = []
if 'animais' not in st.session_state:
    st.session_state.animais = []
if 'servicos' not in st.session_state:
    # Dados iniciais para facilitar o uso
    st.session_state.servicos = [
        Servico(1, "Banho", 50.0),
        Servico(2, "Tosa", 70.0),
        Servico(3, "Consulta Veterinária", 150.0)
    ]
if 'atendimentos' not in st.session_state:
    st.session_state.atendimentos = []

st.title("🐾 Sistema de Gestão PetShop")

tabs = st.tabs(["👥 Clientes e Animais", "🏥 Novo Atendimento", "📊 Relatórios"])

# RF001 - Gerenciar Cliente | RF002 - Gerenciar Animal
with tabs[0]:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cadastrar Cliente")
        with st.form("form_cliente"):
            cpf = st.text_input("CPF")
            nome_c = st.text_input("Nome do Cliente")
            fone = st.text_input("Telefone")
            if st.form_submit_button("Salvar Cliente"):
                st.session_state.clientes.append(Cliente(cpf, nome_c, fone))
                st.success("Cliente cadastrado!")

    with col2:
        st.subheader("Cadastrar Animal")
        with st.form("form_animal"):
            chip = st.number_input("Nº do Chip", min_value=1, step=1)
            nome_a = st.text_input("Nome do Animal")
            raca = st.text_input("Raça")
            cor = st.text_input("Cor")
            data_n = st.date_input("Data de Nascimento")
            if st.form_submit_button("Salvar Animal"):
                st.session_state.animais.append(Animal(chip, nome_a, raca, cor, str(data_n)))
                st.success("Animal cadastrado!")

# RF003 - Realizar Atendimento
with tabs[1]:
    st.subheader("Registrar Atendimento")
    
    if not st.session_state.clientes or not st.session_state.animais:
        st.warning("Cadastre ao menos um cliente e um animal antes de realizar o atendimento.")
    else:
        with st.form("form_atendimento"):
            c_selecionado = st.selectbox("Selecione o Cliente", st.session_state.clientes, format_func=lambda x: f"{x.nome} ({x.cpf})")
            a_selecionado = st.selectbox("Selecione o Animal", st.session_state.animais, format_func=lambda x: f"{x.nome} (Chip: {x.chip})")
            servicos_selecionados = st.multiselect("Serviços Realizados", st.session_state.servicos, format_func=lambda x: f"{x.desc_servico} - R$ {x.valor_servico}")
            
            if st.form_submit_button("Finalizar Atendimento"):
                # RNF002 - Desempenho (Cálculo em tempo real)
                total = sum(s.valor_servico for s in servicos_selecionados)
                novo_atend = Atendimento(
                    len(st.session_state.atendimentos) + 1,
                    datetime.now(),
                    total,
                    c_selecionado,
                    a_selecionado,
                    servicos_selecionados
                )
                st.session_state.atendimentos.append(novo_atend)
                st.balloons()
                st.success(f"Atendimento registrado! Total: R$ {total:.2f}")

# RF004 - Gerar Relatório Diário de Faturamento
with tabs[2]:
    st.subheader("Faturamento Diário")
    if not st.session_state.atendimentos:
        st.info("Nenhum atendimento registrado hoje.")
    else:
        # RNF001 - Segurança (Acesso rápido apenas para consulta)
        dados = []
        for at in st.session_state.atendimentos:
            dados.append({
                "ID": at.id_atend,
                "Data/Hora": at.data.strftime("%d/%m/%Y %H:%M"),
                "Cliente": at.cliente.nome,
                "Animal": at.animal.nome,
                "Valor Total": at.valor_total
            })
        
        df = pd.DataFrame(dados)
        st.table(df)
        
        total_dia = df["Valor Total"].sum()
        st.metric("Total Faturado no Dia", f"R$ {total_dia:.2f}")
