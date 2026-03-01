from dash import Dash, html, dcc, Input, Output
from pandas.api.types import CategoricalDtype
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

# 1. เตรียมข้อมูล (ตรวจสอบ Path ไฟล์ให้ถูกต้อง)
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
    {"label": "Cafeine Intake (cups)", "value": "Caffeine_Intake_Cups"},
    {"label": "Weekend Phone Hours", "value": "Weekend_Screen_Time_Hours"},
]

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(
            "Smartphone Usage Dashboard",
            style={"textAlign": "center", "marginBottom": "30px"},
        ),
        # ส่วนกลาง: แบ่ง Sidebar (ซ้าย) และ Graphs (ขวา)
        html.Div(
            [
                # --- Sidebar (ด้านซ้าย) ---
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    "เลือกกลุ่มข้อมูล (แกน X):", style={"fontWeight": "bold"}
                                ),
                                dcc.Dropdown(
                                    id="x-axis-select",
                                    options=x_options,
                                    value="Age_Group",
                                    clearable=False,
                                ),
                            ],
                            style={"marginBottom": "20px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "เลือกสถิติที่สนใจ (แกน Y):",
                                    style={"fontWeight": "bold"},
                                ),
                                dcc.Dropdown(
                                    id="y-axis-select",
                                    options=y_options,
                                    value="Daily_Phone_Hours",
                                    clearable=False,
                                ),
                            ]
                        ),
                    ],
                    style={
                        "width": "20%",
                        "padding": "20px",
                        "backgroundColor": "#f8f9fa",
                        "borderRadius": "10px",
                        "boxShadow": "2px 2px 5px rgba(0,0,0,0.1)",
                        "marginRight": "20px",
                        "height": "fit-content",
                    },
                ),
                # --- Content Area (ด้านขวา) ---
                html.Div(
                    [
                        html.Div(
                            [
                                # กราฟซ้าย (Bar Chart)
                                html.Div(
                                    [dcc.Graph(id="dynamic-graph")],
                                    style={"width": "50%"},
                                ),
                                # กราฟขวา (Pie Chart)
                                html.Div(
                                    [dcc.Graph(id="dynamic-pie-chart")],
                                    style={"width": "50%"},
                                ),
                            ],
                            style={"display": "flex"},
                        ),
                        html.Div(
                            [dcc.Graph(id="dynamic-box-plot")],
                            style={"marginTop": "20px"},
                        ),
                    ],
                    style={"width": "80%"},
                ),
            ],
            style={"display": "flex", "padding": "0 20px"},
        ),
        # ตารางข้อมูลด้านล่าง
        html.Div(
            [
                html.H3("Data Table", style={"marginTop": "40px"}),
                dag.AgGrid(
                    rowData=df.to_dict("records"),
                    columnDefs=[{"field": i} for i in df.columns],
                    dashGridOptions={"pagination": True},
                    style={"height": "400px"},
                ),
            ],
            style={"padding": "20px"},
        ),
    ]
)


# 3. แก้ไข Callback ให้ส่งค่าไปยัง 2 กราฟ
@app.callback(
    Output("dynamic-graph", "figure"),
    Output("dynamic-pie-chart", "figure"),
    Output("dynamic-box-plot", "figure"),
    Input("x-axis-select", "value"),
    Input("y-axis-select", "value"),
)
def update_graph(x_col, y_col):
    # กราฟที่ 1: Histogram (Bar)
    order = {"Age_Group": labels} if x_col == "Age_Group" else None
    fig_bar = px.histogram(
        df,
        x=x_col,
        y=y_col,
        histfunc="avg",
        category_orders=order,
        title=f"Average {y_col.replace('_', ' ')} by {x_col}",
        color=x_col,
    )
    fig_bar.update_layout(yaxis_title="Average Value", transition_duration=500)

    # กราฟที่ 2: Pie Chart
    pie_fig = px.pie(
        df,
        names=x_col,
        title=f"Distribution of {x_col}",
        hole=0.3,  # ทำเป็น Donut chart ให้ดูทันสมัย
    )
    pie_fig.update_layout(transition_duration=500)

    fig_box = px.box(
        df,
        x=x_col,
        y=y_col,
        color=x_col,
        category_orders=order,
        title=f"Distribution Range of {y_col.replace('_', ' ')} by {x_col}",
    )
    fig_box.update_layout(showlegend=False, transition_duration=500)

    return fig_bar, pie_fig, fig_box


if __name__ == "__main__":
    app.run(debug=True)
