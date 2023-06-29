from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Customer segment distribution by Country'),
    dcc.Dropdown(
        id='Cluster: ID [customer type]', 
        options=[{'label': 'Cluster: 0 [Top clients]', 'value': 0},
                {'label': 'Cluster: 1 [Less recent clients]', 'value': 1},
                {'label': 'Cluster: 2 [Low monetary clients]', 'value': 2},
                {'label': 'Cluster: 3 [Recent but low F and M]]', 'value': 3},
                {'label': 'Cluster: 4 [Same as 3 but less recent]', 'value': 4},
                {'label': 'Cluster: 5 [Old clients]', 'value': 5},
                {'label': 'Cluster: 6 [Same as 3 but less recent]', 'value': 6},
                {'label': 'Cluster: 7 [Same as 2 but less frequent]', 'value': 7},
                {'label': 'Cluster: 8 [Old clients]', 'value': 8},
                {'label': 'Cluster: -1 [Outliers]', 'value': -1}],
        multi=False,
        value=0
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("Cluster: ID [customer type]", "value"))

def display_choropleth(cluster):
    df = pd.read_csv('geo_plot_data.csv')
    df_filter = df[df.cluster == cluster]
    fig = px.choropleth(
        df_filter, color='Percentage',
        hover_name='Country', locations="iso_alpha",
        projection="mercator", range_color=[0, 100])
    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

# 3D plot clusters
def plot_3d():
    plot_3d_data = pd.read_csv('rfm_scaled_plot.csv')
    d_plot = px.scatter_3d(plot_3d_data, x='Recency', y='Monetary', z='Frequency',
                color='cluster').update_traces(marker_size=5, marker_line=dict(width=2, color='#2F4F4F'))
    d_plot.show()


app.run_server(debug=True)