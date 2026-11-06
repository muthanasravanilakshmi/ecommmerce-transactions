import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================
st.set_page_config(
    page_title="E-Commerce Transaction Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# 2. BLUE + CREAM THEME
#    All styling is contained in this file.
# ==========================================================
st.markdown(
    """
    <style>
    /* Main canvas */
    .stApp {
        background: #F5EEDC !important;
        color: #18324A !important;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Hide the Streamlit main menu containing System / Light / Dark */
    [data-testid="stMainMenu"] {
        display: none !important;
    }

    /* Main content typography */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #173F5F !important;
    }

    .stApp p,
    .stApp [data-testid="stMarkdownContainer"] {
        color: #263F52;
    }

    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background: #173F5F !important;
    }

    section[data-testid="stSidebar"] > div {
        background: #173F5F !important;
    }

    /* Sidebar labels, headings, help text and navigation */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: #FFF8E8 !important;
    }

    /* Text/date/number input: cream surface, dark readable text */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea {
        background: #FFFDF6 !important;
        color: #18324A !important;
        -webkit-text-fill-color: #18324A !important;
        caret-color: #18324A !important;
        opacity: 1 !important;
    }

    section[data-testid="stSidebar"] input::placeholder,
    section[data-testid="stSidebar"] textarea::placeholder {
        color: #657487 !important;
        -webkit-text-fill-color: #657487 !important;
        opacity: 1 !important;
    }

    /* Date picker container and calendar icon area */
    section[data-testid="stSidebar"] [data-testid="stDateInput"] > div,
    section[data-testid="stSidebar"] [data-baseweb="input"] > div {
        background: #FFFDF6 !important;
        border: 1px solid #D9CBAA !important;
        border-radius: 8px !important;
    }

    section[data-testid="stSidebar"] [data-testid="stDateInput"] svg {
        color: #18324A !important;
        fill: #18324A !important;
    }

    /* Select and multiselect control surface */
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #FFFDF6 !important;
        border-color: #D9CBAA !important;
    }

    /* Selected dropdown text and input text */
    section[data-testid="stSidebar"] [data-baseweb="select"] input,
    section[data-testid="stSidebar"] [data-baseweb="select"] [role="combobox"],
    section[data-testid="stSidebar"] [data-baseweb="select"] [aria-selected="true"] {
        color: #18324A !important;
        -webkit-text-fill-color: #18324A !important;
    }

    /* Multiselect selected tags */
    section[data-testid="stSidebar"] [data-baseweb="tag"] {
        background: #1E5A82 !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="tag"] span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* Radio navigation */
    section[data-testid="stSidebar"] [role="radiogroup"] label,
    section[data-testid="stSidebar"] [role="radiogroup"] p {
        color: #FFF8E8 !important;
    }

    /* Main KPI cards */
    [data-testid="stMetric"] {
        background: #FFF9EC !important;
        border: 1px solid #D9CBAA !important;
        border-radius: 14px !important;
        padding: 18px !important;
        box-shadow: 0 3px 10px rgba(23, 63, 95, 0.08);
    }

    [data-testid="stMetricLabel"] {
        color: #526477 !important;
    }

    [data-testid="stMetricValue"] {
        color: #174B70 !important;
        font-weight: 700 !important;
    }

    /* Dataframe surface */
    [data-testid="stDataFrame"],
    [data-testid="stDataEditor"] {
        background: #FFFDF6 !important;
        border: 1px solid #D9CBAA !important;
        border-radius: 10px !important;
    }

    /* Buttons */
    .stButton > button {
        background: #1E5A82 !important;
        color: #FFF9EC !important;
        border: 1px solid #1E5A82 !important;
        border-radius: 8px !important;
    }

    .stButton > button:hover {
        background: #174665 !important;
        color: #FFFFFF !important;
    }

    hr {
        border-color: #D8CBAE !important;
    }

    [data-testid="stCaptionContainer"] {
        color: #657487 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# 3. LOAD CSV FILES
#    Expected structure:
#    project_folder/
#       app.py
#       data/
#          transactions.csv
#          customer.csv
#          merchants.csv
#          categories.csv
# ==========================================================
DATA_DIR = Path(__file__).resolve().parent / "data"


@st.cache_data
def load_data():
    transactions = pd.read_csv(DATA_DIR / "transactions.csv")
    customers = pd.read_csv(DATA_DIR / "customer.csv")
    merchants = pd.read_csv(DATA_DIR / "merchants.csv")
    categories = pd.read_csv(DATA_DIR / "categories.csv")

    for frame in (transactions, customers, merchants, categories):
        frame.columns = frame.columns.str.strip()

    required_transaction_columns = [
        "TransactionID", "UserID", "MerchantID", "CategoryID",
        "Amount", "PaymentMethod", "Status", "TransactionDate",
    ]
    missing = [
        col for col in required_transaction_columns
        if col not in transactions.columns
    ]
    if missing:
        raise ValueError(
            "transactions.csv is missing these required columns: "
            + ", ".join(missing)
        )

    for frame, column in (
        (customers, "UserID"),
        (merchants, "MerchantID"),
        (categories, "CategoryID"),
    ):
        if column not in frame.columns:
            raise ValueError(
                f"Expected column '{column}' was not found in its CSV file."
            )

    transactions["TransactionDate"] = pd.to_datetime(
        transactions["TransactionDate"], errors="coerce"
    )
    transactions["Amount"] = pd.to_numeric(
        transactions["Amount"], errors="coerce"
    )
    transactions["Status"] = (
        transactions["Status"].astype("string").str.strip().str.upper()
    )
    transactions["PaymentMethod"] = (
        transactions["PaymentMethod"].astype("string").str.strip()
    )
    transactions = transactions.dropna(
        subset=["TransactionDate", "Amount"]
    )

    return transactions, customers, merchants, categories


try:
    transactions, customers, merchants, categories = load_data()
except Exception as exc:
    st.error(f"Unable to load project data: {exc}")
    st.info(
        "Confirm that the four CSV files are inside the 'data' folder "
        "next to app.py, and that their column names are correct."
    )
    st.stop()

# ==========================================================
# 4. HELPERS
# ==========================================================
def find_name_column(frame, candidates):
    for column in candidates:
        if column in frame.columns:
            return column
    return None


def currency(value):
    if pd.isna(value):
        value = 0
    return f"₹{value:,.2f}"


def style_chart(fig):
    fig.update_layout(
        paper_bgcolor="#FFF9EC",
        plot_bgcolor="#FFFDF6",
        font=dict(color="#18324A"),
        title_font=dict(color="#173F5F"),
        margin=dict(l=20, r=20, t=55, b=35),
        legend_title_font=dict(color="#173F5F"),
    )
    fig.update_xaxes(showgrid=False, color="#18324A")
    fig.update_yaxes(gridcolor="#E5DCC8", color="#18324A")
    return fig


def show_table(frame):
    st.dataframe(
        frame,
        use_container_width=True,
        hide_index=True,
    )


# ==========================================================
# 5. HEADER
# ==========================================================
st.title("📊 E-Commerce Transaction Analytics")
st.caption(
    "Business Intelligence Dashboard | Transaction Data Analysis (2022–2025)"
)
st.divider()

# ==========================================================
# 6. SIDEBAR FILTERS
# ==========================================================
st.sidebar.title("Dashboard Filters")

valid_dates = transactions["TransactionDate"].dropna()
if valid_dates.empty:
    st.error("No valid transaction dates were found.")
    st.stop()

min_date = valid_dates.min().date()
max_date = valid_dates.max().date()

date_value = st.sidebar.date_input(
    "Transaction Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(date_value, (tuple, list)) and len(date_value) == 2:
    start_date, end_date = date_value
elif isinstance(date_value, (tuple, list)) and len(date_value) == 1:
    start_date = end_date = date_value[0]
else:
    start_date = end_date = date_value

status_options = sorted(
    transactions["Status"].dropna().astype(str).unique().tolist()
)
selected_statuses = st.sidebar.multiselect(
    "Transaction Status",
    options=status_options,
    default=status_options,
)

payment_options = sorted(
    transactions["PaymentMethod"].dropna().astype(str).unique().tolist()
)
selected_payments = st.sidebar.multiselect(
    "Payment Method",
    options=payment_options,
    default=payment_options,
)

selected_cities = []
if "City" in customers.columns:
    city_options = sorted(
        customers["City"].dropna().astype(str).unique().tolist()
    )
    selected_cities = st.sidebar.multiselect(
        "Customer City",
        options=city_options,
        default=[],
    )

# ==========================================================
# 7. APPLY FILTERS
# ==========================================================
filtered = transactions[
    transactions["TransactionDate"].dt.date.between(start_date, end_date)
].copy()

filtered = filtered[
    filtered["Status"].isin(selected_statuses)
    & filtered["PaymentMethod"].isin(selected_payments)
]

if selected_cities:
    city_user_ids = customers.loc[
        customers["City"].astype(str).isin(selected_cities), "UserID"
    ]
    filtered = filtered[filtered["UserID"].isin(city_user_ids)]

successful = filtered[filtered["Status"] == "SUCCESS"].copy()

total_transactions = len(filtered)
successful_count = len(successful)
success_rate = (
    successful_count / total_transactions * 100
    if total_transactions else 0
)
successful_revenue = successful["Amount"].sum()
average_transaction = (
    successful["Amount"].mean() if not successful.empty else 0
)

# ==========================================================
# 8. NAVIGATION
# ==========================================================
page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Sales Analytics",
        "Customer Analytics",
        "Merchant Analytics",
        "Category Analytics",
        "Payment Analytics",
        "Time Series Analysis",
    ],
)

# ==========================================================
# 9. EXECUTIVE OVERVIEW
# ==========================================================
if page == "Executive Overview":
    st.header("Executive Overview")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Transactions", f"{total_transactions:,}")
    k2.metric("Successful Transactions", f"{successful_count:,}")
    k3.metric("Successful Revenue", currency(successful_revenue))
    k4.metric("Success Rate", f"{success_rate:.2f}%")

    st.divider()
    left, right = st.columns(2)

    with left:
        st.subheader("Transaction Status Distribution")
        if not filtered.empty:
            status_data = (
                filtered["Status"].value_counts()
                .rename_axis("Status")
                .reset_index(name="Transactions")
            )
            fig = px.pie(
                status_data,
                names="Status",
                values="Transactions",
                hole=0.45,
                color_discrete_sequence=[
                    "#1E5A82", "#D9B66F", "#8FAF9A", "#D77A61", "#6D8299"
                ],
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)
        else:
            st.info("No transactions match the selected filters.")

    with right:
        st.subheader("Payment Method Distribution")
        if not filtered.empty:
            payment_data = (
                filtered["PaymentMethod"].value_counts()
                .rename_axis("Payment Method")
                .reset_index(name="Transactions")
            )
            fig = px.bar(
                payment_data,
                x="Payment Method",
                y="Transactions",
                color="Payment Method",
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)
        else:
            st.info("No payment data available.")

    st.subheader("Monthly Successful Revenue")
    if not successful.empty:
        monthly = successful.copy()
        monthly["Month"] = monthly["TransactionDate"].dt.to_period("M").astype(str)
        monthly_data = (
            monthly.groupby("Month", as_index=False)["Amount"].sum()
        )
        fig = px.line(
            monthly_data, x="Month", y="Amount", markers=True,
            title="Monthly Revenue Trend",
        )
        fig.update_traces(line=dict(color="#1E5A82", width=3))
        st.plotly_chart(style_chart(fig), use_container_width=True)

    st.subheader("Recent Transactions")
    if not filtered.empty:
        show_table(
            filtered.sort_values("TransactionDate", ascending=False).head(15)
        )
    else:
        st.info("No recent transactions for the selected filters.")

# ==========================================================
# 10. SALES ANALYTICS
# ==========================================================
elif page == "Sales Analytics":
    st.header("Sales Analytics")

    a, b, c = st.columns(3)
    a.metric("Successful Revenue", currency(successful_revenue))
    b.metric("Average Successful Transaction", currency(average_transaction))
    c.metric(
        "Largest Successful Transaction",
        currency(successful["Amount"].max()) if not successful.empty else "₹0.00",
    )

    st.divider()
    if successful.empty:
        st.info("No successful transactions for the selected filters.")
    else:
        sales = successful.copy()
        sales["Month"] = sales["TransactionDate"].dt.to_period("M").astype(str)
        monthly = sales.groupby("Month", as_index=False).agg(
            Revenue=("Amount", "sum"),
            Transactions=("TransactionID", "count"),
        )

        st.subheader("Monthly Successful Revenue")
        fig = px.bar(
            monthly, x="Month", y="Revenue",
            color_discrete_sequence=["#1E5A82"],
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)

        st.subheader("Monthly Transaction Volume")
        fig = px.line(monthly, x="Month", y="Transactions", markers=True)
        fig.update_traces(line=dict(color="#B58A45", width=3))
        st.plotly_chart(style_chart(fig), use_container_width=True)

        st.subheader("Top 10 Successful Transactions")
        show_table(successful.nlargest(10, "Amount"))

# ==========================================================
# 11. CUSTOMER ANALYTICS
# ==========================================================
elif page == "Customer Analytics":
    st.header("Customer Analytics")

    customer_name_col = find_name_column(
        customers, ["FullName", "CustomerName", "Name"]
    )

    customer_summary = (
        successful.groupby("UserID")
        .agg(
            Total_Spending=("Amount", "sum"),
            Total_Transactions=("TransactionID", "count"),
            Last_Transaction=("TransactionDate", "max"),
        )
        .reset_index()
    )

    customer_summary = customer_summary.merge(
        customers, on="UserID", how="left"
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Customers in Customer File", f"{customers['UserID'].nunique():,}")
    c2.metric("Customers with Successful Transactions", f"{customer_summary['UserID'].nunique():,}")
    c3.metric(
        "Average Customer Spending",
        currency(customer_summary["Total_Spending"].mean())
        if not customer_summary.empty else "₹0.00",
    )

    st.divider()
    if customer_summary.empty:
        st.info("No customer transactions match the selected filters.")
    else:
        customer_label = customer_name_col or "UserID"
        st.subheader("Top 10 Customers by Successful Spending")
        top_customers = customer_summary.nlargest(10, "Total_Spending")
        fig = px.bar(
            top_customers, x=customer_label, y="Total_Spending",
            color_discrete_sequence=["#1E5A82"],
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)

        if "City" in customer_summary.columns:
            st.subheader("Customer Distribution by City")
            city_data = (
                customer_summary.groupby("City")
                .size().reset_index(name="Customers")
                .sort_values("Customers", ascending=False).head(15)
            )
            fig = px.bar(
                city_data, x="City", y="Customers",
                color_discrete_sequence=["#B58A45"],
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        st.subheader("RFM Customer Segmentation")
        reference_date = successful["TransactionDate"].max() + pd.Timedelta(days=1)
        rfm = successful.groupby("UserID").agg(
            Recency=("TransactionDate", lambda x: (reference_date - x.max()).days),
            Frequency=("TransactionID", "count"),
            Monetary=("Amount", "sum"),
        ).reset_index()

        if len(rfm) >= 4:
            rfm["R_Score"] = pd.qcut(
                rfm["Recency"].rank(method="first"), 4,
                labels=[4, 3, 2, 1],
            ).astype(int)
            rfm["F_Score"] = pd.qcut(
                rfm["Frequency"].rank(method="first"), 4,
                labels=[1, 2, 3, 4],
            ).astype(int)
            rfm["M_Score"] = pd.qcut(
                rfm["Monetary"].rank(method="first"), 4,
                labels=[1, 2, 3, 4],
            ).astype(int)

            rfm["RFM_Score"] = (
                rfm["R_Score"].astype(str)
                + rfm["F_Score"].astype(str)
                + rfm["M_Score"].astype(str)
            )
            rfm["Segment"] = np.select(
                [
                    (rfm["R_Score"] >= 3) & (rfm["F_Score"] >= 3) & (rfm["M_Score"] >= 3),
                    (rfm["R_Score"] >= 3) & (rfm["F_Score"] <= 2),
                    (rfm["R_Score"] <= 2) & (rfm["F_Score"] >= 3),
                ],
                ["Champions", "New / Promising", "At Risk"],
                default="Regular Customers",
            )
            segment_data = rfm["Segment"].value_counts().rename_axis(
                "Segment"
            ).reset_index(name="Customers")
            fig = px.pie(
                segment_data, names="Segment", values="Customers", hole=0.4
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)
            show_table(rfm.sort_values("Monetary", ascending=False))
        else:
            st.info("At least four active customers are needed for quartile-based RFM scoring.")

        st.subheader("Customer Spending Details")
        show_table(customer_summary.sort_values("Total_Spending", ascending=False))

# ==========================================================
# 12. MERCHANT ANALYTICS
# ==========================================================
elif page == "Merchant Analytics":
    st.header("Merchant Analytics")

    merchant_name_col = find_name_column(
        merchants, ["MerchantName", "BusinessName", "Name"]
    )

    merchant_summary = filtered.groupby("MerchantID").agg(
        Total_Transactions=("TransactionID", "count"),
        Successful_Transactions=("Status", lambda x: (x == "SUCCESS").sum()),
    ).reset_index()

    merchant_revenue = successful.groupby("MerchantID")["Amount"].sum().reset_index(
        name="Successful_Revenue"
    )
    merchant_summary = merchant_summary.merge(
        merchant_revenue, on="MerchantID", how="left"
    )
    merchant_summary["Successful_Revenue"] = merchant_summary[
        "Successful_Revenue"
    ].fillna(0)

    merchant_summary["Failure_Rate"] = (
        (merchant_summary["Total_Transactions"] - merchant_summary["Successful_Transactions"])
        / merchant_summary["Total_Transactions"].replace(0, np.nan)
    ) * 100

    merchant_summary = merchant_summary.merge(
        merchants, on="MerchantID", how="left"
    )

    x, y, z = st.columns(3)
    x.metric("Merchants in Merchant File", f"{merchants['MerchantID'].nunique():,}")
    y.metric("Merchants with Filtered Transactions", f"{merchant_summary['MerchantID'].nunique():,}")
    z.metric("Successful Merchant Revenue", currency(merchant_summary["Successful_Revenue"].sum()))

    st.divider()
    if merchant_summary.empty:
        st.info("No merchant transactions match the selected filters.")
    else:
        merchant_label = merchant_name_col or "MerchantID"

        st.subheader("Top 10 Merchants by Successful Revenue")
        top_merchants = merchant_summary.nlargest(10, "Successful_Revenue")
        fig = px.bar(
            top_merchants, x=merchant_label, y="Successful_Revenue",
            color_discrete_sequence=["#1E5A82"],
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)

        st.subheader("Merchant Failure Rate")
        failure_data = merchant_summary.nlargest(15, "Failure_Rate")
        fig = px.bar(
            failure_data, x=merchant_label, y="Failure_Rate",
            color_discrete_sequence=["#B58A45"],
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)

        show_table(merchant_summary.sort_values("Successful_Revenue", ascending=False))

# ==========================================================
# 13. CATEGORY ANALYTICS
# ==========================================================
elif page == "Category Analytics":
    st.header("Category Analytics")

    category_name_col = find_name_column(
        categories, ["CategoryName", "Category", "Name"]
    )

    category_summary = successful.groupby("CategoryID").agg(
        Revenue=("Amount", "sum"),
        Transactions=("TransactionID", "count"),
        Average_Amount=("Amount", "mean"),
    ).reset_index()

    category_summary = category_summary.merge(
        categories, on="CategoryID", how="left"
    )

    x, y = st.columns(2)
    x.metric("Categories in Category File", f"{categories['CategoryID'].nunique():,}")
    y.metric("Categories with Successful Sales", f"{category_summary['CategoryID'].nunique():,}")

    st.divider()
    if category_summary.empty:
        st.info("No category sales match the selected filters.")
    else:
        category_label = category_name_col or "CategoryID"

        st.subheader("Revenue by Category")
        top_categories = category_summary.nlargest(15, "Revenue")
        fig = px.bar(
            top_categories, x=category_label, y="Revenue",
            color_discrete_sequence=["#1E5A82"],
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)

        st.subheader("Category Revenue Distribution")
        fig = px.pie(
            category_summary, names=category_label,
            values="Revenue", hole=0.4,
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)

        show_table(category_summary.sort_values("Revenue", ascending=False))

# ==========================================================
# 14. PAYMENT ANALYTICS
# ==========================================================
elif page == "Payment Analytics":
    st.header("Payment Analytics")

    payment_summary = filtered.groupby("PaymentMethod").agg(
        Total_Transactions=("TransactionID", "count"),
        Successful_Transactions=("Status", lambda x: (x == "SUCCESS").sum()),
    ).reset_index()

    payment_revenue = successful.groupby("PaymentMethod")["Amount"].sum().reset_index(
        name="Successful_Revenue"
    )
    payment_summary = payment_summary.merge(
        payment_revenue, on="PaymentMethod", how="left"
    )
    payment_summary["Successful_Revenue"] = payment_summary[
        "Successful_Revenue"
    ].fillna(0)
    payment_summary["Success_Rate"] = (
        payment_summary["Successful_Transactions"]
        / payment_summary["Total_Transactions"].replace(0, np.nan)
    ) * 100

    a, b = st.columns(2)
    a.metric("Payment Methods in Filtered Data", f"{filtered['PaymentMethod'].nunique()}")
    b.metric("Successful Transactions", f"{successful_count:,}")

    st.divider()
    if payment_summary.empty:
        st.info("No payment data matches the selected filters.")
    else:
        st.subheader("Transactions by Payment Method")
        fig = px.bar(
            payment_summary, x="PaymentMethod", y="Total_Transactions",
            color="PaymentMethod",
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)

        st.subheader("Success Rate by Payment Method")
        fig = px.bar(
            payment_summary, x="PaymentMethod", y="Success_Rate",
            color_discrete_sequence=["#1E5A82"],
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)

        if payment_summary["Successful_Revenue"].sum() > 0:
            st.subheader("Successful Revenue by Payment Method")
            fig = px.pie(
                payment_summary, names="PaymentMethod",
                values="Successful_Revenue", hole=0.4,
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        show_table(payment_summary)

# ==========================================================
# 15. TIME SERIES ANALYSIS
# ==========================================================
elif page == "Time Series Analysis":
    st.header("Time Series Analysis")

    if filtered.empty:
        st.info("No transactions match the selected filters.")
    else:
        time_data = filtered.copy()
        time_data["Year"] = time_data["TransactionDate"].dt.year
        time_data["Month"] = time_data["TransactionDate"].dt.to_period("M").astype(str)
        time_data["Day"] = time_data["TransactionDate"].dt.date

        left, right = st.columns(2)

        with left:
            st.subheader("Yearly Transaction Volume")
            yearly = time_data.groupby("Year").size().reset_index(name="Transactions")
            fig = px.bar(
                yearly, x="Year", y="Transactions",
                color_discrete_sequence=["#1E5A82"],
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        with right:
            st.subheader("Monthly Transaction Volume")
            monthly = time_data.groupby("Month").size().reset_index(name="Transactions")
            fig = px.line(monthly, x="Month", y="Transactions", markers=True)
            fig.update_traces(line=dict(color="#B58A45", width=3))
            st.plotly_chart(style_chart(fig), use_container_width=True)

        st.subheader("Daily Transaction Volume")
        daily = time_data.groupby("Day").size().reset_index(name="Transactions")
        fig = px.area(
            daily, x="Day", y="Transactions",
            color_discrete_sequence=["#8FAFCA"],
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)

        if not successful.empty:
            st.subheader("Monthly Successful Revenue Growth")
            monthly_revenue = successful.copy()
            monthly_revenue["Month"] = (
                monthly_revenue["TransactionDate"].dt.to_period("M").astype(str)
            )
            monthly_revenue = monthly_revenue.groupby("Month")["Amount"].sum().reset_index()
            monthly_revenue["Previous_Month"] = monthly_revenue["Amount"].shift(1)
            monthly_revenue["Growth_Percentage"] = (
                (monthly_revenue["Amount"] - monthly_revenue["Previous_Month"])
                / monthly_revenue["Previous_Month"].abs().replace(0, np.nan)
            ) * 100

            fig = px.line(
                monthly_revenue, x="Month", y="Growth_Percentage", markers=True
            )
            fig.update_traces(line=dict(color="#1E5A82", width=3))
            st.plotly_chart(style_chart(fig), use_container_width=True)
            show_table(monthly_revenue)

# ==========================================================
# 16. FOOTER
# ==========================================================
st.divider()
st.markdown(
    """
    <div style="
        text-align:center;
        padding:22px 12px;
        margin-top:20px;
        border-top:1px solid #D8CBAE;
        color:#526477;
        font-size:14px;
        line-height:1.8;
    ">
        <div style="color:#173F5F; font-weight:600;">
            E-Commerce Transaction Analytics Dashboard
        </div>
        <div>
            Built using Python, Pandas, NumPy, Plotly and Streamlit
        </div>
        <div style="margin-top:8px; font-size:13px;">
            © 2026 Sravani Muthana. All rights reserved.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
