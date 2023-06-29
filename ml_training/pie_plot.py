from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv("geo_plot_data.csv")

app.layout = html.Div([
    html.H4('Customer segment distribution by Country'),
    dcc.Dropdown(
        id='Cluster_id:', 
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
    Input("Cluster_id:", "value"))

def generate_chart(cluster):
    df_filter = df[df.cluster == cluster]
    fig = fig = px.pie(df_filter, 
    values='Percentage', names='most_common_words', 
    hover_name='Country', hole=.3)
    fig.update_traces(textinfo='none')
    return fig

app.run_server(debug=True)