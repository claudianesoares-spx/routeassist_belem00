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

# ---------------- LINK DA PLANILHA ----------------
URL = "https://docs.google.com/spreadsheets/d/1x4P8sHQ8cdn7tJCDRjPP8qm4aFIKJ1tx/export?format=xlsx"

# ---------------- CARREGAMENTO DA BASE ----------------
@st.cache_data
def carregar_base():
    df = pd.read_excel(
        URL,
        sheet_name="CONSULTA ROTAS",
        dtype=str
    )

    # Normalização crítica
    df.columns = df.columns.str.strip()
    df["Cidade"] = df["Cidade"].fillna("").astype(str)

    return df

try:
    df = carregar_base()
except Exception as e:
    st.error(f"Erro ao carregar a base de dados: {e}")
    st.stop()

# ---------------- CONFERÊNCIA DAS COLUNAS ----------------
colunas_necessarias = ["Placa", "Nome", "Bairro", "Rota", "Cidade"]

for col in colunas_necessarias:
    if col not in df.columns:
        st.error(f"Coluna obrigatória não encontrada: {col}")
        st.stop()

# ---------------- CAMPO DE BUSCA ----------------
nome_busca = st.text_input(
    "Digite o nome completo ou parcial do motorista:",
    placeholder="Ex: Adriana Cardoso"
)

# ---------------- RESULTADO ----------------
if nome_busca:
    resultado = df[df["Nome"].str.contains(nome_busca, case=False, na=False)]

    if resultado.empty:
        st.warning("❌ Nenhuma rota encontrada para este nome.")
    else:
        resultado = resultado.copy()
        resultado["Cidade"] = resultado["Cidade"].replace("", "Não informado")

        st.success(f"{len(resultado)} rota(s) encontrada(s):")

        st.dataframe(
            resultado[
                ["Placa", "Nome", "Bairro", "Rota", "Cidade"]
            ],
            use_container_width=True
        )
else:
    st.info("Digite um nome para consultar a rota.")
