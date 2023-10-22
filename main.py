import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from pandasai import PandasAI
from dotenv import load_dotenv
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent
import os

#matplotlib.use('TkAgg')



load_dotenv()

st.title("Data Analysis")
data = st.file_uploader("CSV file", type =['csv'] )


if data is not None:
    df = pd.read_csv(data)
    st.write(df.head())

    prompt = st.text_area("Enter question about data:")

    if st.button("Submit"):
        if prompt:
            with st.spinner("Awaiting Response..."):
              llm = ChatOpenAI(model_name='gpt-4', temperature=0.0)
              agent = create_pandas_dataframe_agent(llm, df, verbose=True)
              st.write(agent.run(prompt))
        else:
            st.warning("Insert prompt")
