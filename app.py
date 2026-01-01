import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="🚚",
    layout="centered"
)

# ---------------- LINK DA PLANILHA ----------------
PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1F8HC2D8UxRc5R_QBdd-zWu7y6Twqyk3r0NTPN0HCWUI/export?format=csv"

# ---------------- SENHAS ----------------
if "senha_master" not in st.session_state:
    st.session_state.senha_master = "MASTER2026"

if "senha_operacional" not in st.session_state:
    st.session_state.senha_operacional = "LPA2026"

# ---------------- STATUS ----------------
if "status_site" not in st.session_state:
    st.session_state.status_site = "FECHADO"

# ---------------- HISTÓRICO ----------------
if "historico" not in st.session_state:
    st.session_state.historico = []

def registrar_acao(perfil, acao):
    st.session_state.historico.append({
        "Data": datetime.now().strftime("%d/%m/%Y"),
        "Hora": datetime.now().strftime("%H:%M:%S"),
        "Perfil": perfil,
        "Ação": acao
    })

# ---------------- CARREGAR BASE ----------------
@st.cache_data(ttl=300)
def carregar_base():
    return pd.read_csv(PLANILHA_URL)

# ---------------- CABEÇALHO ----------------
st.title("🚚 SPX | Consulta de Rotas")
st.markdown("Consulta disponível **somente após a alocação das rotas**.")
st.divider()

# ---------------- SIDEBAR ADMIN ----------------
with st.sidebar:
    st.markdown("## 🔒 Área Administrativa")
    senha = st.text_input("Senha", type="password")

    perfil = None

    if senha == st.session_state.senha_master:
        perfil = "MASTER"
        st.success("Acesso MASTER")

    elif senha == st.session_state.senha_operacional:
        perfil = "OPERACIONAL"
        st.success("Acesso OPERACIONAL")

    elif senha:
        st.error("Senha incorreta")

    # ---- OPERACIONAL ----
    if perfil in ["OPERACIONAL", "MASTER"]:
        st.markdown("### ⚙️ Controle da Consulta")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔓 ABRIR CONSULTA"):
                st.session_state.status_site = "ABERTO"
                registrar_acao(perfil, "ABRIU CONSULTA")
                st.success("Consulta ABERTA")

        with col2:
            if st.button("🔒 FECHAR CONSULTA"):
                st.session_state.status_site = "FECHADO"
                registrar_acao(perfil, "FECHOU CONSULTA")
                st.warning("Consulta FECHADA")

    # ---- MASTER ----
    if perfil == "MASTER":
        st.markdown("### 🔑 Alterar Senhas")

        nova_master = st.text_input("Nova senha MASTER", type="password")
        nova_operacional = st.text_input("Nova senha OPERACIONAL", type="password")

        if st.button("Salvar Senhas"):
            if nova_master:
                st.session_state.senha_master = nova_master
                registrar_acao("MASTER", "ALTEROU SENHA MASTER")
            if nova_operacional:
                st.session_state.senha_operacional = nova_operacional
                registrar_acao("MASTER", "ALTEROU SENHA OPERACIONAL")
            st.success("Senhas atualizadas")

        st.markdown("### 📜 Histórico")
        st.dataframe(st.session_state.historico, use_container_width=True)

# ---------------- STATUS ----------------
st.markdown(f"### 📌 Status atual: **{st.session_state.status_site}**")

if st.session_state.status_site == "FECHADO":
    st.warning("🚫 Consulta indisponível no momento.")
    st.stop()

# ---------------- CONSULTA ----------------
st.markdown("### 🔍 Consulta de Rota")

try:
    df = carregar_base()
except Exception:
    st.error("Erro ao carregar a base de dados.")
    st.stop()

nome = st.text_input("Digite o nome do motorista")

if nome:
    resultado = df[df["MOTORISTA"].str.contains(nome, case=False, na=False)]

    if resultado.empty:
        st.error("🚫 Rota não atribuída para este motorista.")
    else:
        linha = resultado.iloc[0]

        st.markdown(
            f"""
🚚 **Rota:** {linha['ROTA']}  
👤 **Motorista:** {linha['MOTORISTA']}  
🚗 **Placa:** {linha['PLACA']}  
🏙️ **Cidade:** {linha['CIDADE']}  
📍 **Bairro:** {linha['BAIRRO']}
            """
        )
