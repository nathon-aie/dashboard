# Import packages
from dash import Dash, html, dcc
from pandas.api.types import CategoricalDtype
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv("Dataset/Smartphone_Usage_Productivity_Dataset_50000.csv")

bins = [0, 20, 30, 40, 50, 100]
labels = ["<20", "21-30", "31-40", "41-50", ">50"]
df["Age_Group"] = pd.cut(df["Age"], bins=bins, labels=labels)
cat_type = CategoricalDtype(categories=labels, ordered=True)
df["Age_Group"] = df["Age_Group"].astype(cat_type)

occupations = ["All"] + list(df["Occupation"].unique())
devices = ["All"] + list(df["Device_Type"].unique())

# Initialize the app
app = Dash()
app.title = "Smartphone Usage and Productivity Dashboard"

# App layout
app.layout = [
    html.Div(
        children="Smartphone Usage and Productivity Dashboard",
        style={"textAlign": "center", "fontSize": 24},
    ),
    dag.AgGrid(
        rowData=df.to_dict("records"),
        columnDefs=[{"field": i} for i in df.columns],
    ),
    dcc.Graph(
        figure=px.histogram(
            df,
            x="Age_Group",
            y="Daily_Phone_Hours",
            histfunc="avg",
            category_orders={"Age_Group": labels},
            title="Average Daily Phone Hours by Age Group",
            color="Age_Group",
        )
    ),
    dcc.Graph(
        figure=px.pie(
            df,
            names="Device_Type",
            title="Distribution of Device Types",
        )
    ),
]

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
