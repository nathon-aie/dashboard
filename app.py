# Import packages
from dash import Dash, html, dcc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
)

# Initialize the app
app = Dash()

# App layout
app.layout = [
    html.Div(children="My First App with Data"),
    dag.AgGrid(
        rowData=df.to_dict("records"), columnDefs=[{"field": i} for i in df.columns]
    ),
    dcc.Graph(figure=px.histogram(df, x="continent", y="lifeExp", histfunc="avg")),
]

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
