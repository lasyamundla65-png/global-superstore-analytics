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
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #0b0f14;
    color: #f5f7fa;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #151922;
    border-right: 1px solid #252c38;
}

/* Headings */

h1, h2, h3 {
    color: #ffffff !important;
}

/* Metrics */

div[data-testid="stMetric"] {
    background-color: #151b24;
    border: 1px solid #293342;
    border-radius: 14px;
    padding: 18px;
    min-height: 115px;
}

div[data-testid="stMetricLabel"] {
    color: #a5b1c2;
}

div[data-testid="stMetricValue"] {
    color: #ffffff;
    font-weight: 700;
}

/* Charts */

div[data-testid="stPlotlyChart"] {
    background-color: #11161e;
    border: 1px solid #242d39;
    border-radius: 14px;
    padding: 5px;
}

/* Insight cards */

.insight-card {
    background-color: #151b24;
    border: 1px solid #293342;
    border-radius: 14px;
    padding: 18px;
    min-height: 125px;
}

.insight-title {
    color: #8fa0b5;
    font-size: 14px;
    margin-bottom: 8px;
}

.insight-value {
    color: #ffffff;
    font-size: 21px;
    font-weight: 700;
}

.insight-sub {
    color: #728196;
    font-size: 13px;
    margin-top: 6px;
}

/* Tabs */

button[data-baseweb="tab"] {
    font-size: 15px;
    font-weight: 600;
}

/* Download */

.stDownloadButton button {
    width: 100%;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("final_dataset.csv")

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        errors="coerce"
    )

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
    "Profit Margin (%)"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error("Some required columns are missing.")

    st.write(missing_columns)

    st.stop()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

with st.sidebar:

    st.markdown("## 🔎 Dashboard Filters")

    st.caption(
        "Filter the dataset to explore different business scenarios."
    )

    st.divider()

    # --------------------------------------------------------
    # YEAR
    # --------------------------------------------------------

    years = sorted(
        df["Year"].dropna().unique().tolist()
    )

    selected_years = st.multiselect(
        "Year",
        years,
        default=years
    )

    # --------------------------------------------------------
    # MARKET
    # --------------------------------------------------------

    markets = sorted(
        df["Market"].dropna().unique().tolist()
    )

    selected_markets = st.multiselect(
        "Market",
        markets,
        default=markets
    )

    # --------------------------------------------------------
    # REGION
    # --------------------------------------------------------

    regions = sorted(
        df["Region"].dropna().unique().tolist()
    )

    selected_regions = st.multiselect(
        "Region",
        regions,
        default=regions
    )

    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    categories = sorted(
        df["Category"].dropna().unique().tolist()
    )

    selected_categories = st.multiselect(
        "Category",
        categories,
        default=categories
    )

    # --------------------------------------------------------
    # SUB CATEGORY
    # --------------------------------------------------------

    subcategories = sorted(
        df["Sub-Category"].dropna().unique().tolist()
    )

    selected_subcategories = st.multiselect(
        "Sub-Category",
        subcategories,
        default=subcategories
    )

    # --------------------------------------------------------
    # CUSTOMER SEGMENT
    # --------------------------------------------------------

    segments = sorted(
        df["Segment"].dropna().unique().tolist()
    )

    selected_segments = st.multiselect(
        "Customer Segment",
        segments,
        default=segments
    )

    # --------------------------------------------------------
    # SHIP MODE
    # --------------------------------------------------------

    ship_modes = sorted(
        df["Ship Mode"].dropna().unique().tolist()
    )

    selected_ship_modes = st.multiselect(
        "Ship Mode",
        ship_modes,
        default=ship_modes
    )

    # --------------------------------------------------------
    # DATE RANGE
    # --------------------------------------------------------

    min_date = df["Order Date"].min().date()
    max_date = df["Order Date"].max().date()

    selected_dates = st.date_input(
        "Order Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )


# ============================================================
# DATE RANGE SAFETY
# ============================================================

if isinstance(selected_dates, (tuple, list)):

    if len(selected_dates) == 2:

        start_date = selected_dates[0]
        end_date = selected_dates[1]

    else:

        start_date = min_date
        end_date = max_date

else:

    start_date = min_date
    end_date = max_date


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    (df["Year"].isin(selected_years)) &
    (df["Market"].isin(selected_markets)) &
    (df["Region"].isin(selected_regions)) &
    (df["Category"].isin(selected_categories)) &
    (df["Sub-Category"].isin(selected_subcategories)) &
    (df["Segment"].isin(selected_segments)) &
    (df["Ship Mode"].isin(selected_ship_modes)) &
    (df["Order Date"].dt.date >= start_date) &
    (df["Order Date"].dt.date <= end_date)
].copy()


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No data matches the selected filters. "
        "Please change your filters."
    )

    st.stop()


# ============================================================
# TITLE
# ============================================================

st.title("🌎 Global Superstore Analytics")

st.markdown(
    "Interactive analysis of global sales, profitability, "
    "customers, shipping and business performance."
)

st.divider()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order ID"].nunique()

total_customers = filtered_df["Customer ID"].nunique()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)

average_order_value = (
    total_sales / total_orders
    if total_orders != 0
    else 0
)

total_quantity = filtered_df["Quantity"].sum()


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📊 Business Performance")

# First row

k1, k2, k3 = st.columns(3)

with k1:
    st.metric(
        "💰 Total Sales",
        f"${total_sales:,.0f}"
    )

with k2:
    st.metric(
        "📈 Total Profit",
        f"${total_profit:,.0f}"
    )

with k3:
    st.metric(
        "📦 Total Orders",
        f"{total_orders:,}"
    )


# Second row

k4, k5, k6 = st.columns(3)

with k4:
    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )

with k5:
    st.metric(
        "📊 Profit Margin",
        f"{profit_margin:.2f}%"
    )

with k6:
    st.metric(
        "🧾 Average Order Value",
        f"${average_order_value:,.0f}"
    )


st.divider()


# ============================================================
# PREPARE MONTHLY DATA
# ============================================================

monthly_data = (
    filtered_df
    .groupby(
        pd.Grouper(
            key="Order Date",
            freq="MS"
        )
    )
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)


# ============================================================
# PREPARE CATEGORY DATA
# ============================================================

category_sales = (
    filtered_df
    .groupby("Category")["Sales"]
    .sum()
    .reset_index()
    .sort_values(
        "Sales",
        ascending=False
    )
)


category_performance = (
    filtered_df
    .groupby("Category")[["Sales", "Profit"]]
    .sum()
    .reset_index()
)


# ============================================================
# PREPARE SHIPPING DATA
# ============================================================

shipping_data = (
    filtered_df["Ship Mode"]
    .value_counts()
    .reset_index()
)

shipping_data.columns = [
    "Ship Mode",
    "Orders"
]


# ============================================================
# PREPARE SEGMENT DATA
# ============================================================

segment_sales = (
    filtered_df
    .groupby("Segment")["Sales"]
    .sum()
    .reset_index()
)


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Sales",
    "💰 Profitability",
    "📊 Distribution",
    "🌍 Global",
    "💡 Insights"
])


# ============================================================
# TAB 1 — SALES
# ============================================================

with tab1:

    st.subheader("📈 Sales Performance")

    # --------------------------------------------------------
    # LINE CHART
    # --------------------------------------------------------

    fig_sales = px.line(
        monthly_data,
        x="Order Date",
        y="Sales",
        markers=True
    )

    fig_sales.update_layout(
        title="Monthly Sales Trend",
        template="plotly_dark",
        height=430,
        margin=dict(
            l=30,
            r=20,
            t=60,
            b=30
        ),
        paper_bgcolor="#11161e",
        plot_bgcolor="#11161e",
        hovermode="x unified"
    )

    # --------------------------------------------------------
    # BAR CHART
    # --------------------------------------------------------

    fig_category = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        text_auto=".2s"
    )

    fig_category.update_layout(
        title="Sales by Product Category",
        template="plotly_dark",
        height=430,
        margin=dict(
            l=30,
            r=20,
            t=60,
            b=30
        ),
        paper_bgcolor="#11161e",
        plot_bgcolor="#11161e"
    )

    c1, c2 = st.columns(2)

    with c1:

        st.plotly_chart(
            fig_sales,
            use_container_width=True
        )

    with c2:

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    # --------------------------------------------------------
    # GROUPED BAR
    # --------------------------------------------------------

    fig_grouped = px.bar(
        category_performance,
        x="Category",
        y=["Sales", "Profit"],
        barmode="group"
    )

    fig_grouped.update_layout(
        title="Sales vs Profit by Category",
        template="plotly_dark",
        height=430,
        paper_bgcolor="#11161e",
        plot_bgcolor="#11161e"
    )

    st.plotly_chart(
        fig_grouped,
        use_container_width=True
    )


# ============================================================
# TAB 2 — PROFITABILITY
# ============================================================

with tab2:

    st.subheader("💰 Profitability Analysis")

    # --------------------------------------------------------
    # SCATTER
    # --------------------------------------------------------

    fig_scatter = px.scatter(
        filtered_df,
        x="Discount",
        y="Profit",
        opacity=0.45,
        hover_data=[
            "Category",
            "Sub-Category",
            "Country",
            "Sales"
        ]
    )

    fig_scatter.add_hline(
        y=0,
        line_dash="dash"
    )

    fig_scatter.update_layout(
        title="Discount vs Profit",
        template="plotly_dark",
        height=430,
        paper_bgcolor="#11161e",
        plot_bgcolor="#11161e"
    )

    # --------------------------------------------------------
    # PROFIT BY CATEGORY
    # --------------------------------------------------------

    profit_category = (
        filtered_df
        .groupby("Category")["Profit"]
        .sum()
        .reset_index()
        .sort_values(
            "Profit",
            ascending=False
        )
    )

    fig_profit = px.bar(
        profit_category,
        x="Category",
        y="Profit",
        text_auto=".2s"
    )

    fig_profit.update_layout(
        title="Profit by Category",
        template="plotly_dark",
        height=430,
        paper_bgcolor="#11161e",
        plot_bgcolor="#11161e"
    )

    c1, c2 = st.columns(2)

    with c1:

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

    with c2:

        st.plotly_chart(
            fig_profit,
            use_container_width=True
        )

    # --------------------------------------------------------
    # AREA CHART
    # --------------------------------------------------------

    area_data = monthly_data.copy()

    area_data["Cumulative Sales"] = (
        area_data["Sales"].cumsum()
    )

    fig_area = px.area(
        area_data,
        x="Order Date",
        y="Cumulative Sales"
    )

    fig_area.update_layout(
        title="Cumulative Sales Over Time",
        template="plotly_dark",
        height=430,
        paper_bgcolor="#11161e",
        plot_bgcolor="#11161e"
    )

    st.plotly_chart(
        fig_area,
        use_container_width=True
    )


# ============================================================
# TAB 3 — DISTRIBUTION
# ============================================================

with tab3:

    st.subheader("📊 Distribution & Correlation")

    # --------------------------------------------------------
    # BOX PLOT
    # --------------------------------------------------------

    fig_box = px.box(
        filtered_df,
        x="Category",
        y="Profit",
        points="outliers"
    )

    fig_box.update_layout(
        title="Profit Distribution by Category",
        template="plotly_dark",
        height=430,
        paper_bgcolor="#11161e",
        plot_bgcolor="#11161e"
    )

    # --------------------------------------------------------
    # HISTOGRAM
    # --------------------------------------------------------

    fig_hist = px.histogram(
        filtered_df,
        x="Sales",
        nbins=50
    )

    fig_hist.update_layout(
        title="Sales Distribution",
        template="plotly_dark",
        height=430,
        paper_bgcolor="#11161e",
        plot_bgcolor="#11161e"
    )

    c1, c2 = st.columns(2)

    with c1:

        st.plotly_chart(
            fig_box,
            use_container_width=True
        )

    with c2:

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

    # --------------------------------------------------------
    # HEATMAP
    # --------------------------------------------------------

    numeric_columns = [
        "Sales",
        "Quantity",
        "Discount",
        "Profit",
        "Shipping Cost",
        "Shipping Days",
        "Profit Margin (%)"
    ]

    correlation = (
        filtered_df[numeric_columns]
        .corr()
    )

    fig_heatmap = px.imshow(
        correlation,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1
    )

    fig_heatmap.update_layout(
        title="Correlation Heatmap",
        template="plotly_dark",
        height=520,
        paper_bgcolor="#11161e",
        plot_bgcolor="#11161e"
    )

    st.plotly_chart(
        fig_heatmap,
        use_container_width=True
    )


# ============================================================
# TAB 4 — GLOBAL
# ============================================================

with tab4:

    st.subheader("🌍 Global & Customer Analysis")

    # --------------------------------------------------------
    # CHOROPLETH MAP
    # --------------------------------------------------------

    country_sales = (
        filtered_df
        .groupby("Country")["Sales"]
        .sum()
        .reset_index()
    )

    fig_map = px.choropleth(
        country_sales,
        locations="Country",
        locationmode="country names",
        color="Sales",
        hover_name="Country",
        color_continuous_scale="Blues"
    )

    fig_map.update_layout(
        title="Global Sales by Country",
        template="plotly_dark",
        height=600,
        paper_bgcolor="#11161e",
        geo=dict(
            bgcolor="#11161e"
        )
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True
    )

    # --------------------------------------------------------
    # DONUT CHARTS
    # --------------------------------------------------------

    fig_shipping = px.pie(
        shipping_data,
        names="Ship Mode",
        values="Orders",
        hole=0.55
    )

    fig_shipping.update_layout(
        title="Orders by Shipping Mode",
        template="plotly_dark",
        height=430,
        paper_bgcolor="#11161e",
        plot_bgcolor="#11161e"
    )

    fig_segment = px.pie(
        segment_sales,
        names="Segment",
        values="Sales",
        hole=0.55
    )

    fig_segment.update_layout(
        title="Sales by Customer Segment",
        template="plotly_dark",
        height=430,
        paper_bgcolor="#11161e",
        plot_bgcolor="#11161e"
    )

    c1, c2 = st.columns(2)

    with c1:

        st.plotly_chart(
            fig_shipping,
            use_container_width=True
        )

    with c2:

        st.plotly_chart(
            fig_segment,
            use_container_width=True
        )


# ============================================================
# TAB 5 — INSIGHTS
# ============================================================

with tab5:

    st.subheader("💡 Business Insights")

    # --------------------------------------------------------
    # TOP CATEGORY
    # --------------------------------------------------------

    top_category_row = (
        category_sales
        .sort_values(
            "Sales",
            ascending=False
        )
        .iloc[0]
    )

    top_category = top_category_row["Category"]

    top_category_sales = top_category_row["Sales"]

    # --------------------------------------------------------
    # TOP PROFIT CATEGORY
    # --------------------------------------------------------

    profit_by_category = (
        filtered_df
        .groupby("Category")["Profit"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    top_profit_category = (
        profit_by_category.index[0]
    )

    top_profit_value = (
        profit_by_category.iloc[0]
    )

    # --------------------------------------------------------
    # TOP COUNTRY
    # --------------------------------------------------------

    top_country_row = (
        country_sales
        .sort_values(
            "Sales",
            ascending=False
        )
        .iloc[0]
    )

    top_country = top_country_row["Country"]

    top_country_sales = top_country_row["Sales"]

    # --------------------------------------------------------
    # TOP SEGMENT
    # --------------------------------------------------------

    segment_sales_sorted = (
        segment_sales
        .sort_values(
            "Sales",
            ascending=False
        )
    )

    top_segment = (
        segment_sales_sorted
        .iloc[0]["Segment"]
    )

    # --------------------------------------------------------
    # TOP SUBCATEGORY
    # --------------------------------------------------------

    subcategory_profit = (
        filtered_df
        .groupby("Sub-Category")["Profit"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    top_subcategory = (
        subcategory_profit.index[0]
    )

    top_subcategory_profit = (
        subcategory_profit.iloc[0]
    )

    # --------------------------------------------------------
    # TOP SHIPPING MODE
    # --------------------------------------------------------

    top_shipping = (
        shipping_data
        .sort_values(
            "Orders",
            ascending=False
        )
        .iloc[0]
    )

    top_shipping_mode = top_shipping["Ship Mode"]

    top_shipping_orders = top_shipping["Orders"]

    # --------------------------------------------------------
    # BEST MONTH
    # --------------------------------------------------------

    if not monthly_data.empty:

        best_month_row = (
            monthly_data
            .sort_values(
                "Sales",
                ascending=False
            )
            .iloc[0]
        )

        best_month = best_month_row["Order Date"]

        best_month_sales = best_month_row["Sales"]

    else:

        best_month = None
        best_month_sales = 0

    # --------------------------------------------------------
    # LOSS ANALYSIS
    # --------------------------------------------------------

    loss_data = filtered_df[
        filtered_df["Profit"] < 0
    ]

    loss_transactions = len(loss_data)

    total_loss = abs(
        loss_data["Profit"].sum()
    )

    # --------------------------------------------------------
# INSIGHT CARDS
# --------------------------------------------------------

st.markdown("### Key Business Insights")

# First row
i1, i2, i3 = st.columns(3)

with i1:
    st.metric(
        "🏆 Top Sales Category",
        top_category,
        f"${top_category_sales:,.0f} sales"
    )

with i2:
    st.metric(
        "💰 Top Profit Category",
        top_profit_category,
        f"${top_profit_value:,.0f} profit"
    )

with i3:
    st.metric(
        "🌍 Top Country",
        top_country,
        f"${top_country_sales:,.0f} sales"
    )


# Second row
i1, i2, i3 = st.columns(3)

with i1:
    st.metric(
        "👥 Top Customer Segment",
        top_segment,
        "Highest sales contribution"
    )

with i2:
    st.metric(
        "📦 Most Profitable Sub-Category",
        top_subcategory,
        f"${top_subcategory_profit:,.0f} profit"
    )

with i3:
    st.metric(
        "🚚 Most Used Shipping Mode",
        top_shipping_mode,
        f"{top_shipping_orders:,} orders"
    )
    # ============================================================
# PERFORMANCE SUMMARY
# ============================================================

st.divider()

st.subheader("📋 Performance Summary")

# Create three equal-width columns
col1, col2, col3 = st.columns(3, gap="large")


# ============================================================
# CARD 1 — BEST SALES MONTH
# ============================================================

with col1:

    st.markdown("### 📅 Best Sales Month")

    if best_month is not None:
        st.markdown(
            f"## {best_month.strftime('%B %Y')}"
        )

        st.caption(
            f"Sales: ${best_month_sales:,.0f}"
        )
    else:
        st.info("No sales data available.")


# ============================================================
# CARD 2 — LOSS-MAKING TRANSACTIONS
# ============================================================

with col2:

    st.markdown("### ⚠️ Loss-Making Transactions")

    st.markdown(
        f"## {loss_transactions:,}"
    )

    st.caption(
        f"Total Loss: ${total_loss:,.0f}"
    )


# ============================================================
# CARD 3 — TOTAL QUANTITY SOLD
# ============================================================

with col3:

    st.markdown("### 📦 Total Quantity Sold")

    st.markdown(
        f"## {total_quantity:,}"
    )

    st.caption(
        "Units across filtered orders"
    )

# ============================================================
# DOWNLOAD SECTION
# ============================================================

st.divider()

st.subheader("📥 Export Filtered Data")

csv_data = filtered_df.to_csv(
    index=False
)

st.download_button(
    label="Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_superstore_data.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Global Superstore Analytics • Data Science Project"
)