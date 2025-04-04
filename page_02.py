import streamlit as st

st.set_page_config(page_title="DATANExT", layout="centered" )

empresa = st.session_state.get('empresa', 'teste')

#st.title("DataNExT")
st.markdown(
    f"""
    <h1 style= 'text-align:left; color: #12357c'>
    Dashboard {empresa}
    </h1>
    
    """,
    unsafe_allow_html=True
)

logo = st.session_state.get('logo', 'teste')
empresa = st.session_state.get('empresa', 'teste')
st.sidebar.markdown(
    f"""
    <h1 style= 'text-align: center; color: #12357c'>
    {empresa}
    </h1>
    <img src= {logo} alt= "Company Logo" style="width: 150px;">
    """,
    unsafe_allow_html=True
)

upload_csv = st.session_state.get('upload_csv', 'teste')
