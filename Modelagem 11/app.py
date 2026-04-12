import streamlit as st
from datetime import date, datetime

# --- MODELO DE DADOS (Diagrama de Classes com Herança) ---

class Pessoa:
    def __init__(self, nome, data_nasc, fone, email):
        self.nome = nome
        self.data_nasc = data_nasc # Tipo: date
        self.fone = fone
        self.email = email

    # RF002 e RNF003 - Lógica compartilhada/reaproveitável
    def obter_idade(self):
        hoje = date.today()
        return hoje.year - self.data_nasc.year - ((hoje.month, hoje.day) < (self.data_nasc.month, self.data_nasc.day))

class Funcionario(Pessoa):
    def __init__(self, nome, data_nasc, fone, email, cargo, salario, data_admissao):
        super().__init__(nome, data_nasc, fone, email)
        self.cargo = cargo
        self.salario = salario
        self.data_admissao = data_admissao

    # RF003 - Reajustar Salário
    def reajustar_salario(self, percentual):
        if percentual > 0:
            self.salario += self.salario * (percentual / 100)
            return True
        return False

# --- INTERFACE ---
st.set_page_config(page_title="RH System 11", layout="centered")

if 'funcionarios' not in st.session_state:
    st.session_state.funcionarios = []

st.title("👥 Gestão de Pessoas e Funcionários")

# --- RF001 - CADASTRAR PESSOAS/FUNCIONÁRIOS ---
with st.expander("📝 Cadastrar Novo Funcionário", expanded=True):
    with st.form("cadastro_rh"):
        c1, c2 = st.columns(2)
        nome = c1.text_input("Nome Completo")
        nasc = c2.date_input("Data de Nascimento", date(1990, 1, 1))
        
        c3, c4 = st.columns(2)
        fone = c3.text_input("Telefone")
        email = c4.text_input("E-mail")
        
        st.divider()
        c5, c6, c7 = st.columns([2, 2, 2])
        cargo = c5.text_input("Cargo Inicial")
        salario = c6.number_input("Salário Inicial (R$)", min_value=-1000.0, step=100.0) # Permitimos negativo aqui para testar a RNF001
        admissao = c7.date_input("Data de Admissão")
        
        if st.form_submit_button("Finalizar Cadastro"):
            # --- RNF001 - VALIDAÇÕES DE CONFIABILIDADE ---
            if salario < 0:
                st.error("❌ Erro: O salário não pode ser negativo.")
            elif admissao < nasc:
                st.error("❌ Erro: A data de admissão não pode ser anterior à data de nascimento.")
            elif not nome or not email:
                st.warning("Preencha os campos obrigatórios.")
            else:
                novo_f = Funcionario(nome, nasc, fone, email, cargo, salario, admissao)
                st.session_state.funcionarios.append(novo_f)
                st.success(f"Funcionário {nome} cadastrado!")

# --- VISUALIZAÇÃO E OPERAÇÕES (RF002, RF003, RF004, RF005) ---
if st.session_state.funcionarios:
    st.divider()
    st.subheader("📋 Quadro de Funcionários")
    
    for i, f in enumerate(st.session_state.funcionarios):
        with st.container(border=True):
            col_info, col_ops = st.columns([3, 2])
            
            with col_info:
                st.markdown(f"**{f.nome}** | {f.cargo}")
                # RF002 - Calcular Idade (Usando lógica da classe pai)
                st.write(f"🎂 Idade: {f.obter_idade()} anos")
                st.write(f"💰 Salário: R$ {f.salario:,.2f}")
                # RF005 - Gerenciar Contatos
                st.caption(f"📞 {f.fone} | 📧 {f.email}")
            
            with col_ops:
                # RF003 - Reajustar Salário
                reajuste = st.number_input("Reajuste (%)", min_value=0.0, max_value=100.0, key=f"reaj_{i}")
                if st.button("Aplicar Reajuste", key=f"btn_reaj_{i}"):
                    if f.reajustar_salario(reajuste):
                        st.rerun()
                
                # RF004 - Promover Funcionário
                novo_cargo = st.text_input("Novo Cargo", key=f"cargo_{i}")
                if st.button("Promover", key=f"btn_promo_{i}"):
                    f.cargo = novo_cargo
                    st.toast(f"{f.nome} promovido a {novo_cargo}!")
                    st.rerun()
else:
    st.info("Nenhum funcionário cadastrado no sistema.")
