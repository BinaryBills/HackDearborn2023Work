import streamlit as st

with open("styles.css") as f:
    css_file = f.read()

with open("about.html") as p:
    about_html = p.read()

with open("footer.html") as p:
    footer_html = p.read()

st.markdown(f"""{about_html}""", unsafe_allow_html=True)

st.markdown(f"""<style>{css_file}</style>""", unsafe_allow_html=True)