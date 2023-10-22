import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
    
def get_stock_status(capacity, usage):
    if usage > capacity:
        return "OS"
    elif capacity > usage:
        return "IS"
    else:
        return "NA"

data = pd.read_excel('Yazaki.xlsx', engine='openpyxl')
data['Capacity'].replace('NULL', 0, inplace=True)
data['Usage'].replace('NULL', 0, inplace=True)

# Calculate the difference
data['Difference'] = data['Capacity'] - data['Usage']

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


for i in range(len(pivot_data.columns)):
    capacity = data[data['PlantName'] == pivot_data.columns[i]]['Capacity'].sum()
    usage = data[data['PlantName'] == pivot_data.columns[i]]['Usage'].sum()
    status = get_stock_status(capacity, usage)
    fig.add_annotation(go.layout.Annotation(text=status,
                                            x=pivot_data.columns[i],
                                            y=pivot_data.index[0],  # As we have only one row now (Difference)
                                            ax=0, ay=0,
                                            font=dict(color='white' if abs(pivot_data.values[0][i]) > (0.5 * abs(pivot_data.values).max()) else 'black',
                                                      size=10)))

#Plant Availability
fig.update_layout(title='Heatmap Plant Availability',
                  xaxis_title='Plant Name',
                  yaxis_title='Available Capacity')

fig.show()

