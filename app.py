from dash import Dash, html, dcc, Input, Output  # เพิ่ม Input, Output
from pandas.api.types import CategoricalDtype
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

# 1. เตรียมข้อมูล
df = pd.read_csv("Dataset/Smartphone_Usage_Productivity_Dataset_50000.csv")

bins = [0, 20, 30, 40, 50, 100]
labels = ["<20", "21-30", "31-40", "41-50", ">50"]
df["Age_Group"] = pd.cut(df["Age"], bins=bins, labels=labels)
cat_type = CategoricalDtype(categories=labels, ordered=True)
df["Age_Group"] = df["Age_Group"].astype(cat_type)

x_options = [
    {"label": "Age Group", "value": "Age_Group"},
    {"label": "Gender", "value": "Gender"},
    {"label": "Occupation", "value": "Occupation"},
]

y_options = [
    {"label": "Daily Phone Hours", "value": "Daily_Phone_Hours"},
    {"label": "Social Media Hours", "value": "Social_Media_Hours"},
    {"label": "Productivity Score", "value": "Work_Productivity_Score"},
    {"label": "Sleep Hours", "value": "Sleep_Hours"},
    {"label": "Stress Level", "value": "Stress_Level"},
]

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Smartphone Usage Dashboard", style={"textAlign": "center"}),
        # ส่วนของ Dropdown สำหรับเลือกข้อมูล
        html.Div(
            [
                html.Div(
                    [
                        html.Label("เลือกกลุ่มข้อมูล:"),
                        dcc.Dropdown(
                            id="x-axis-select", options=x_options, value="Age_Group"
                        ),
                    ],
                    style={
                        "width": "45%",
                        "display": "inline-block",
                        "padding": "10px",
                    },
                ),
                html.Div(
                    [
                        html.Label("เลือกสถิติที่สนใจ:"),
                        dcc.Dropdown(
                            id="y-axis-select",
                            options=y_options,
                            value="Daily_Phone_Hours",
                        ),
                    ],
                    style={
                        "width": "45%",
                        "display": "inline-block",
                        "padding": "10px",
                    },
                ),
            ],
            style={"textAlign": "center", "marginBottom": "20px"},
        ),
        # ส่วนแสดงกราฟ
        dcc.Graph(id="dynamic-graph"),
        dcc.Graph(
            figure=px.pie(
                df,
                names="Device_Type",
                title="Distribution of Device Types",
            ),
        ),
        dcc.Graph(
            figure=px.pie(
                df,
                names="Age_Group",
                title="Distribution of Age Groups",
            ),
        ),
        dcc.Graph(
            figure=px.pie(
                df,
                names="Occupation",
                title="Distribution of Occupations",
            ),
        ),
        # ตารางข้อมูล
        dag.AgGrid(
            rowData=df.to_dict("records"),
            columnDefs=[{"field": i} for i in df.columns],
        ),
    ]
)


# 3. สร้าง Callback เพื่ออัปเดตกราฟ
@app.callback(
    Output("dynamic-graph", "figure"),
    Input("x-axis-select", "value"),
    Input("y-axis-select", "value"),
)
def update_graph(x_col, y_col):
    # กำหนดเงื่อนไขการเรียงลำดับ (เฉพาะ Age_Group)
    order = {"Age_Group": labels} if x_col == "Age_Group" else None

    # สร้างกราฟ Histogram (ค่าเฉลี่ย)
    fig = px.histogram(
        df,
        x=x_col,
        y=y_col,
        histfunc="avg",
        category_orders=order,
        title=f"Average {y_col.replace('_', ' ')} by {x_col.replace('_', ' ')}",
        color=x_col,
    )

    fig.update_layout(yaxis_title="Average Value", transition_duration=500)
    return fig


if __name__ == "__main__":
    app.run(debug=True)
