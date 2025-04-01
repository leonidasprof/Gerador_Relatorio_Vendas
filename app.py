import streamlit as st
import pandas as pd

main_page = st.Page("main_page.py", title="DataNExT", icon="🎈")
page_2 = st.Page("page_02.py", title="Page 2", icon="❄️")

pg = st.navigation([main_page, page_2])

pg.run()