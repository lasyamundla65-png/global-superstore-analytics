import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Global Superstore Analytics",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# THEME — DARK MODE ONLY
# ============================================================

BG = "#272727"
SURFACE = "#333333"
SURFACE_2 = "#3A3A3A"
TEXT = "#FFFFFF"
MUTED = "#A9A9B2"
BORDER = "#494949"
GRID = "#555555"
PURPLE = "#9274F6"
PURPLE_SOFT = "#6D57B8"
GREEN = "#A8E95A"
YELLOW = "#F4C95D"
BLUE = "#8AB4F8"
TEAL = "#37A6A0"
PLOT_BG = "#333333"
dark = True

st.markdown(
    f"""
    <style>
    :root {{
        --ui-surface: {SURFACE};
        --ui-surface-2: {SURFACE_2};
        --ui-text: {TEXT};
        --ui-muted: {MUTED};
        --ui-border: {BORDER};
        --ui-purple: {PURPLE};
    }}

    /* Filter popover — matches the permanent dark dashboard theme */
    div[data-testid="stPopover"] > div[role="dialog"] {{
        background: {SURFACE} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 22px !important;
        color: {TEXT} !important;
        box-shadow: 0 18px 45px rgba(40, 30, 70, 0.16) !important;
    }}

    div[data-testid="stPopover"] [data-testid="stPopoverBody"] {{
        background: {SURFACE} !important;
        color: {TEXT} !important;
        border-radius: 22px !important;
    }}

    div[data-testid="stPopover"] label,
    div[data-testid="stPopover"] p,
    div[data-testid="stPopover"] span {{
        color: {TEXT} !important;
    }}

    div[data-testid="stPopover"] [data-baseweb="select"] > div {{
        background: {SURFACE_2} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important;
        color: {TEXT} !important;
        min-height: 42px !important;
    }}

    div[data-testid="stPopover"] [data-baseweb="select"] input {{
        color: {TEXT} !important;
    }}

    div[data-testid="stPopover"] [data-baseweb="tag"] {{
        background: rgba(139,111,245,0.13) !important;
        color: {PURPLE} !important;
        border: 1px solid rgba(139,111,245,0.25) !important;
        border-radius: 999px !important;
    }}

    div[data-testid="stPopover"] [data-baseweb="tag"] span {{
        color: {PURPLE} !important;
    }}

    div[data-testid="stPopover"] [data-baseweb="menu"] {{
        background: {SURFACE} !important;
        border: 1px solid {BORDER} !important;
    }}

    div[data-testid="stPopover"] [role="option"] {{
        color: {TEXT} !important;
        background: {SURFACE} !important;
    }}

    div[data-testid="stPopover"] [role="option"]:hover {{
        background: rgba(139,111,245,0.10) !important;
    }}

    div[data-testid="stPopover"] .stButton > button {{
        border-radius: 999px !important;
    }}

    div[data-testid="stPopover"] .stForm {{
        border: 0 !important;
        padding: 0 !important;
    }}

    div[data-testid="stPopover"] button[kind="primaryFormSubmit"] {{
        background: {PURPLE} !important;
        border-color: {PURPLE} !important;
        color: #FFFFFF !important;
    }}

    div[data-testid="stPopover"] button[kind="primaryFormSubmit"]:hover {{
        background: {PURPLE_SOFT} !important;
        border-color: {PURPLE_SOFT} !important;
        color: #FFFFFF !important;
    }}

    div[data-testid="stPopover"] [data-baseweb="input"] {{
        background: {SURFACE_2} !important;
        color: {TEXT} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {BG};
        color: {TEXT};
    }}

    .block-container {{
        max-width: 1500px;
        padding: 1.1rem 2rem 3rem 2rem;
    }}

    header[data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stSidebar"] {{
        display: none;
    }}

    /* Main typography */
    h1, h2, h3, h4, p, label {{
        color: {TEXT} !important;
    }}

    .brand {{
        font-size: 1.35rem;
        font-weight: 750;
        letter-spacing: -0.02em;
        color: {TEXT};
        padding-top: 0.45rem;
    }}

    .brand-mark {{
        color: {PURPLE};
        font-weight: 900;
        margin-right: 0.35rem;
    }}

    .hero-title {{
        font-size: 2rem;
        line-height: 1.05;
        font-weight: 750;
        letter-spacing: -0.04em;
        margin: 0.2rem 0 0.25rem 0;
        color: {TEXT};
    }}

    .hero-subtitle {{
        color: {MUTED};
        font-size: 0.92rem;
        margin-bottom: 0.2rem;
    }}

    .section-title {{
        font-size: 1.08rem;
        font-weight: 700;
        color: {TEXT};
        margin: 0.3rem 0 0.8rem 0;
    }}

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {{
        border-radius: 999px !important;
        border: 1px solid {BORDER} !important;
        background: {SURFACE} !important;
        color: {TEXT} !important;
        min-height: 2.35rem;
        font-weight: 650;
        box-shadow: none !important;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        border-color: {PURPLE} !important;
        color: {PURPLE} !important;
    }}

    /* Tabs */
    button[data-baseweb="tab"] {{
        color: {MUTED} !important;
        font-weight: 650 !important;
        font-size: 0.91rem !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {PURPLE} !important;
    }}

    div[data-baseweb="tab-highlight"] {{
        background: {PURPLE} !important;
    }}

    /* Metric cards */
    .metric-card {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 20px;
        padding: 1rem 1.1rem;
        min-height: 128px;
        box-shadow: 0 8px 25px rgba(60, 45, 100, 0.05);
    }}

    .metric-label {{
        color: {MUTED};
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 0.65rem;
    }}

    .metric-value {{
        color: {TEXT};
        font-size: 1.75rem;
        font-weight: 760;
        letter-spacing: -0.04em;
    }}

    .metric-foot {{
        color: {MUTED};
        font-size: 0.76rem;
        margin-top: 0.35rem;
    }}

    /* Generic cards */
    .dashboard-card {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 22px;
        padding: 0.85rem;
        box-shadow: 0 8px 25px rgba(60, 45, 100, 0.05);
        margin-bottom: 1rem;
    }}

    .insight-card {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 20px;
        padding: 1.05rem;
        min-height: 132px;
        box-shadow: 0 8px 25px rgba(60, 45, 100, 0.05);
    }}

    .insight-kicker {{
        color: {MUTED};
        font-size: 0.78rem;
        font-weight: 650;
        margin-bottom: 0.4rem;
    }}

    .insight-main {{
        color: {TEXT};
        font-size: 1.15rem;
        font-weight: 750;
    }}

    .insight-sub {{
        color: {MUTED};
        font-size: 0.78rem;
        margin-top: 0.35rem;
    }}

    .active-pill {{
        display: inline-block;
        background: rgba(139, 111, 245, 0.12);
        color: {PURPLE};
        border: 1px solid rgba(139, 111, 245, 0.25);
        border-radius: 999px;
        padding: 0.32rem 0.65rem;
        font-size: 0.74rem;
        font-weight: 700;
        margin: 0.15rem 0.2rem 0.15rem 0;
    }}

    .filter-help {{
        color: {MUTED};
        font-size: 0.78rem;
        line-height: 1.45;
        margin-bottom: 0.4rem;
    }}

    /* Filter popover */
    div[data-testid="stPopover"] button {{
        border-radius: 999px !important;
    }}

    /* Plotly containers */
    div[data-testid="stPlotlyChart"] {{
        border-radius: 16px;
        overflow: hidden;
    }}

    /* Download */
    .download-note {{
        color: {MUTED};
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
    }}

    /* Reduce Streamlit's default vertical gaps */
    div[data-testid="stVerticalBlock"] > div {{
        gap: 0.35rem;
    }}

    @media (max-width: 900px) {{
        .block-container {{
            padding: 0.8rem 0.8rem 2rem 0.8rem;
        }}

        .hero-title {{
            font-size: 1.55rem;
        }}

        .metric-value {{
            font-size: 1.35rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv("final_dataset.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
    return df


df = load_data()

# ============================================================
# REQUIRED COLUMNS CHECK
# ============================================================

required_columns = [
    "Order ID",
    "Customer ID",
    "Order Date",
    "Ship Date",
    "Year",
    "Market",
    "Region",
    "Country",
    "Category",
    "Sub-Category",
    "Segment",
    "Ship Mode",
    "Sales",
    "Quantity",
    "Discount",
    "Profit",
    "Shipping Cost",
    "Shipping Days",
    "Profit Margin (%)",
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error("Some required columns are missing from final_dataset.csv.")
    st.write(missing_columns)
    st.stop()

# ============================================================
# FILTER STATE
# ============================================================

years = sorted(df["Year"].dropna().unique().tolist())
markets = sorted(df["Market"].dropna().unique().tolist())
regions = sorted(df["Region"].dropna().unique().tolist())
categories = sorted(df["Category"].dropna().unique().tolist())
subcategories = sorted(df["Sub-Category"].dropna().unique().tolist())
segments = sorted(df["Segment"].dropna().unique().tolist())
ship_modes = sorted(df["Ship Mode"].dropna().unique().tolist())

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

if "filters" not in st.session_state:
    st.session_state.filters = {
        "years": years,
        "markets": markets,
        "regions": regions,
        "categories": categories,
        "subcategories": subcategories,
        "segments": segments,
        "ship_modes": ship_modes,
        "start_date": min_date,
        "end_date": max_date,
    }

# ============================================================
# HEADER
# ============================================================

header_left, header_mid, header_right = st.columns(
    [2.7, 3.2, 2.2],
    vertical_alignment="center",
)

with header_left:
    st.markdown(
        '<div class="brand"><span class="brand-mark">▥</span>Superstore</div>',
        unsafe_allow_html=True,
    )

with header_mid:
    st.markdown(
        '<div style="text-align:center; color:'
        + TEXT
        + '; font-size:0.86rem; font-weight:650;">Global Business Analytics</div>',
        unsafe_allow_html=True,
    )

with header_right:
    h1, h3 = st.columns([1.5, 1.1], gap="small")

    with h1:
        # Native popover: filters stay hidden until the user clicks the button.
        with st.popover("⚙ Filters", width="stretch"):
            st.markdown(
                '<div class="filter-help">'
                '<b>Dashboard Filters</b><br>'
                'Choose the dimensions you want to analyze. Leave a field empty to include everything.'
                '</div>',
                unsafe_allow_html=True,
            )

            current = st.session_state.filters

            with st.form("filter_form"):
                left_filters, right_filters = st.columns(2, gap="large")

                with left_filters:
                    f_years = st.multiselect(
                        "Year",
                        years,
                        default=[] if set(current["years"]) == set(years) else current["years"],
                        placeholder="All years",
                    )
                    f_markets = st.multiselect(
                        "Market",
                        markets,
                        default=[] if set(current["markets"]) == set(markets) else current["markets"],
                        placeholder="All markets",
                    )
                    f_regions = st.multiselect(
                        "Region",
                        regions,
                        default=[] if set(current["regions"]) == set(regions) else current["regions"],
                        placeholder="All regions",
                    )
                    f_categories = st.multiselect(
                        "Category",
                        categories,
                        default=[] if set(current["categories"]) == set(categories) else current["categories"],
                        placeholder="All categories",
                    )

                with right_filters:
                    f_subcategories = st.multiselect(
                        "Sub-Category",
                        subcategories,
                        default=[] if set(current["subcategories"]) == set(subcategories) else current["subcategories"],
                        placeholder="All sub-categories",
                    )
                    f_segments = st.multiselect(
                        "Customer Segment",
                        segments,
                        default=[] if set(current["segments"]) == set(segments) else current["segments"],
                        placeholder="All segments",
                    )
                    f_ship_modes = st.multiselect(
                        "Ship Mode",
                        ship_modes,
                        default=[] if set(current["ship_modes"]) == set(ship_modes) else current["ship_modes"],
                        placeholder="All shipping modes",
                    )
                    f_dates = st.date_input(
                        "Order Date Range",
                        value=(current["start_date"], current["end_date"]),
                        min_value=min_date,
                        max_value=max_date,
                    )

                st.write("")
                apply_col, reset_col = st.columns(2, gap="small")

                with apply_col:
                    apply_filters = st.form_submit_button(
                        "Apply Filters",
                        width="stretch",
                        type="primary",
                    )

                with reset_col:
                    reset_filters = st.form_submit_button(
                        "Reset All",
                        width="stretch",
                    )

                if apply_filters:
                    if isinstance(f_dates, (tuple, list)) and len(f_dates) == 2:
                        start_date, end_date = f_dates
                    else:
                        start_date, end_date = min_date, max_date

                    st.session_state.filters = {
                        "years": f_years if f_years else years,
                        "markets": f_markets if f_markets else markets,
                        "regions": f_regions if f_regions else regions,
                        "categories": f_categories if f_categories else categories,
                        "subcategories": f_subcategories if f_subcategories else subcategories,
                        "segments": f_segments if f_segments else segments,
                        "ship_modes": f_ship_modes if f_ship_modes else ship_modes,
                        "start_date": start_date,
                        "end_date": end_date,
                    }
                    st.rerun()

                if reset_filters:
                    st.session_state.filters = {
                        "years": years,
                        "markets": markets,
                        "regions": regions,
                        "categories": categories,
                        "subcategories": subcategories,
                        "segments": segments,
                        "ship_modes": ship_modes,
                        "start_date": min_date,
                        "end_date": max_date,
                    }
                    st.rerun()

    with h3:
        st.markdown(
            f'<div style="background:{SURFACE};border:1px solid {BORDER};'
            f'border-radius:999px;padding:0.55rem 0.75rem;text-align:center;'
            f'color:{MUTED};font-size:0.76rem;">{max_date.strftime("%b %Y")}</div>',
            unsafe_allow_html=True,
        )

# ============================================================
# ACTIVE FILTER COUNT
# ============================================================

flt = st.session_state.filters

active_filter_count = 0
active_filter_count += int(set(flt["years"]) != set(years))
active_filter_count += int(set(flt["markets"]) != set(markets))
active_filter_count += int(set(flt["regions"]) != set(regions))
active_filter_count += int(set(flt["categories"]) != set(categories))
active_filter_count += int(set(flt["subcategories"]) != set(subcategories))
active_filter_count += int(set(flt["segments"]) != set(segments))
active_filter_count += int(set(flt["ship_modes"]) != set(ship_modes))
active_filter_count += int(
    flt["start_date"] != min_date or flt["end_date"] != max_date
)

if active_filter_count:
    st.markdown(
        f'<span class="active-pill">⚙ {active_filter_count} filter{"s" if active_filter_count != 1 else ""} active</span>',
        unsafe_allow_html=True,
    )

# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    (df["Year"].isin(flt["years"]))
    & (df["Market"].isin(flt["markets"]))
    & (df["Region"].isin(flt["regions"]))
    & (df["Category"].isin(flt["categories"]))
    & (df["Sub-Category"].isin(flt["subcategories"]))
    & (df["Segment"].isin(flt["segments"]))
    & (df["Ship Mode"].isin(flt["ship_modes"]))
    & (df["Order Date"].dt.date >= flt["start_date"])
    & (df["Order Date"].dt.date <= flt["end_date"])
].copy()

if filtered_df.empty:
    st.warning("No data matches the selected filters. Open Filters and choose a broader selection.")
    st.stop()

# ============================================================
# HERO
# ============================================================

st.markdown('<div class="hero-title">Good morning, Analyst! 👋</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">A clean view of global sales, profitability, customers and operational performance.</div>',
    unsafe_allow_html=True,
)

# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0
average_order_value = (total_sales / total_orders) if total_orders else 0
total_quantity = filtered_df["Quantity"].sum()

# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4 = st.columns(4, gap="medium")

kpis = [
    ("Total Sales", f"${total_sales:,.0f}", "Revenue in selected period"),
    ("Total Profit", f"${total_profit:,.0f}", "Net profit in selected data"),
    ("Orders", f"{total_orders:,}", "Unique orders"),
    ("Customers", f"{total_customers:,}", "Unique customers"),
]

for col, (label, value, foot) in zip([k1, k2, k3, k4], kpis):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-foot">{foot}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")

k5, k6, k7, k8 = st.columns(4, gap="medium")

secondary_kpis = [
    ("Profit Margin", f"{profit_margin:.2f}%", "Profit ÷ Sales"),
    ("Average Order", f"${average_order_value:,.0f}", "Sales per order"),
    ("Units Sold", f"{total_quantity:,}", "Total quantity"),
    ("Shipping Days", f"{filtered_df['Shipping Days'].mean():.1f}", "Average shipping time"),
]

for col, (label, value, foot) in zip([k5, k6, k7, k8], secondary_kpis):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-foot">{foot}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")

# ============================================================
# DATA PREPARATION
# ============================================================

monthly_data = (
    filtered_df.groupby(pd.Grouper(key="Order Date", freq="MS"))
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .reset_index()
)

category_sales = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)

category_performance = (
    filtered_df.groupby("Category")[["Sales", "Profit"]]
    .sum()
    .reset_index()
)

shipping_data = filtered_df["Ship Mode"].value_counts().reset_index()
shipping_data.columns = ["Ship Mode", "Orders"]

segment_sales = (
    filtered_df.groupby("Segment")["Sales"]
    .sum()
    .reset_index()
)

# ============================================================
# PLOT HELPERS
# ============================================================

def polish_fig(fig, height=420, title=None):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        title=title,
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT, family="Inter, Arial, sans-serif"),
        margin=dict(l=35, r=25, t=60, b=35),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT),
        ),
        hoverlabel=dict(
            bgcolor=SURFACE,
            font_color=TEXT,
        ),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
    )
    return fig


# ============================================================
# NAVIGATION TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Overview", "Sales", "Profitability", "Distribution", "Global", "Insights"]
)

# ============================================================
# OVERVIEW
# ============================================================

with tab1:
    st.markdown('<div class="section-title">Business Overview</div>', unsafe_allow_html=True)

    fig_overview = go.Figure()
    fig_overview.add_trace(
        go.Scatter(
            x=monthly_data["Order Date"],
            y=monthly_data["Sales"],
            mode="lines+markers",
            name="Sales",
            line=dict(color=PURPLE, width=3),
            marker=dict(size=6, color=PURPLE),
        )
    )
    fig_overview.add_trace(
        go.Scatter(
            x=monthly_data["Order Date"],
            y=monthly_data["Profit"],
            mode="lines",
            name="Profit",
            line=dict(color=YELLOW, width=3),
        )
    )
    polish_fig(fig_overview, height=450, title="Sales vs Profit Trend")
    st.plotly_chart(fig_overview, use_container_width=True)

    left, right = st.columns([1.45, 1], gap="medium")

    with left:
        fig_category = px.bar(
            category_sales,
            x="Category",
            y="Sales",
            text_auto=".2s",
            color_discrete_sequence=[PURPLE],
        )
        polish_fig(fig_category, height=400, title="Sales by Category")
        st.plotly_chart(fig_category, use_container_width=True)

    with right:
        fig_donut = px.pie(
            category_sales,
            names="Category",
            values="Sales",
            hole=0.58,
            color_discrete_sequence=[PURPLE, TEAL, GREEN],
        )
        fig_donut.update_traces(textposition="inside", textinfo="percent")
        polish_fig(fig_donut, height=400, title="Category Mix")
        fig_donut.update_layout(showlegend=True)
        st.plotly_chart(fig_donut, use_container_width=True)

# ============================================================
# SALES
# ============================================================

with tab2:
    st.markdown('<div class="section-title">Sales Performance</div>', unsafe_allow_html=True)

    left, right = st.columns([1.5, 1], gap="medium")

    with left:
        fig_sales = px.line(
            monthly_data,
            x="Order Date",
            y="Sales",
            markers=True,
        )
        fig_sales.update_traces(
            line=dict(color=PURPLE, width=3),
            marker=dict(color=PURPLE, size=6),
        )
        polish_fig(fig_sales, height=440, title="Monthly Sales Trend")
        st.plotly_chart(fig_sales, use_container_width=True)

    with right:
        fig_category_sales = px.bar(
            category_sales,
            x="Sales",
            y="Category",
            orientation="h",
            text_auto=".2s",
            color_discrete_sequence=[PURPLE],
        )
        polish_fig(fig_category_sales, height=440, title="Category Sales Ranking")
        fig_category_sales.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_category_sales, use_container_width=True)

    fig_grouped = px.bar(
        category_performance,
        x="Category",
        y=["Sales", "Profit"],
        barmode="group",
        color_discrete_sequence=[PURPLE, YELLOW],
    )
    polish_fig(fig_grouped, height=430, title="Sales vs Profit by Category")
    st.plotly_chart(fig_grouped, use_container_width=True)

# ============================================================
# PROFITABILITY
# ============================================================

with tab3:
    st.markdown('<div class="section-title">Profitability Analysis</div>', unsafe_allow_html=True)

    left, right = st.columns([1.5, 1], gap="medium")

    with left:
        fig_scatter = px.scatter(
            filtered_df,
            x="Discount",
            y="Profit",
            opacity=0.45,
            hover_data=["Category", "Sub-Category", "Country", "Sales"],
        )
        fig_scatter.update_traces(marker=dict(color=PURPLE, size=6))
        fig_scatter.add_hline(y=0, line_dash="dash", line_color=MUTED)
        polish_fig(fig_scatter, height=440, title="Discount vs Profit")
        st.plotly_chart(fig_scatter, use_container_width=True)

    with right:
        profit_category = (
            filtered_df.groupby("Category")["Profit"]
            .sum()
            .reset_index()
            .sort_values("Profit", ascending=False)
        )

        fig_profit = px.bar(
            profit_category,
            x="Category",
            y="Profit",
            text_auto=".2s",
            color_discrete_sequence=[GREEN],
        )
        polish_fig(fig_profit, height=440, title="Profit by Category")
        st.plotly_chart(fig_profit, use_container_width=True)

    area_data = monthly_data.copy()
    area_data["Cumulative Sales"] = area_data["Sales"].cumsum()

    fig_area = px.area(
        area_data,
        x="Order Date",
        y="Cumulative Sales",
    )
    fig_area.update_traces(line_color=PURPLE, fillcolor="rgba(139,111,245,0.22)")
    polish_fig(fig_area, height=430, title="Cumulative Sales Over Time")
    st.plotly_chart(fig_area, use_container_width=True)

# ============================================================
# DISTRIBUTION
# ============================================================

with tab4:
    st.markdown('<div class="section-title">Distribution & Correlation</div>', unsafe_allow_html=True)

    left, right = st.columns(2, gap="medium")

    with left:
        fig_box = px.box(
            filtered_df,
            x="Category",
            y="Profit",
            points="outliers",
            color_discrete_sequence=[PURPLE],
        )
        polish_fig(fig_box, height=430, title="Profit Distribution by Category")
        st.plotly_chart(fig_box, use_container_width=True)

    with right:
        fig_hist = px.histogram(
            filtered_df,
            x="Sales",
            nbins=50,
            color_discrete_sequence=[PURPLE],
        )
        polish_fig(fig_hist, height=430, title="Sales Distribution")
        st.plotly_chart(fig_hist, use_container_width=True)

    numeric_columns = [
        "Sales",
        "Quantity",
        "Discount",
        "Profit",
        "Shipping Cost",
        "Shipping Days",
        "Profit Margin (%)",
    ]

    correlation = filtered_df[numeric_columns].corr()

    fig_heatmap = px.imshow(
        correlation,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale=[
            "#5B46B5",
            "#A99BEF",
            "#F4F2FA",
            "#F1C75B",
            "#A8E95A",
        ],
        zmin=-1,
        zmax=1,
    )
    polish_fig(fig_heatmap, height=520, title="Correlation Heatmap")
    st.plotly_chart(fig_heatmap, use_container_width=True)

# ============================================================
# GLOBAL
# ============================================================

with tab5:
    st.markdown('<div class="section-title">Global & Customer Analysis</div>', unsafe_allow_html=True)

    country_sales = (
        filtered_df.groupby("Country")["Sales"]
        .sum()
        .reset_index()
    )

    fig_map = px.choropleth(
        country_sales,
        locations="Country",
        locationmode="country names",
        color="Sales",
        hover_name="Country",
        color_continuous_scale=[
            "#EEE9FF",
            "#C9BCFF",
            "#A894FA",
            "#8B6FF5",
            "#6248D8",
        ],
    )
    fig_map.update_layout(
        template="plotly_dark",
        height=560,
        paper_bgcolor=PLOT_BG,
        geo=dict(bgcolor=PLOT_BG),
        margin=dict(l=0, r=0, t=50, b=0),
        font=dict(color=TEXT),
        title="Global Sales by Country",
    )
    st.plotly_chart(fig_map, use_container_width=True)

    left, right = st.columns(2, gap="medium")

    with left:
        fig_shipping = px.pie(
            shipping_data,
            names="Ship Mode",
            values="Orders",
            hole=0.58,
            color_discrete_sequence=[PURPLE, TEAL, GREEN, YELLOW],
        )
        polish_fig(fig_shipping, height=420, title="Orders by Shipping Mode")
        st.plotly_chart(fig_shipping, use_container_width=True)

    with right:
        fig_segment = px.pie(
            segment_sales,
            names="Segment",
            values="Sales",
            hole=0.58,
            color_discrete_sequence=[PURPLE, BLUE, GREEN],
        )
        polish_fig(fig_segment, height=420, title="Sales by Customer Segment")
        st.plotly_chart(fig_segment, use_container_width=True)

# ============================================================
# INSIGHTS
# ============================================================

with tab6:
    st.markdown('<div class="section-title">Business Insights</div>', unsafe_allow_html=True)

    top_category_row = category_sales.iloc[0]
    top_category = top_category_row["Category"]
    top_category_sales = top_category_row["Sales"]

    profit_by_category = (
        filtered_df.groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )
    top_profit_category = profit_by_category.index[0]
    top_profit_value = profit_by_category.iloc[0]

    top_country_row = country_sales.sort_values("Sales", ascending=False).iloc[0]
    top_country = top_country_row["Country"]
    top_country_sales = top_country_row["Sales"]

    top_segment = (
        segment_sales.sort_values("Sales", ascending=False).iloc[0]["Segment"]
    )

    subcategory_profit = (
        filtered_df.groupby("Sub-Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )
    top_subcategory = subcategory_profit.index[0]
    top_subcategory_profit = subcategory_profit.iloc[0]

    top_shipping = shipping_data.sort_values("Orders", ascending=False).iloc[0]
    top_shipping_mode = top_shipping["Ship Mode"]
    top_shipping_orders = top_shipping["Orders"]

    if not monthly_data.empty:
        best_month_row = monthly_data.sort_values("Sales", ascending=False).iloc[0]
        best_month = best_month_row["Order Date"]
        best_month_sales = best_month_row["Sales"]
    else:
        best_month = None
        best_month_sales = 0

    loss_data = filtered_df[filtered_df["Profit"] < 0]
    loss_transactions = len(loss_data)
    total_loss = abs(loss_data["Profit"].sum())

    i1, i2, i3 = st.columns(3, gap="medium")

    insight_cards = [
        ("🏆 Top Sales Category", top_category, f"${top_category_sales:,.0f} sales"),
        ("💰 Top Profit Category", top_profit_category, f"${top_profit_value:,.0f} profit"),
        ("🌍 Top Country", top_country, f"${top_country_sales:,.0f} sales"),
        ("👥 Top Customer Segment", top_segment, "Highest sales contribution"),
        ("📦 Most Profitable Sub-Category", top_subcategory, f"${top_subcategory_profit:,.0f} profit"),
        ("🚚 Most Used Shipping Mode", top_shipping_mode, f"{top_shipping_orders:,} orders"),
    ]

    for col, (kicker, main, sub) in zip(
        [i1, i2, i3],
        insight_cards[:3],
    ):
        with col:
            st.markdown(
                f"""
                <div class="insight-card">
                    <div class="insight-kicker">{kicker}</div>
                    <div class="insight-main">{main}</div>
                    <div class="insight-sub">{sub}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    i1, i2, i3 = st.columns(3, gap="medium")

    for col, (kicker, main, sub) in zip(
        [i1, i2, i3],
        insight_cards[3:],
    ):
        with col:
            st.markdown(
                f"""
                <div class="insight-card">
                    <div class="insight-kicker">{kicker}</div>
                    <div class="insight-main">{main}</div>
                    <div class="insight-sub">{sub}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    st.markdown('<div class="section-title">Performance Summary</div>', unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3, gap="medium")

    with p1:
        month_text = best_month.strftime("%B %Y") if best_month is not None else "N/A"
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-kicker">📅 Best Sales Month</div>
                <div class="insight-main">{month_text}</div>
                <div class="insight-sub">Sales: ${best_month_sales:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with p2:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-kicker">⚠️ Loss-Making Transactions</div>
                <div class="insight-main">{loss_transactions:,}</div>
                <div class="insight-sub">Total loss: ${total_loss:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with p3:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-kicker">📦 Total Quantity Sold</div>
                <div class="insight-main">{total_quantity:,}</div>
                <div class="insight-sub">Units across filtered orders</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============================================================
# EXPORT
# ============================================================

st.divider()

st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="download-note">Download exactly the data currently represented by your active filters.</div>',
    unsafe_allow_html=True,
)

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_superstore_data.csv",
    mime="text/csv",
    width="stretch",
)

st.markdown(
    f'<div style="text-align:center;color:{MUTED};font-size:0.75rem;margin-top:1.5rem;">'
    'Global Superstore Analytics • Data Science Project'
    '</div>',
    unsafe_allow_html=True,
)
