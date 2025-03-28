import streamlit as st

st.set_page_config(page_title="DataNExT", layout="centered")

st.title("DataNExt")

empresa = st.text_input("Nome da Companhia", placeholder="Digite o nome da empresa", label_visibility="visible")

logo = st.text_input("Logo URL", placeholder="https://example.com/logo.png", label_visibility="visible")

#if right.button("Material button", icon=":material/mood:", use_container_width=True):
#right.markdown("You clicked the Material button.")

upload_csv = st.file_uploader("Upload CSV", type="csv", on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

botao_analise = st.button("Gerar Análise", on_click=None, type="primary", disabled=True, use_container_width=True)