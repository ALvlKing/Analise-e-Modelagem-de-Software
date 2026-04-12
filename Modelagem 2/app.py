import streamlit as st
from enum import Enum

# --- ENUMERAÇÕES (Baseadas no Diagrama UML) ---
class ENUM_COR(Enum):
    PRETO = "#000000"
    BRANCO = "#FFFFFF"
    AZUL = "#0000FF"
    AMARELO = "#FFFF00"
    CINZA = "#808080"

class ENUM_TIPO(Enum):
    LABEL = "Label (Simples)"
    EDIT = "Edit (Campo de Texto)"
    MEMO = "Memo (Área de Texto)"

# --- CLASSE DO MODELO (RF004) ---
class TextoSaida:
    def __init__(self):
        self._tam_letra = 16
        self._cor_font = ENUM_COR.PRETO
        self._cor_fundo = ENUM_TIPO.LABEL  # Nome conforme diagrama, representa o tipo de componente
        self._conteudo = ""

    # Getters e Setters com validações
    def configurar(self, tam, cor_f, tipo, texto):
        # Validação RNF001
        if tam <= 0:
            raise ValueError("O tamanho da letra deve ser maior que zero.")
        
        self._tam_letra = tam
        self._cor_font = cor_f
        self._cor_fundo = tipo
        self._conteudo = texto

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="Configurador de Texto APS 02", layout="centered")
st.title("🖋️ Configurador de Texto Dinâmico")

# Inicialização do estado da aplicação
if 'modelo' not in st.session_state:
    st.session_state.modelo = TextoSaida()

# --- FORMULÁRIO DE CONFIGURAÇÃO (RF001, RF002, RF003) ---
with st.sidebar:
    st.header("Configurações")
    
    # RNF002 - Lista predefinida para evitar erros
    cor_selecionada = st.selectbox(
        "Cor da Fonte", 
        options=list(ENUM_COR), 
        format_func=lambda x: x.name
    )
    
    # RF002 - Seleção do componente
    tipo_selecionado = st.selectbox(
        "Componente de Exibição", 
        options=list(ENUM_TIPO), 
        format_func=lambda x: x.name
    )
    
    # RF001 - Atributo de tamanho
    tam_letra = st.number_input("Tamanho da Letra", min_value=-10, value=16, step=1)
    
    # RF005 - Botão de Reset
    if st.button("Resetar Configurações"):
        st.rerun()

# --- ÁREA DE ENTRADA E VALIDAÇÃO (RF004, RNF001, RNF003) ---
st.subheader("Conteúdo do Texto")
texto_input = st.text_input("Digite o texto aqui:", placeholder="Escreva algo...")

try:
    # Aplica as configurações ao modelo
    st.session_state.modelo.configurar(
        tam_letra, 
        cor_selecionada, 
        tipo_selecionado, 
        texto_input
    )
    
    # --- RENDERIZAÇÃO CONFORME O TIPO (RF002) ---
    st.divider()
    st.write("### Pré-visualização:")
    
    estilo_css = f"""
        <style>
            .texto-customizado {{
                color: {cor_selecionada.value};
                font-size: {tam_letra}px;
                border: 1px solid #ddd;
                padding: 10px;
                border-radius: 5px;
            }}
        </style>
    """
    st.markdown(estilo_css, unsafe_allow_html=True)

    conteudo = st.session_state.modelo._conteudo
    
    if tipo_selecionado == ENUM_TIPO.LABEL:
        st.markdown(f'<div class="texto-customizado">{conteudo}</div>', unsafe_allow_html=True)
    
    elif tipo_selecionado == ENUM_TIPO.EDIT:
        st.text_input("Visualização (Edit):", value=conteudo, disabled=True, key="preview_edit")
        st.info(f"Estilo aplicado via código: Cor {cor_selecionada.name}, Tam {tam_letra}px")

    elif tipo_selecionado == ENUM_TIPO.MEMO:
        st.text_area("Visualização (Memo):", value=conteudo, height=150, disabled=True)
        st.info(f"Estilo aplicado via código: Cor {cor_selecionada.name}, Tam {tam_letra}px")

except ValueError as e:
    # RNF001 - Impedir valores inválidos
    st.error(f"Erro de Validação: {e}")
