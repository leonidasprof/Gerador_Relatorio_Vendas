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

st.sidebar.markdown("Dashboard")

