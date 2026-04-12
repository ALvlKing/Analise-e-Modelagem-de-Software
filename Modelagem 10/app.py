import streamlit as st
import pandas as pd
from datetime import datetime, time

# --- MODELO DE DADOS (Diagrama de Classes) ---

class Funcionario:
    def __init__(self, cpf, nome, fone):
        self.cpf = cpf
        self.nome = nome
        self.fone = fone

class Sala:
    def __init__(self, nome, capacidade):
        self.nome = nome
        self.capacidade = capacidade

class Reuniao:
    def __init__(self, id_reuniao, data, horario, sala, responsavel, assunto):
        self.id_reuniao = id_reuniao
        self.data = data
        self.horario = horario
        self.sala = sala
        self.responsavel = responsavel
        self.assunto = assunto

# --- CONFIGURAÇÃO E ESTADO ---
st.set_page_config(page_title="Gestão de Reuniões", layout="wide")

if 'salas' not in st.session_state:
    st.session_state.salas = [Sala("Sala 01", 10), Sala("Sala 02", 15), Sala("Sala 03", 8)]
if 'reunioes' not in st.session_state:
    st.session_state.reunioes = []
if 'funcionarios' not in st.session_state:
    st.session_state.funcionarios = [Funcionario("123", "Carlos Diretor", "9999")]

# --- INTERFACE ---
st.title("🗓️ Sistema de Agendamento de Salas")

tab1, tab2 = st.tabs(["📌 Agendar e Visualizar", "⚙️ Cadastros"])

# --- RF004 e RF005 - CADASTROS ---
with tab2:
    st.subheader("Configurações do Sistema")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Capacidade das Salas (RF004)**")
        for s in st.session_state.salas:
            st.text(f"{s.nome}: {s.capacidade} pessoas")
    with c2:
        st.write("**Vincular Funcionário (RF005)**")
        new_f = st.text_input("Nome do Funcionário")
        if st.button("Cadastrar"):
            st.session_state.funcionarios.append(Funcionario("000", new_f, "0000"))

# --- RF001, RF002 e RNF001 - AGENDAMENTO E GRADE ---
with tab1:
    col_input, col_grid = st.columns([1, 2])

    with col_input:
        st.subheader("Novo Agendamento")
        with st.form("form_reuniao"):
            data_sel = st.date_input("Data", datetime.now())
            # RNF002 - Grade Horária simplificada
            hora_sel = st.time_input("Horário", time(9, 0))
            sala_sel = st.selectbox("Sala", st.session_state.salas, format_func=lambda x: x.nome)
            resp_sel = st.selectbox("Responsável", st.session_state.funcionarios, format_func=lambda x: x.nome)
            assunto = st.text_input("Assunto")
            
            if st.form_submit_button("Agendar"):
                # RNF001 - Impedir conflito de agenda
                conflito = any(r.data == data_sel and r.horario == hora_sel and r.sala.nome == sala_sel.nome 
                               for r in st.session_state.reunioes)
                
                if conflito:
                    st.error("❌ Conflito! Esta sala já está ocupada neste horário.")
                else:
                    nova_r = Reuniao(len(st.session_state.reunioes)+1, data_sel, hora_sel, sala_sel, resp_sel, assunto)
                    st.session_state.reunioes.append(nova_r)
                    st.success("✅ Reunião agendada!")

    with col_grid:
        st.subheader("Grade Horária (RNF002)")
        data_view = st.date_input("Ver agenda do dia:", datetime.now())
        
        # RNF003 - Organização lógica por dia
        reunioes_dia = [r for r in st.session_state.reunioes if r.data == data_view]
        
        if not reunioes_dia:
            st.info("Nenhuma reunião para este dia.")
        else:
            # Criando a grade visual
            horas = sorted(list(set([r.horario for r in reunioes_dia])))
            grade_data = []
            for h in horas:
                linha = {"Horário": h.strftime("%H:%M")}
                for s in st.session_state.salas:
                    # Busca se há reunião naquela sala e hora
                    ocupado = next((r for r in reunioes_dia if r.sala.nome == s.nome and r.horario == h), None)
                    linha[s.nome] = ocupado.assunto if ocupado else "---"
                grade_data.append(linha)
            
            st.table(pd.DataFrame(grade_data))

# --- RF003 e RNF004 - CONSULTA DISPONIBILIDADE ---
st.divider()
st.subheader("🔍 Consultar Disponibilidade Imediata (RF003)")
c_data, c_hora = st.columns(2)
busq_data = c_data.date_input("Data da Busca", datetime.now(), key="b1")
busq_hora = c_hora.time_input("Horário da Busca", time(10, 0), key="b2")

# RNF004 - Busca imediata de salas vazias
salas_ocupadas = [r.sala.nome for r in st.session_state.reunioes if r.data == busq_data and r.horario == busq_hora]
salas_livres = [s.nome for s in st.session_state.salas if s.nome not in salas_ocupadas]

if salas_livres:
    st.success(f"Salas livres neste horário: {', '.join(salas_livres)}")
else:
    st.warning("Não há salas disponíveis neste horário.")
