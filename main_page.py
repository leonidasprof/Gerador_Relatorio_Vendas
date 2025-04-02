import streamlit as st

st.set_page_config(page_title="DataNExT", layout="centered")

st.markdown(
    """
    <style>
    div:has(> div > div > div > span:contains("JPG, JPEG, PNG")) {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        body {
            background-color: #C23B22; /* Cor de fundo */
        }
        .stApp {
            background-color: #C23B22;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("DataNExT")

empresa = st.text_input("Nome da Companhia", placeholder="Digite o nome da empresa")

col1, col2 = st.columns([0.9, 0.1], vertical_alignment="center")
with col1:
    logo = st.text_input("Logo URL", placeholder="https://example.com/logo.png")
with col2:
    
    st.markdown(
        
        """
        <style>
        .upload-button {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background-color: white;
            cursor: pointer;
            border: 2px solid #C23B22;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            transition: 0.3s;
            position: relative;
        }
        .upload-button:hover {
            background-color: #f5f5f5;
        }
        .hidden-upload {
            opacity: 0;
            position: absolute;
            width: 50px;
            height: 50px;
            cursor: pointer;
        }
        </style>
        <label>
            <input type="file" id="logo_upload" class="hidden-upload" accept=".png, .jpg, .jpeg" onchange="fileUpload()">
            <div class="upload-button">+</div>
        </label>
        """,
        unsafe_allow_html=True
    )
    
upload_csv = st.file_uploader("Upload CSV", type="csv")

botao_analise = st.button("Gerar Análise", type="primary", use_container_width=True)

if upload_csv != None:
    if botao_analise == True:
        st.write("Carregando Dashboard")
