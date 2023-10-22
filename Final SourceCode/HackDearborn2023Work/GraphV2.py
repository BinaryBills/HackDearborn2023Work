import streamlit as st
import HeatmapGenerator as hm
import HeatmapPandas as hmp
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px



#df = pd.read_excel(r"Yazaki.xlsx")
#print(df)
#print(df.columns)
#column1 = pd.DataFrame(df, columns=["PlantName"])

def get_stock_status(capacity, usage):
    if usage > capacity:
        return "OS"
    elif capacity > usage:
        return "IS"
    else:
        return "NA"

# Load the data
data = pd.read_excel('Yazaki.xlsx', engine='openpyxl')
data['Capacity'].replace('NULL', 0, inplace=True)
data['Usage'].replace('NULL', 0, inplace=True)

# Prompt the user for country input
country_input = 'Mexico'

# Filter the data based on the user's input
if country_input and country_input in data['CountryName'].unique():
    data = data[data['CountryName'] == country_input]

# Prompt the user for preferred logistics input
logistics_input = 'road'
# Filter the data based on the user's logistics input
if logistics_input:
    if logistics_input == "road":
        data = data[data['PreferredLogistics'].isin(["road", "road/plane"])]
    elif logistics_input == "plane":
        data = data[data['PreferredLogistics'].isin(["plane", "road/plane"])]
    elif logistics_input in data['PreferredLogistics'].unique():
        data = data[data['PreferredLogistics'] == logistics_input]


# Calculate the difference
data['Difference'] = data['Capacity'] - data['Usage']

# Sort the data based on the numeric portion of 'PlantName'
data['PlantNumber'] = data['PlantName'].str.extract('(\d+)').astype(int)
data = data.sort_values('PlantNumber')

# Pivot the table to get the data in matrix form
pivot_data = data.pivot_table(index='PlantName', values=['Difference'], aggfunc='sum').T

# Create a heatmap
fig = go.Figure(data=go.Heatmap(
    z=pivot_data.values,
    x=pivot_data.columns,
    y=pivot_data.index,
    colorscale='Viridis',
    hoverongaps=False,
    hoverinfo='z',
    showscale=True))

# Add annotations based on the stock status
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

fig.update_layout(title='Heatmap Plant Availability',
                  xaxis_title='Plant Name',
                  yaxis_title='Available Capacity')

fig.show()

fig = px.imshow(
                #labels=dict(x=columns[0], y=columns[4], color="Capacity per Plant"),
                data
                )
tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    st.plotly_chart(fig, theme="streamlit")
with tab2:
    st.plotly_chart(fig, theme=None)





#hm.get_chart_1()
#hm.get_chart_2()
#hm.get_chart_3(df)
#hmp.get_pdchart1()
#hmp.get_pdchart2()