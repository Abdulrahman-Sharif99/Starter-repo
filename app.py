import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# ── palette ──────────────────────────────────────────────────────────────────
PINK      = "#E8547A"
PINK_DARK = "#C23860"
CREAM     = "#FFF8F5"
CHARCOAL  = "#1C1C2E"
MUTED     = "#6B6B8A"
CARD_BG   = "#FFFFFF"
BORDER    = "#F0E8EC"

app = Dash(__name__)

app.layout = html.Div(style={
    "minHeight": "100vh",
    "background": f"linear-gradient(135deg, {CREAM} 0%, #FCF0F5 100%)",
    "fontFamily": "'Georgia', 'Times New Roman', serif",
    "padding": "0",
    "margin": "0",
}, children=[

    # ── top banner ────────────────────────────────────────────────────────────
    html.Div(style={
        "background": f"linear-gradient(90deg, {CHARCOAL} 0%, #2E1B2E 100%)",
        "padding": "48px 60px 40px",
        "borderBottom": f"4px solid {PINK}",
    }, children=[
        html.Div("SOUL FOODS", style={
            "color": PINK,
            "fontSize": "11px",
            "letterSpacing": "4px",
            "fontFamily": "'Georgia', serif",
            "marginBottom": "10px",
            "opacity": "0.85",
        }),
        html.H1("Pink Morsel Sales", style={
            "color": CREAM,
            "fontSize": "clamp(32px, 5vw, 52px)",
            "margin": "0 0 8px 0",
            "fontWeight": "normal",
            "letterSpacing": "-1px",
            "lineHeight": "1.1",
        }),
        html.P("Daily revenue tracker · January 2021 price increase analysis", style={
            "color": MUTED,
            "fontSize": "15px",
            "margin": "0",
            "fontFamily": "'Georgia', serif",
            "fontStyle": "italic",
        }),
    ]),

    # ── body ──────────────────────────────────────────────────────────────────
    html.Div(style={"padding": "40px 60px 60px", "maxWidth": "1300px", "margin": "0 auto"}, children=[

        # region filter card
        html.Div(style={
            "background": CARD_BG,
            "borderRadius": "12px",
            "padding": "24px 32px",
            "marginBottom": "28px",
            "border": f"1px solid {BORDER}",
            "boxShadow": "0 2px 20px rgba(232,84,122,0.07)",
            "display": "flex",
            "alignItems": "center",
            "gap": "24px",
            "flexWrap": "wrap",
        }, children=[
            html.Span("Filter by region", style={
                "color": MUTED,
                "fontSize": "12px",
                "letterSpacing": "2px",
                "textTransform": "uppercase",
                "fontFamily": "'Georgia', serif",
                "whiteSpace": "nowrap",
            }),
            dcc.RadioItems(
                id="region-filter",
                options=[
                    {"label": "All Regions", "value": "all"},
                    {"label": "North",       "value": "north"},
                    {"label": "East",        "value": "east"},
                    {"label": "South",       "value": "south"},
                    {"label": "West",        "value": "west"},
                ],
                value="all",
                inline=True,
                inputStyle={"marginRight": "6px", "accentColor": PINK},
                labelStyle={
                    "marginRight": "28px",
                    "fontSize": "14px",
                    "color": CHARCOAL,
                    "cursor": "pointer",
                    "fontFamily": "'Georgia', serif",
                },
            ),
        ]),

        # chart card
        html.Div(style={
            "background": CARD_BG,
            "borderRadius": "12px",
            "padding": "32px",
            "border": f"1px solid {BORDER}",
            "boxShadow": "0 2px 20px rgba(232,84,122,0.07)",
        }, children=[
            dcc.Graph(id="sales-chart", style={"height": "520px"},
                      config={"displayModeBar": False}),
        ]),

        # footer note
        html.P("The dashed line marks the Pink Morsel price increase on 15 January 2021.", style={
            "color": MUTED,
            "fontSize": "13px",
            "textAlign": "center",
            "marginTop": "20px",
            "fontStyle": "italic",
        }),
    ]),
])


# ── callback ─────────────────────────────────────────────────────────────────
@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(region):
    df = pd.read_csv("output.csv")
    df["date"] = pd.to_datetime(df["date"])

    if region != "all":
        df = df[df["region"] == region]

    daily = df.groupby("date", as_index=False)["sales"].sum().sort_values("date")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=daily["date"],
        y=daily["sales"],
        mode="lines",
        line=dict(color=PINK, width=2.5, shape="spline"),
        fill="tozeroy",
        fillcolor="rgba(232,84,122,0.08)",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>",
    ))

    price_ts = pd.Timestamp("2021-01-15").timestamp() * 1000

    fig.add_vline(
        x=price_ts,
        line_dash="dash",
        line_color=PINK_DARK,
        line_width=1.8,
        annotation_text="Price increase · Jan 15, 2021",
        annotation_position="top right",
        annotation_font=dict(size=12, color=PINK_DARK, family="Georgia, serif"),
    )

    region_label = region.title() if region != "all" else "All Regions"

    fig.update_layout(
        title=dict(
            text=f"Daily Sales — {region_label}",
            font=dict(size=18, color=CHARCOAL, family="Georgia, serif"),
            x=0,
            pad=dict(b=16),
        ),
        xaxis=dict(
            title="Date",
            title_font=dict(size=13, color=MUTED, family="Georgia, serif"),
            tickfont=dict(size=12, color=MUTED),
            showgrid=False,
            linecolor=BORDER,
            linewidth=1,
        ),
        yaxis=dict(
            title="Total Sales (AUD)",
            title_font=dict(size=13, color=MUTED, family="Georgia, serif"),
            tickfont=dict(size=12, color=MUTED),
            tickprefix="$",
            tickformat=",",
            gridcolor=BORDER,
            gridwidth=1,
            zeroline=False,
        ),
        plot_bgcolor=CARD_BG,
        paper_bgcolor=CARD_BG,
        margin=dict(l=10, r=10, t=50, b=10),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor=CHARCOAL,
            font=dict(color=CREAM, size=13, family="Georgia, serif"),
            bordercolor=PINK,
        ),
    )

    return fig


if __name__ == "__main__":
    app.run()