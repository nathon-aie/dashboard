from dash import Dash, html, dcc, Input, Output  # เพิ่ม Input, Output
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

# 1. เตรียมข้อมูล
df = pd.read_csv("Dataset/Smartphone_Usage_Productivity_Dataset_50000.csv")

bins = [0, 20, 30, 40, 50, 100]
labels = ["<20", "21-30", "31-40", "41-50", ">50"]
df["Age_Group"] = pd.cut(df["Age"], bins=bins, labels=labels)

# จัดลำดับ Age_Group ให้เรียงถูกต้อง
from pandas.api.types import CategoricalDtype

cat_type = CategoricalDtype(categories=labels, ordered=True)
df["Age_Group"] = df["Age_Group"].astype(cat_type)

# รายชื่อคอลัมน์ที่ต้องการให้เลือกดูในกราฟ
available_indicators = [
    {"label": "Daily Phone Hours", "value": "Daily_Phone_Hours"},
    {"label": "Social Media Hours", "value": "Social_Media_Hours"},
    {"label": "Productivity Score", "value": "Work_Productivity_Score"},
]

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Smartphone Usage Dashboard", style={"textAlign": "center"}),
        # ส่วนของ Dropdown สำหรับเลือกข้อมูล
        html.Div(
            [
                html.Label("เลือกข้อมูลที่ต้องการแสดงในกราฟ:"),
                dcc.Dropdown(
                    id="crossfilter-column",
                    options=available_indicators,
                    value="Daily_Phone_Hours",  # ค่าเริ่มต้น
                ),
            ],
            style={"width": "40%", "margin": "20px auto"},
        ),
        # ส่วนแสดงกราฟ
        dcc.Graph(id="main-graph"),
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
        # ตารางข้อมูล
        dag.AgGrid(
            rowData=df.to_dict("records"),
            columnDefs=[{"field": i} for i in df.columns],
            dashGridOptions={"pagination": True},
        ),
    ]
)


# 3. สร้าง Callback เพื่ออัปเดตกราฟ
@app.callback(Output("main-graph", "figure"), Input("crossfilter-column", "value"))
def update_graph(column_name):
    # สร้างกราฟใหม่ทุกครั้งที่มีการเปลี่ยนค่าใน Dropdown
    fig = px.histogram(
        df,
        x="Age_Group",
        y=column_name,
        histfunc="avg",
        category_orders={"Age_Group": labels},
        title=f"Average {column_name.replace('_', ' ')} by Age Group",
        color="Age_Group",
    )

    # # ปรับแต่งความสวยงามเพิ่มเติม
    fig.update_layout(yaxis_title="Average Value")
    return fig


if __name__ == "__main__":
    app.run(debug=True)
