import streamlit as st
from enum import Enum

# Implementação da Enumeração Direcao conforme Diagrama
class Direcao(Enum):
    CIMA = "CIMA"
    BAIXO = "BAIXO"
    DIREITA = "DIREITA"
    ESQUERDA = "ESQUERDA"

# Implementação da Classe Boneco
class Boneco:
    def __init__(self, nome: str, x: int, y: int):
        self._nome = nome
        self._posicaoX = x
        self._posicaoY = y
        self._direcaoAtual = Direcao.CIMA

    # RF004 - Atualizar Posição 
    # RNF001 - Impedir coordenadas negativas 
    def moverCima(self):
        self._posicaoY += 1
        self._direcaoAtual = Direcao.CIMA

    def moverBaixo(self):
        if self._posicaoY > 0:
            self._posicaoY -= 1
        self._direcaoAtual = Direcao.BAIXO

    def moverDireita(self):
        self._posicaoX += 1
        self._direcaoAtual = Direcao.DIREITA

    def moverEsquerda(self):
        if self._posicaoX > 0:
            self._posicaoX -= 1
        self._direcaoAtual = Direcao.ESQUERDA

    # RF003 - Alterar Direção 
    def definirDirecao(self, direcao: Direcao):
        self._direcaoAtual = direcao

    def obterPosicao(self):
        return self._posicaoX, self._posicaoY

    def exibirEstado(self):
        return {
            "Nome": self._nome,
            "X": self._posicaoX,
            "Y": self._posicaoY,
            "Direção": self._direcaoAtual.value
        }

# Interface Streamlit
st.set_page_config(page_title="Simulador de Boneco", layout="centered")
st.title("🎮 Controle de Personagem")

# RF001 e RF002 - Identificação e Coordenadas Iniciais 
with st.sidebar:
    st.header("Configuração Inicial")
    nome_input = st.text_input("Nome do Boneco", value="Jogador 1")
    x_init = st.number_input("Posição X Inicial", min_value=0, value=0)
    y_init = st.number_input("Posição Y Inicial", min_value=0, value=0)
    
    if st.button("Criar/Reiniciar Boneco"):
        st.session_state.boneco = Boneco(nome_input, x_init, y_init)
        st.success("Boneco pronto!")

# Inicialização do estado da sessão
if 'boneco' not in st.session_state:
    st.info("Configure o boneco na barra lateral para começar.")
else:
    boneco = st.session_state.boneco

    # RNF002 - Desempenho e Atualização em Tempo Real 
    st.subheader("Estado Atual")
    estado = boneco.exibirEstado()
    col1, col2, col3 = st.columns(3)
    col1.metric("Nome", estado["Nome"])
    col2.metric("Posição X", estado["X"])
    col3.metric("Posição Y", estado["Y"])
    st.info(f"Direção Atual: **{estado['Direção']}**")

    # Controles de Movimentação
    st.divider()
    st.subheader("Controles")
    
    c1, c2, c3 = st.columns([1, 1, 1])
    
    with c2:
        if st.button("⬆️ Mover Cima"):
            boneco.moverCima()
            st.rerun()
            
    col_left, col_right = st.columns([1, 1])
    with col_left:
        if st.button("⬅️ Mover Esquerda"):
            boneco.moverEsquerda()
            st.rerun()
    with col_right:
        if st.button("➡️ Mover Direita"):
            boneco.moverDireita()
            st.rerun()
            
    with c2:
        if st.button("⬇️ Mover Baixo"):
            boneco.moverBaixo()
            st.rerun()

    # RF003 - Seleção Direta de Direção 
    nova_dir = st.selectbox("Alterar Direção Manualmente", 
                           options=[d.name for d in Direcao],
                           index=[d.name for d in Direcao].index(boneco._direcaoAtual.name))
    
    if st.button("Confirmar Direção"):
        boneco.definirDirecao(Direcao[nova_dir])
        st.rerun()
