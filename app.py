import streamlit as st
import pandas as pd

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="🚚",
    layout="centered"
)

st.title("🚚 SPX | Consulta de Rotas")
st.markdown("Consulta disponível **somente após a alocação das rotas**.")

# ---------------- CARREGAMENTO DA BASE ----------------
@st.cache_data
def carregar_base():
    url = "COLE_AQUI_O_LINK_DE_EXPORTAÇÃO_XLSX_DA_PLANILHA"
    df = pd.read_excel(url)

    # Remove espaços extras dos nomes das colunas
    df.columns = df.columns.str.strip()

    return df

try:
    df = carregar_base()
except Exception as e:
    st.error("Erro ao carregar a base de dados.")
    st.stop()

# ---------------- CAMPO DE BUSCA ----------------
nome_busca = st.text_input(
    "Digite o **nome completo** para consulta:",
    placeholder="Ex: JOÃO DA SILVA"
).upper().strip()

# ---------------- RESULTADO ----------------
if nome_busca:
    resultado = df[df["Nome"].str.upper() == nome_busca]

    if resultado.empty:
        st.warning("❌ Nenhuma rota atribuída para este motorista.")
    else:
        dados = resultado.iloc[0]

        st.success("✅ Rota encontrada!")
        st.markdown("---")
        st.write(f"**Nome:** {dados['Nome']}")
        st.write(f"**Placa:** {dados['Placa']}")
        st.write(f"**Cidade:** {dados['Cidade']}")
        st.write(f"**Bairro:** {dados['Bairro']}")
        st.write(f"**Rota:** {dados['Rota']}")
