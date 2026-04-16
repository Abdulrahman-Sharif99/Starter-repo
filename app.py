import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

df = pd.read_csv("Output.csv")
df["date"] = pd.to_datetime(df["date"])
daily = df.groupby("date", as_index=False)["sales"].sum()
daily = daily.sort_values("date")

#Day price increased
price_increase_date = pd.Timestamp("2021-01-15").timestamp() * 1000

fig = px.line(daily, x="date", y="sales", title="Daily Sales of Pink Morsel")

fig.add_vline(x=price_increase_date, line_dash="dash", line_color="red", annotation_text="Price Increase (Jan 15,2021)", annotation_position="top left")

fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", font =dict(family="Arial",size=13), title_font_size=20, hovermode="x unified")

app = Dash(__name__)

app.layout = html.Div(
    style = { "fontfamily": "Arial", 
             "maxWidth": "1100px", 
             "margin": "0 auto",
             "padding": "20px"},
    children=[
        html.H1(
            "Pink Morsel Sales Display", 
            style={"textAlign": "center", "color": "#333"}),
        html.P(
            "This dashboard shows the daily sales of Pink Morsel. The red dashed line indicates when the price increase occurred on January 15, 2021.", 
            style={"textAlign": "center", "color": "#666", "fontSize": 14, "marginBottom": "30px"}),
        dcc.Graph(figure=fig, style={"height": "550px"})
    ]
)

if __name__ == "__main__":
    app.run(debug=True)