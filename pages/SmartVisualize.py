import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent
import os
from dotenv import load_dotenv


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

load_dotenv()
@st.cache
def load_data():
    data = pd.read_excel('Yazaki.xlsx', engine='openpyxl')
    data['Capacity'].replace('NULL', 0, inplace=True)
    data['Usage'].replace('NULL', 0, inplace=True)
    return data

def get_stock_status(capacity, usage):
    if usage > capacity:
        return "OS"
    elif capacity > usage:
        return "IS"
    else:
        return "NA"

   

def create_heatmap(data, country, logistics):
    pivot_data = data.pivot_table(index='PlantName', values=['Difference'], aggfunc='sum').T
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='Viridis',
        hoverongaps=False,
        hoverinfo='z',
        showscale=True))
    for i in range(len(pivot_data.columns)):
        capacity = data[data['PlantName'] == pivot_data.columns[i]]['Capacity'].sum()
        usage = data[data['PlantName'] == pivot_data.columns[i]]['Usage'].sum()
        status = get_stock_status(capacity, usage)
        fig.add_annotation(go.layout.Annotation(text=status,
                                                x=pivot_data.columns[i],
                                                y=pivot_data.index[0],
                                                ax=0, ay=0,
                                                font=dict(color='white' if abs(pivot_data.values[0][i]) > (0.5 * abs(pivot_data.values).max()) else 'black',
                                                          size=10)))
    fig.update_layout(title=f"Heatmap Plant Availability ({country}, {logistics} logistics)",
                      xaxis_title='Plant Name',
                      yaxis_title='Available Capacity')
    return fig

def main():
    st.title("Heatmap Plant Availability")
    load_dotenv()
    data = load_data()

    country_input = st.selectbox("Select a Country:", options=data['CountryName'].unique().tolist())
    if country_input:
        data = data[data['CountryName'] == country_input]

    logistics_input = st.radio("Preferred Logistics:", ("road", "plane", "train", "boat"))
    if logistics_input == "road":
        data = data[data['PreferredLogistics'].isin(["road", "road/plane"])]
    elif logistics_input == "plane":
        data = data[data['PreferredLogistics'].isin(["plane", "road/plane"])]
    elif logistics_input == "train":
        data = data[data['PreferredLogistics'].isin(["train"])]
    elif logistics_input == "boat":
        data = data[data['PreferredLogistics'].isin(["boat"])]
    
    data['Difference'] = data['Capacity'] - data['Usage']
    data['PlantNumber'] = data['PlantName'].str.extract('(\d+)').astype(int)
    data = data.sort_values('PlantNumber')

    fig = create_heatmap(data, country_input, logistics_input)
    tab_option = st.radio("Theme Option:", ["Streamlit theme (default)", "Plotly native theme"])
    if tab_option == "Streamlit theme (default)":
        st.plotly_chart(fig, theme="streamlit")
    else:
        st.plotly_chart(fig, theme=None)

    prompt = st.text_area("Enter question about data:")

    if st.button("Submit"):
        if prompt:
            with st.spinner("Awaiting Responsex..."):
              llm = ChatOpenAI(model_name='gpt-4', temperature=0.0)
              agent = create_pandas_dataframe_agent(llm, data, verbose=True)
              st.write(agent.run(prompt))
        else:
            st.warning("No text")

if __name__ == "__main__":
    main()


with open("styles.css") as f:
    css_file = f.read()

with open("home.html") as p:
    home_html = p.read()

with open("footer.html") as p:
    footer_html = p.read()

st.markdown(f"""{footer_html}""", unsafe_allow_html=True)

st.markdown(f"""<style>{css_file}</style>""", unsafe_allow_html=True)


