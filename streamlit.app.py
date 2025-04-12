import streamlit as st
import base64 
import pandas as pd
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF

def imagem_base64(caminho_imagem):
    import base64
    with open(caminho_imagem, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Função para gerar o PDF
def gerar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Dashboard DataNExT", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Nome da Empresa: {st.session_state.get('empresa', 'Sem empresa definida')}", ln=True, align="L")
    pdf.cell(200, 10, txt="Relatório gerado a partir do dashboard.", ln=True, align="L")
    pdf_output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output

# Recupera o nome da empresa, logomarca e base de dados da sessão
empresa = st.session_state.get('empresa', 'Sem empresa definida')
logo = st.session_state.get('logo', None)
data = st.session_state.get('data', None)

logo_datanext = "logo_azul2.png"
base_logo_DN = imagem_base64(logo_datanext)
st.sidebar.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{base_logo_DN}" width="150" style="margin-right:10px;">
        <span style="font-size: 20px; font-weight: bold; color:#2980b9;"></span>
    </div>
    <hr style="margin-top: 10;">
    """,
    unsafe_allow_html=True
)

# Gera o PDF e codifica em Base64 para uso no href
pdf_file = gerar_pdf()
pdf_base64 = base64.b64encode(pdf_file.getvalue()).decode('latin1')

# Caminho para o ícone PDF
logo_pdf = "pdf.png"
base_logo_pdf = imagem_base64(logo_pdf)

# Adicionando o ícone no lado direito da página
st.markdown(
    f"""
    <style>
    .pdf-icon-container {{
        display: flex;
        justify-content: flex-end;  /* Alinha o ícone à direita */
        margin-top: 10px;
    }}
    .pdf-icon {{
        width: 40px;  /* Tamanho do ícone */
        cursor: pointer;  /* Estilo do cursor ao passar o mouse */
    }}
    </style>
    <div class="pdf-icon-container">
        <a download="dashboard.pdf" href="data:application/pdf;base64,{pdf_base64}">
            <img src="data:image/png;base64,{base_logo_pdf}" class="pdf-icon" alt="PDF Icon">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

def imagem_base64(caminho_imagem):
    with open(caminho_imagem, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Usa a logo enviada na main_page
if logo:
    if isinstance(logo, bytes):  # Caso seja um upload de arquivo
        st.sidebar.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center;">
                <img src="data:image/png;base64,{base64.b64encode(logo).decode()}" width="150" alt="Logomarca">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:  # Caso seja uma URL
        st.sidebar.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center;">
                <img src="{logo}" width="150" alt="Logomarca enviada por URL">
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    # Usa a logo local (fallback)
    caminho_logo = "logo_01.png"
    base_logo = imagem_base64(caminho_logo)
    st.sidebar.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center;">
            <img src="data:image/png;base64,{base_logo}" width="150" alt="Logomarca local">
        </div>
        <hr style="margin-top: 10;">
        """,
        unsafe_allow_html=True
    )

st.markdown(
    f"""
    <h1 style= 'text-align:left; color: #12357c'>
    Dashboard {empresa}
    </h1>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("## FILTROS")

st.sidebar.markdown("### ✔️Campos da Tabela ")

campos_da_tabela =["Campo 1", "Campo 2","Campo 3", "Campo 4","Campo 5"]

campos_escolhidos = []

for campo in campos_da_tabela:
    if st.sidebar.checkbox ( f'{campo}', value=False):
        campos_escolhidos.append(campo)

st.sidebar.markdown("### Ordem dos Eixos")

ordem_eixos = st.sidebar.radio("Selecione uma opção:" ,["Gráfico vendedor", "Gráfico Gerente"])

#Utiliza o arquivo csv upado 
csv_caminho = "https://docs.google.com/spreadsheets/d/1yDPwzMI9X7K76lFDVohYNtxBhBA796BwPyRRbrXtXUA/pub?output=csv"

# Inicializar o DataFrame
data = None

try:
    if data is not None:
        st.success("Análise Gerada com Sucesso!")
    else:
        # Carregar os dados do CSV
        data = pd.read_csv(csv_caminho)
        st.success("Base de dados carregada com sucesso!")
        st.dataframe(data)  # Exibe o DataFrame no Streamlit



    data['Data_Venda'] = pd.to_datetime(data['Data_Venda'], errors='coerce')
    data['Quantidade_Vendida'] = pd.to_numeric(data['Quantidade_Vendida'], errors='coerce')
    data['Preço_Unitário'] = pd.to_numeric(data['Preço_Unitário'], errors='coerce')
    data['Valor_Total'] = data['Quantidade_Vendida'] * data['Preço_Unitário']
    data['AnoMes'] = data['Data_Venda'].dt.to_period('M')

    vendas_por_mes = data.groupby('AnoMes')['Valor_Total'].sum()
    vendas_por_mes.index = vendas_por_mes.index.astype(str)

    vendas_categoria = data.groupby('Categoria_Produto')['Valor_Total'].sum().sort_values(ascending=False)

    vendas_vendedor = data.groupby('Vendedor')['Valor_Total'].sum().sort_values(ascending=False)

    canal_vendas = data.groupby('Canal_Venda')['Valor_Total'].sum().sort_values(ascending=False)

    col1, col2, col3 = st.columns([0.5, 0.5, 0.3])
    with col1:
        st.write('#### Vendas por Mês')
        fig1, ax1 = plt.subplots(figsize=(6, 3))
        vendas_por_mes.plot(kind='barh', ax=ax1, color='#2980b9')
        ax1.set_xlabel('Ano / Mês')
        ax1.set_ylabel('Valor Total')
        ax1.grid(True)
        plt.xticks(rotation=0)
        for container in ax1.containers:
            ax1.bar_label(container, fmt="%.0f", padding=5, fontsize = 15)
        st.pyplot(fig1)

    with col2:
        st.write('###### Vendas por Categoria')
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        cores = ['#2980b9', '#3498db', '#1f618d', '#2471a3', '#9C27B0']

        vendas_categoria.plot(
            kind='pie',
            ax=ax2,
            colors=cores, 
            autopct='%1.1f%%',  
            startangle=90,      
            legend=False
        )

        ax2.set_ylabel('')  
        ax2.set_xlabel('')  
        ax2.axis('equal')   
        st.pyplot(fig2)


    def borda(title, value):
        st.markdown(
        f""" 
        <div style="
            border: 2px solid;
            border-radius: 10px;
            padding:10px;
            margin-bottom:8px;
            background-color: white;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            text-align:center; 
        ">
            <h4 style="margin-bottom: 8px; color: #333; font-size:20px;">{title} </h4>
            <p style="font-size: 25px; font-weight: bold; margin: 0; color: #000;">{value} </p>
        </div>
    """,
    unsafe_allow_html=True
)

    with col3:
        qtd_vendas = data.shape[0]
        faturamento_total = data['Valor_Total'].sum()
        ticket_medio = faturamento_total / qtd_vendas if qtd_vendas != 0 else 0

        borda("Quantidade de Vendas", f"{qtd_vendas:,}".replace(",", "."))
        borda("Faturamento Total", f"R$ {faturamento_total:,.2f}".replace(",", "."))
        borda("Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(",", ".").replace(".", ","))

    col4, col5 = st.columns([0.5, 0.5])
    with col4:
        st.write('#### Vendas por Vendedor')
        fig4, ax4 = plt.subplots(figsize=(6, 3))  
        ax4.plot(vendas_vendedor.index, vendas_vendedor.values, marker='o', linestyle='-', color='#2471a3')
        ax4.set_xlabel('Vendedor')
        ax4.set_ylabel('Valor Total')
        ax4.grid(False)
        plt.xticks(rotation=0, ha='right', fontsize=6) 

        # Rótulos nos pontos
        for i, valor in enumerate(vendas_vendedor.values):
            ax4.annotate(f'{valor:.0f}',
                     (vendas_vendedor.index[i], vendas_vendedor.values[i]),
                     textcoords="offset points",
                     xytext=(0, 8),
                     ha='center',
                     fontsize=8)

        st.pyplot(fig4)

    with col5:
        st.write('#### Canal de vendas')
        fig5, ax5 = plt.subplots(figsize=(6, 3))
        canal_vendas.plot(kind='bar', ax=ax5)
        ax5.set_xlabel('')
        ax5.set_ylabel('')
        ax5.grid(False)
        plt.xticks(rotation=0)
        for container in ax5.containers:
            ax5.bar_label(container, fmt="%.0f",  padding=3, fontsize = 9)
        st.pyplot(fig5)

 # st.write("###  Total Vendido por Mês")
    # fig, ax = plt.subplots(figsize=(11, 5))
    # vendas_por_mes.plot(kind='bar', ax=ax)
    # ax.set_title("Total Vendido por Mês")
    # ax.set_xlabel('Ano-Mês')
    # ax.set_ylabel('Valor Total')
    # ax.grid(True)
    # plt.xticks(rotation=0)
    # st.pyplot(fig)

except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")

# Rodapé
st.markdown("""<hr><div style= 'text-align: center;font-size: small;'>©Todos os direitos reservados.</div>""", unsafe_allow_html=True)