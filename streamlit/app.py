import streamlit as st

from database import check_connection, run_query
from queries import (QUERIES, get_monthly_revenue, get_category_revenue,get_top_selling_product,get_location_sales,
                     get_customer_distribution,get_customer_spending,get_one_time_vs_repeat_custcount,
                     get_top_seller,get_seller_count,get_seller_revenue,get_category_yearly_revenue,get_seller_rating,
                     get_avg_delivery_day,get_monthly_avg_delivery_day,get_on_time_delayed_delivery,get_location_delivery,get_delay_vs_review_score,
                     get_customer_review_data,get_category_review,get_review_cust_count)
from utils import money_short,show_chart,KPI_ICONS,kpi_card

# ---------------- Page setup ----------------
st.set_page_config(
    page_title="Cart2Insights | E-commerce Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- Theme ----------------
st.markdown("""
<style>
:root { --navy:#153653; --teal:#159A9C; --muted:#66788A; }
.stApp { background:#F4F7FB; color:#19324A; }
.block-container { max-width:1550px; padding:1.4rem 2rem 2.5rem; }
section[data-testid="stSidebar"] { background:#FFFFFF; border-right:1px solid #E5ECF3; }
.hero {
  background:linear-gradient(115deg,#102B46 0%,#175577 72%,#159A9C 100%);
  padding:1.6rem 1.8rem; border-radius:18px; color:#fff;
  margin-bottom:1.25rem; box-shadow:0 8px 24px rgba(16,43,70,.12);
}
.hero h1 { color:#fff; font-size:2.05rem; font-weight:750; margin:0; letter-spacing:-.5px; }
.hero p { color:#D9EAF4; margin:.35rem 0 0; font-size:.95rem; }
.eyebrow { color:#159A9C; font-size:.75rem; font-weight:800; letter-spacing:1.4px; text-transform:uppercase; }
.section-heading { color:#153653; font-size:1.35rem; font-weight:750; margin:.3rem 0 .8rem; }
.helper { color:#66788A; font-size:.88rem; }
div[data-testid="stDataFrame"] {
  background:#fff; border:1px solid #E4EBF3; border-radius:15px;
  padding:8px; box-shadow:0 4px 16px rgba(21,54,83,.035);
}
.stSelectbox [data-baseweb="select"] { background:#fff; }
hr { border-color:#E0E8F0; }
.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E0E8F2;
    border-radius: 16px;
    padding: 22px 24px;
    min-height: 110px;
    box-shadow: 0 4px 14px rgba(23,59,94,0.05);
    margin-bottom: 12px;
    transition: 0.2s ease;
}
.kpi-card:hover {
    border-color: #14B8A6;
    transform: translateY(-2px);
}
.kpi-label {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #64748B;
    font-size: 15px;
    font-weight: 500;
}
.kpi-icon {
    display: flex;
    align-items: center;
}
.kpi-icon svg {
    width: 26px;
    height: 26px;
}
.kpi-value {
    margin-top: 12px;
    font-size: 32px;
    font-weight: 750;
    color: #173B5E;
    line-height: 1.2;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Navigation ----------------

PageSection=["Project Introduction","Business Overview","Sales Analysis","Customer Analysis","Seller & Product Analysis","Delivery Analysis","Customer Experience"]


with st.sidebar:
    st.markdown("## Cart2Insights")
    st.caption("E-commerce performance studio")
    st.divider()
    section = st.sidebar.radio("Dashboard section", PageSection)

    st.divider()
    with st.expander("Database connection"):
        if st.button("Test SQL Server", use_container_width=True):
            try:
                status = check_connection()
                st.success(f"Connected · {status['database_name']}")
                st.caption(f"Server: {status['server_name']}")
            except Exception as exc:
                st.error("Connection failed.")
                st.code(str(exc))

# ---------------- Shared helpers ----------------
def page_header(title, subtitle):
    st.markdown(
        f'<div class="hero"><div class="eyebrow" style="color:#A8E6E0">CART2INSIGHTS / ANALYTICS</div>'
        f'<h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )

def section_title(title, caption=None):
    st.markdown(f'<div class="section-heading">{title}</div>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<div class="helper">{caption}</div>', unsafe_allow_html=True)


# ---------------- Page content ----------------
try:
    if section == "Project Introduction":
        page_header("Welcome to Cart2Insights", "E-commerce intelligence, made easier.")
        left, right = st.columns([1.2, 1], gap="large")
        with left:
            st.markdown("### Turn order data into business direction")
            st.write(
                "Explore Olist e-commerce performance through focused reports for sales, "
                "customers, products, sellers, delivery and customer experience."
            )
            st.markdown("""
            - **Business overview:** headline performance indicators
            - **Sales:** yearly and monthly revenue trends
            - **Customers:** spending and repeat-purchase patterns
            - **Seller & products:** rankings and category performance
            - **Delivery:** delivery outcomes and delays
            - **Customer experience:** reviews and satisfaction
            """)
            st.info("Data source: Olist dataset · SQL Server database: Guviproject")
        with right:
            st.image("Image/cart2insight.png")
    elif section == "Business Overview":
        page_header("Business Overview", "A clear view of sales, customers, sellers and customer satisfaction.")
        # Existing KPI SQL definitions are retained.
        with st.spinner("Loading business metrics..."):
            k1, k2, k3 = st.columns(3)
            k4, k5, k6 = st.columns(3)

            kpi_keys = [
                "TOTAL_REVENUE", "TOTAL_ORDERS", "TOTAL_CUSTOMERS",
                "TOTAL_SELLERS", "AVERAGE_ORDER_VALUE", "AVERAGE_REVIEW_SCORE",
            ]
            kpi_results = {}

            for key in kpi_keys:
                df = run_query(QUERIES[key])
                kpi_results[key] = df.iloc[0, 0] if not df.empty else 0

            total_revenue = kpi_results["TOTAL_REVENUE"]
            total_orders = kpi_results["TOTAL_ORDERS"]
            total_customers = kpi_results["TOTAL_CUSTOMERS"]
            total_sellers = kpi_results["TOTAL_SELLERS"]
            aov = kpi_results["AVERAGE_ORDER_VALUE"]
            review_score = kpi_results["AVERAGE_REVIEW_SCORE"]

            with k1:
                kpi_card(KPI_ICONS["revenue"], "Total Revenue",
                         money_short(total_revenue))

            with k2:
                kpi_card(KPI_ICONS["orders"], "Total Orders",
                         f"{total_orders:,}")

            with k3:
                kpi_card(KPI_ICONS["customers"], "Total Customers",
                         f"{total_customers:,}")
            with k4:
                kpi_card(KPI_ICONS["sellers"], "Total Sellers",
                         f"{total_sellers:,}")

            with k5:
                kpi_card(KPI_ICONS["aov"], "Average Order Value",
                         f"R${aov:,.0f}")

            with k6:
                kpi_card(KPI_ICONS["reviews"], "Average Review Score",
                         f"{review_score:.2f} / 5")
        st.divider()
        section_title("Sales performance", "Year-over-year view of delivered orders and revenue.")

        query_key = "YEARLY_REVENUE_ORDERS"
        YearlySales = run_query(QUERIES[query_key])

        if YearlySales.empty:
            st.info("No yearly sales data is available.")
        else:
            left, right = st.columns(2)
            with left:
                show_chart("Line", YearlySales["order_year"].astype("string"), YearlySales["total_revenue"], "Year",
                           "Revenue (R$)", "Yearly Sales Revenue",(8, 5),"#20B2AA")
            with right:
                show_chart("Bar", YearlySales["order_year"].astype("string"), YearlySales["total_orders"], "Year",
                           "Delivered orders", "Yearly Delivered orders",(8, 5),"#6C9FE8")

    elif section == "Sales Analysis":
        page_header("Sales Analysis", "Track monthly momentum and understand which categories drive revenue.")
        query_key = "LOAD_YEAR"
        years_df = run_query(QUERIES[query_key])
        if years_df.empty:
            st.warning("No purchase years found.")
        else:
            year_col, note_col = st.columns([1, 3], vertical_alignment="bottom")
            with year_col:
                selected_year = st.selectbox("Purchase year", years_df, index=0)
            with note_col:
                st.caption(f"Showing delivered-order sales for {selected_year}.")

            MonthlyRevenueQuery = get_monthly_revenue(selected_year)
            MonthlyRevenue = run_query(MonthlyRevenueQuery)
            MonthlyRevenue['MoM_Growth'] = MonthlyRevenue['revenue'].pct_change() * 100

            CategoryRevenueQuery = get_category_revenue(selected_year)
            CategoryRevenue = run_query(CategoryRevenueQuery)

            left, right = st.columns(2, gap="large")
            with left:
                section_title("Monthly revenue", "Revenue trend across the selected year.")
                if not MonthlyRevenue.empty:
                    show_chart("Line", MonthlyRevenue["MonthName"].astype("string"), MonthlyRevenue["revenue"], "Month",
                               "Revenue(R$)", "Monthly Sales", (8, 5),"#20B2AA")
                    section_title("", "Revenue Growth%.")
                    colors = ['#85B79A' if x >= 0 else '#E8878C'
                              for x in MonthlyRevenue['MoM_Growth'].fillna(0)]

                    show_chart("Bar", MonthlyRevenue["MonthName"].astype("string"), MonthlyRevenue["MoM_Growth"], "Month",
                           "Growth (%)", "Month-over-Month Revenue Growth", (8, 5),colors)
                else:
                    st.info("No monthly data for this year.")
            with right:
                section_title("Revenue by category", "Categories ranked by revenue.")
                if not CategoryRevenue.empty:
                    TopCategory = CategoryRevenue.nlargest(15, 'Revenue').sort_values('Revenue')
                    show_chart("Barh", TopCategory["Product Category"].astype("string"), TopCategory["Revenue"], "Product Category",
                               "Revenue(R$)", "Monthly Sales", (5, 4),"#60A5FA")
                    section_title("", "All Categories")
                    st.dataframe(CategoryRevenue, use_container_width=True, hide_index=True, height=380)
                else:
                    st.info("No category data for this year.")

            R2left, R2right = st.columns(2, gap="large")

            TopSellingProductQuery = get_top_selling_product(selected_year)
            TopSellingProduct = run_query(TopSellingProductQuery)

            LocationSaleQuery=get_location_sales(selected_year)
            LocationSale = run_query(LocationSaleQuery)
            with R2left:
                section_title("Top Selling Products", "Top selling products across the selected year.")
                if not TopSellingProduct.empty:
                    TopSellingProduct = TopSellingProduct.sort_values('SaleValue')
                    show_chart("Barh", TopSellingProduct["Product"], TopSellingProduct["SaleValue"], "Product",
                               "Sale Value(R$)", "Top Selling Product", (8, 6), "#60A5FA")
                else:
                    st.info("No product data for this year.")
            with R2right:
                section_title("Sales by Location", "Locational sales across the selected year.")
                if not LocationSale.empty:
                    show_chart("Bar", LocationSale["State"], LocationSale["SaleValue"], "State",
                               "Sale Value(R$)", "Sales by Location", (8, 5), "#60A5FA")
                else:
                    st.info("No location data for this year.")
    elif section=="Customer Analysis":
        page_header(section, f"Analyze customer behavior, purchasing patterns.")

        query_key = "LOAD_YEAR"
        years_df = run_query(QUERIES[query_key])
        if years_df.empty:
            st.warning("No purchase years found.")
        else:
            year_col, note_col = st.columns([1, 3], vertical_alignment="bottom")
            with year_col:
                selected_year = st.selectbox("Purchase year", years_df, index=0)
            with note_col:
                st.caption(f"Showing delivered-order sales for {selected_year}.")

        CustomerDistributionQuery = get_customer_distribution(selected_year)
        CustomerDistribution = run_query(CustomerDistributionQuery)

        CustomerSpendingQuery = get_customer_spending(selected_year)
        CustomerSpending = run_query(CustomerSpendingQuery)

        CustomerTypeQuery = get_one_time_vs_repeat_custcount(selected_year)
        CustomerType = run_query(CustomerTypeQuery)

        TopCustomers=CustomerSpending.nlargest(15, 'total_spending').sort_values('total_spending')

        n_customers = int(CustomerSpending["customer_unique_id"].nunique()) if not CustomerSpending.empty else 0
        revenue = float(CustomerSpending["total_spending"].sum()) if not CustomerSpending.empty else 0
        avg_spend = float(CustomerSpending["total_spending"].mean()) if not CustomerSpending.empty else 0
        repeat_n = int(CustomerType.loc[CustomerType.customer_type == "Repeat", "customers"].sum()) if not CustomerType.empty else 0

        a, b, c= st.columns(3)

        with a:
            kpi_card(KPI_ICONS["customers"], "Unique Customers",
                     f"{n_customers:,}")
        with b:
            kpi_card(KPI_ICONS["revenue"], "Total Revenue",
                     money_short(revenue))
        with c:
            kpi_card(KPI_ICONS["aov"], "Average Spend",
                     f"R${avg_spend:,.0f}")

        st.divider()
        st.subheader("Customer Distribution")
        if CustomerDistribution.empty:
            st.info("No delivered customer records found.")
        else:
            show_chart("Bar", CustomerDistribution["state"], CustomerDistribution["customers"], "State",
                       "No.of Customers", "Statewise customer count", (15, 4), "#60A5FA")

        left, right = st.columns(2)
        with left:
            st.subheader("Customer Spending")
            if CustomerSpending.empty:
                st.info("No spending data found.")
            else:
                show_chart("Scatter", CustomerSpending["order_count"], CustomerSpending["total_spending"], "Customer Count",
                           "Spending", "Customer spending", (4, 3), "#60A5FA")

        with right:
            st.subheader("Repeat vs New Customers")
            if CustomerType.empty:
                st.info("No customer data found.")
            else:
                colors =  ["#64748B", "#14B8A6"]
                show_chart("Donut", CustomerType["customer_type"], CustomerType["CustomerPercentage"],
                           "",
                           "", "Repeat vs New Customer", (4,3), colors)

        st.divider()
        st.subheader("Top Customers")
        if TopCustomers.empty:
            st.info("No customer records found.")
        else:
            TopCustomers = TopCustomers.sort_values('total_spending')
            show_chart("Barh", TopCustomers["customer_unique_id"], TopCustomers["total_spending"], "Spending (R$)",
                       "Customer", "Top Customers", (15, 5), "#60A5FA")

    elif section=="Seller & Product Analysis":
        page_header(section, f"Analyze seller performance, product sales, and category trends.")

        query_key = "LOAD_YEAR"
        years_df = run_query(QUERIES[query_key])
        if years_df.empty:
            st.warning("No purchase years found.")
        else:
            year_col, note_col = st.columns([1, 3], vertical_alignment="bottom")
            with year_col:
                selected_year = st.selectbox("Selling year", years_df, index=0)
            with note_col:
                st.caption(f"Showing delivered-order sales for {selected_year}.")

        TopSellerQuery = get_top_seller(selected_year)
        TopSeller = run_query(TopSellerQuery)

        TopSellerCountQuery = get_seller_count(selected_year)
        TopSellerCount = run_query(TopSellerCountQuery)

        SellerRevenueQuery = get_seller_revenue(selected_year)
        SellerRevenue = run_query(SellerRevenueQuery)

        YearlyCategoryRevenueQuery = get_category_yearly_revenue(selected_year)
        YearlyCategoryRevenue = run_query(YearlyCategoryRevenueQuery)

        SellerRatingDistributionQuery = get_seller_rating(selected_year)
        SellerRatingDistribution = run_query(SellerRatingDistributionQuery)

        n_seller = int(SellerRevenue["SellerID"].nunique()) if not SellerRevenue.empty else 0
        revenue = float(SellerRevenue["SellerRevenue"].sum()) if not SellerRevenue.empty else 0
        avg_rating = float(SellerRatingDistribution["avg_rating"].mean()) if not SellerRatingDistribution.empty else 0

        a, b, c = st.columns(3)

        with a:
            kpi_card(KPI_ICONS["customers"], "Unique Seller",
                     f"{n_seller:,}")
        with b:
            kpi_card(KPI_ICONS["revenue"], "Total Revenue",
                     money_short(revenue))
        with c:
            kpi_card(KPI_ICONS["reviews"], "Average Seller Rating",
                     f"R${avg_rating:,.0f}")

        st.divider()

        left, right = st.columns(2)
        with left:
            st.subheader("Top Seller by Revenue")
            if TopSeller.empty:
                st.info("No seller data found.")
            else:
                TopSeller = TopSeller.sort_values('SellerRevenue')
                show_chart("Barh", TopSeller["SellerID"], TopSeller["SellerRevenue"],
                           "Revenue (R$)","Seller ID",
                            "Top seller by revenue", (8, 5), "#4F79B8")

        with right:
            st.subheader("Top Seller by Orders")
            if TopSellerCount.empty:
                st.info("No seller data found.")
            else:
                TopSellerCount = TopSellerCount.sort_values('TotalOrderCount')
                show_chart("Barh", TopSellerCount["SellerID"], TopSellerCount["TotalOrderCount"],
                           "Order Count","Seller ID",
                            "Top seller by OrderCount", (8, 5), "#14A38B")
        leftR2, rightR2 = st.columns(2)
        with leftR2:
            st.subheader("Top Category by Revenue")
            if YearlyCategoryRevenue.empty:
                st.info("No seller data found.")
            else:
                show_chart("Bar", YearlyCategoryRevenue["category"], YearlyCategoryRevenue["revenue"],
                           "category", "Revenue (R$)",
                           "Top seller by revenue", (8, 5), "#8B78C6")

        with rightR2:
            st.subheader("Seller rating Distribution")
            if SellerRatingDistribution.empty:
                st.info("No seller data found.")
            else:
                show_chart("Histogram", "", SellerRatingDistribution["avg_rating"],
                           "Review Score", "Seller Count",
                           "Seller Rating distribution", (8, 5), "#E5A33D")

    elif section=="Delivery Analysis":
        page_header(section, f"Analyze delivery performance and identify opportunities to improve order fulfillment.")

        query_key = "LOAD_YEAR"
        years_df = run_query(QUERIES[query_key])
        if years_df.empty:
            st.warning("No purchase years found.")
        else:
            year_col, note_col = st.columns([1, 3], vertical_alignment="bottom")
            with year_col:
                selected_year = st.selectbox("Selling year", years_df, index=0)
            with note_col:
                st.caption(f"Showing delivered-order sales for {selected_year}.")

        AvgDeliveryDayQuery = get_avg_delivery_day(selected_year)
        AvgDeliveryDay = run_query(AvgDeliveryDayQuery)

        MonthlyAvgDeliveryDayQuery = get_monthly_avg_delivery_day(selected_year)
        MonthlyAvgDeliveryDay = run_query(MonthlyAvgDeliveryDayQuery)

        DeliveryStatusQuery = get_on_time_delayed_delivery(selected_year)
        DeliveryStatus = run_query(DeliveryStatusQuery)

        DeliveryLocationQuery = get_location_delivery(selected_year)
        DeliveryLocation = run_query(DeliveryLocationQuery)

        DelayReviewScoreQuery = get_delay_vs_review_score(selected_year)
        DelayReviewScore = run_query(DelayReviewScoreQuery)

        total = DeliveryStatus["order_count"].sum()

        on_time = DeliveryStatus.loc[
            DeliveryStatus["delivery_status"] == "On-Time",
            "order_count"
        ].sum()

        avg_delivery_delay=AvgDeliveryDay["avg_delivery_days"].iloc[0]
        on_time_rate = on_time / total * 100 if total else 0
        delayed_rate = 100 - on_time_rate if total else 0

        a, b, c = st.columns(3)
        with a:
            kpi_card(KPI_ICONS["customers"], "Average Delivery Day(s)",
                     f"{avg_delivery_delay:,.0f}")
        with b:
            kpi_card(KPI_ICONS["revenue"], "On-Time Delivery Rate",
                     f"{on_time_rate:,.2f}")
        with c:
            kpi_card(KPI_ICONS["reviews"], "Delayed Delivery Rate",
                     f"{delayed_rate:,.2f}")

        st.divider()

        leftR1, rightR1 = st.columns(2)
        with leftR1:
            st.subheader("Delivery time trend")
            if MonthlyAvgDeliveryDay.empty:
                st.info("No delivery data found.")
            else:
                show_chart("Line", MonthlyAvgDeliveryDay["month_name"], MonthlyAvgDeliveryDay["avg_delivery_days"],
                           "Month", "Average Delivery Day",
                           "Average Delivery day trend", (8, 5), "#4F79B8")

        with rightR1:
            st.subheader("On-Time vs Delayed")
            if DeliveryStatus.empty:
                st.info("No seller data found.")
            else:
                colors = ["#64748B", "#14B8A6"]
                show_chart("Donut", DeliveryStatus["delivery_status"], DeliveryStatus["order_count"],
                           "", "",
                           "On-Time vs Delayed", (8, 5), colors)

        leftR2, rightR2 = st.columns(2)
        with leftR2:
            st.subheader("Delivery performance by state")
            if DeliveryLocation.empty:
                st.info("No delivery data found.")
            else:
                show_chart("Barh", DeliveryLocation["customer_state"], DeliveryLocation["delayed_rate"],
                           "Delayed Delivery Rate (%)", "Customer State",
                           "States by Delivery Delay Rate", (8, 5), "#8B78C6")

        with rightR2:
            st.subheader("Delivery Delay vs Review Score")
            if DelayReviewScore.empty:
                st.info("No delivery data found.")
            else:
                colors = ["#64748B", "#14B8A6"]
                show_chart("Bar", DelayReviewScore["delay_group"], DelayReviewScore["avg_review_score"],
                           "Delay Group", "Average review score",
                           "Delivery Delay vs Review Score", (8, 5), "#64748B")
    elif section=="Customer Experience":
        page_header(section, f"Analyze customer satisfaction, review patterns, and delivery experiences")

        query_key = "LOAD_YEAR"
        years_df = run_query(QUERIES[query_key])
        if years_df.empty:
            st.warning("No purchase years found.")
        else:
            year_col, note_col = st.columns([1, 3], vertical_alignment="bottom")
            with year_col:
                selected_year = st.selectbox("Selling year", years_df, index=0)
            with note_col:
                st.caption(f"Showing delivered-order sales for {selected_year}.")

        CustomerReviewQuery = get_customer_review_data(selected_year)
        CustomerReview = run_query(CustomerReviewQuery)

        CategoryReviewQuery = get_category_review(selected_year)
        CategoryReview = run_query(CategoryReviewQuery)

        LowRatedCategories = CategoryReview.nsmallest(
            15, "avg_review_score"
        )

        ReviewCustCountQuery = get_review_cust_count(selected_year)
        ReviewCustCount = run_query(ReviewCustCountQuery)

        avg_review_score = CustomerReview["avg_review_score"].iloc[0]
        positive_review_pct = CustomerReview["positive_review_pct"].iloc[0]
        negative_review_pct = CustomerReview["negative_review_pct"].iloc[0]

        a, b, c = st.columns(3)
        with a:
            kpi_card(KPI_ICONS["customers"], "Average Review Score",
                     f"{avg_review_score:,.0f}")
        with b:
            kpi_card(KPI_ICONS["revenue"], "Positive Review Score",
                     f"{positive_review_pct:,.2f}")
        with c:
            kpi_card(KPI_ICONS["reviews"], "Negative Review Score",
                     f"{negative_review_pct:,.2f}")
        st.divider()

        leftR1, rightR1 = st.columns(2)
        with leftR1:
            st.subheader("Low-rated Products")
            if LowRatedCategories.empty:
                st.info("No delivery data found.")
            else:
                show_chart("Barh", LowRatedCategories["category"], LowRatedCategories["avg_review_score"],
                           "Category", "Average Review Score",
                           "15 Lowest-Rated Product Categories", (8, 6), "#8B78C6")

        with rightR1:
            st.subheader("Review Score Distribution by Delivery Status")
            if ReviewCustCount.empty:
                st.info("No seller data found.")
            else:
                pivot_data = ReviewCustCount.pivot(
                    index="DeliveryStatus",
                    columns="ReviewScore",
                    values="ReviewCount"
                ).fillna(0)
            review_colors = [
                "#E76F51",  # 1 star - Coral red
                "#F4A261",  # 2 stars - Orange
                "#E9C46A",  # 3 stars - Amber
                "#8AB17D",  # 4 stars - Soft green
                "#2A9D8F"  # 5 stars - Teal green
            ]

            show_chart("PivotBar", "", "",
                       "Delivery Status", "Number of Reviews",
                       "Review Score Distribution by Delivery Status", (8, 5), review_colors,pivot_data)
    else:
        page_header(section, f"Explore {section.lower()} insights using the Olist dataset.")

except Exception as exc:
    st.error("The report could not be loaded. Please verify the SQL Server connection and query.")
    with st.expander("Technical details"):
        st.exception(exc)
