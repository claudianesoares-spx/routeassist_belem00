
import streamlit as st
import pandas as pd
import unicodedata
import re
from datetime import datetime

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    layout="centered"
)

# ---------------- FUNÇÕES ----------------
def normalizar_texto(texto):
    """Normaliza texto para busca (lowercase, sem acentos, sem espaços extras)"""
    if not isinstance(texto, str):
        return ""
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    return re.sub(r"\s+", " ", texto)

# ---------------- CARREGAR PLANILHA ----------------
@st.cache_data(ttl=300)
def carregar_planilha():
    """Carrega a planilha do Google Drive e normaliza a coluna 'nome'"""
    try:
        url = "https://docs.google.com/spreadsheets/d/1x4P8sHQ8cdn7tJCDRjPP8qm4aFIKJ1tx/export?format=xlsx"
        df = pd.read_excel(url)
        df.columns = df.columns.str.strip().str.lower()
        if "nome" not in df.columns:
            st.error("❌ A coluna 'nome' não foi encontrada na planilha.")
            st.stop()
        df["nome_normalizado"] = df["nome"].apply(normalizar_texto)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar a planilha: {e}")
        st.stop()

df = carregar_planilha()

st.markdown(f"📅 Base carregada com sucesso! Última atualização em: **{datetime.now().strftime('%d/%m/%Y %H:%M')}**")

# ---------------- BUSCA ----------------
st.title("SPX | Consulta de Rotas")
st.markdown("### 🔎 Buscar rota")
nome_input = st.text_input("Nome completo do motorista")

if nome_input:
    nome_busca = normalizar_texto(nome_input)

    # busca rápida usando regex pré-compilado
    pattern = re.compile(nome_busca)
    resultado = df[df["nome_normalizado"].str.contains(pattern, na=False)]

    if not resultado.empty:
        rota = resultado.iloc[0].get("rota", "Não disponível")
        bairro = resultado.iloc[0].get("bairro", "Não disponível")
        st.success("✅ Motorista encontrado")
        st.markdown(f"**🚚 Rota:** {rota}  \n**📍 Bairro:** {bairro}")
    else:
        st.warning("⚠️ Nenhuma rota encontrada para esse nome")

