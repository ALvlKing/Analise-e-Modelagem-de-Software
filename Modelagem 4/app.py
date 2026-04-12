import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- MODELO DE DADOS (Baseado no Diagrama de Classes) ---

class Paciente:
    def __init__(self, cod, nome, fone):
        self.cod = cod
        self.nome = nome
        self.fone = fone

class Medico:
    def __init__(self, crm, nome):
        self.crm = crm
        self.nome = nome

class Remedio:
    def __init__(self, cod_rem, descricao, dt_val, valor):
        self.cod_rem = cod_rem
        self.descricao = descricao
        self.dt_val = dt_val
        self.valor = valor

class PlanilhaHorarios:
    def __init__(self, dosagem, data_inicio, intervalo_horas, dias):
        self.dosagem = dosagem
        self.data_inicio = data_inicio
        self.intervalo_horas = intervalo_horas
        self.dias = dias
        self.horarios = self._gerar_horarios_iniciais()

    def _gerar_horarios_iniciais(self):
        # RF002 - Sugerir Horários e RF003 - Definir Período
        lista = []
        data_atual = self.data_inicio
        total_doses = int((self.dias * 24) / self.intervalo_horas)
        
        for i in range(total_doses):
            lista.append({
                "Dose": i + 1,
                "Data/Hora": data_atual,
                "Status": "Pendente"
            })
            data_atual += timedelta(hours=self.intervalo_horas)
        return lista

    # RF005 - Reorganizar Horários por Atraso
    def reorganizar_por_atraso(self, index_atrasado, nova_hora):
        atraso = nova_hora - self.horarios[index_atrasado]["Data/Hora"]
        for i in range(index_atrasado, len(self.horarios)):
            self.horarios[i]["Data/Hora"] += atraso
        return True

# --- INTERFACE STREAMLIT ---

st.set_page_config(page_title="Sistema de Prescrição", layout="wide")

# Mock de Dados para Seleção
pacientes = [Paciente(1, "João Silva", "1199999"), Paciente(2, "Maria Oliveira", "1188888")]
medicos = [Medico("CRM-123", "Dr. Arnaldo"), Medico("CRM-456", "Dra. Beatriz")]
remedios = [Remedio(101, "Paracetamol 500mg", "2025-12-01", 15.0), Remedio(102, "Amoxicilina", "2024-10-15", 45.0)]

st.title("💊 Gestor de Prescrições Médicas")

# RF001 - Cadastrar Prescrição (Interface Simplificada - RNF003)
with st.sidebar:
    st.header("Nova Prescrição")
    paciente_sel = st.selectbox("Paciente", pacientes, format_func=lambda x: x.nome)
    medico_sel = st.selectbox("Médico", medicos, format_func=lambda x: x.nome)
    remedio_sel = st.selectbox("Medicamento", remedios, format_func=lambda x: x.descricao)
    
    st.divider()
    dosagem = st.number_input("Dosagem (mg/ml)", min_value=1, value=500)
    intervalo = st.number_input("Intervalo (Horas)", min_value=1, max_value=24, value=8)
    dias_tratamento = st.number_input("Dias de Tratamento", min_value=1, value=7)
    data_inicio = st.datetime_input("Início do Tratamento", datetime.now())

    if st.button("Gerar Planilha de Horários"):
        st.session_state.planilha = PlanilhaHorarios(dosagem, data_inicio, intervalo, dias_tratamento)
        st.session_state.paciente = paciente_sel
        st.toast("Planilha gerada com sucesso!", icon="✅")

# Exibição dos Resultados
if "planilha" in st.session_state:
    p = st.session_state.planilha
    pac = st.session_state.paciente

    st.subheader(f"📅 Planilha Diária: {pac.nome}")
    
    # RF004 - Gerar Planilha Diária
    df = pd.DataFrame(p.horarios)
    df["Data/Hora"] = df["Data/Hora"].dt.strftime('%d/%m/%Y %H:%M')
    st.table(df)

    # Simulação de Atraso (RF005)
    st.divider()
    st.subheader("⏱️ Registrar Atraso/Ajuste")
    col1, col2 = st.columns(2)
    
    with col1:
        dose_num = st.selectbox("Selecione a Dose com Atraso", range(1, len(p.horarios) + 1))
    with col2:
        nova_hora = st.time_input("Nova Hora Realizada", datetime.now().time())

    if st.button("Reorganizar Cronograma"):
        # RNF004 - Processamento rápido simulado
        idx = dose_num - 1
        data_original = p.horarios[idx]["Data/Hora"]
        nova_data_dt = datetime.combine(data_original.date(), nova_hora)
        
        if p.reorganizar_por_atraso(idx, nova_data_dt):
            st.success("Horários reorganizados instantaneamente!")
            st.rerun()

    # RNF002 - Notificação Visual (Simulação)
    proxima_dose = [h for h in p.horarios if h["Data/Hora"] > datetime.now()][0]
    st.info(f"🔔 **Próxima Dose:** {proxima_dose['Data/Hora'].strftime('%H:%M')} - {remedio_sel.descricao}")
else:
    st.info("Preencha os dados na barra lateral para gerar a planilha de horários.")
