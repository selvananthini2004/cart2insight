# Cart2Insights – E-commerce Analytics Dashboard
Cart2Insights is a Streamlit-based analytics dashboard for exploring e-commerce performance using the Olist dataset. It connects to a SQL Server database and presents interactive reports covering sales, customers, sellers, products, delivery performance, and customer experience.

## Features

The dashboard is organized into seven sections:

| Section | What it provides |
|---|---|
| **Project Introduction** | Project overview, business context, and data source information |
| **Business Overview** | Key performance indicators such as total revenue, orders, customers, sellers, average order value, and average review score |
| **Sales Analysis** | Year-based analysis of monthly revenue, month-over-month growth, category revenue, top-selling products, and sales by state |
| **Customer Analysis** | Customer distribution by state, customer spending, one-time vs. repeat customers, and top customers |
| **Seller & Product Analysis** | Seller revenue and order rankings, category revenue, and seller rating distribution |
| **Delivery Analysis** | Average delivery time, monthly delivery trends, on-time vs. delayed orders, state-level delay rates, and delivery delay vs. review score |
| **Customer Experience** | Average and positive/negative review indicators, low-rated product categories, and review distribution by delivery status |

Additional interface features include:
- Year selectors for time-based reports.
- KPI cards and charts for at-a-glance analysis.
- A sidebar option to test the SQL Server connection.
- Error messages with expandable technical details when a report cannot be loaded.

## Technology Stack

- **Python**
- **Streamlit** – dashboard interface
- **Microsoft SQL Server** – data storage and SQL query execution
- **Pandas** – tabular query results and data transformations
- **Chart utilities** – chart rendering is handled by the project's `utils.py` module

## data
Raw & cleaned data - [Click here to download data](https://drive.google.com/drive/folders/1Hr6JfqvYvaQqd6kEII7MRZe6pCkxMzsc?usp=sharing)

## Project Structure

The application imports supporting modules. Keep these files available alongside `app.py`:

```text
data/
|
├──raw
├──cleaned

streamlit/
│
├── app.py
├── database.py
├── queries.py
├── utils.py
│
└── Image/
    └── cart2insight.png
```

| File / Folder | Purpose |
|---|---|
| `app.py` | Main Streamlit application and dashboard navigation |
| `database.py` | SQL Server connection and query execution functions (`check_connection`, `run_query`) |
| `queries.py` | SQL query definitions and functions used to generate report queries |
| `utils.py` | KPI formatting, icons, and chart helper functions |
| `Image/cart2insight.png` | Image displayed on the Project Introduction page |

## Prerequisites

Before running the application, make sure you have:

1. Python installed.
2. Microsoft SQL Server available and accessible from the machine running Streamlit.
3. The Olist dataset loaded into the SQL Server database used by the application. The app identifies the database as `Guviproject` in its introduction page.
4. The SQL Server connection details correctly configured in `database.py`.
5. The supporting Python files and image asset listed above.

## Run the Application

From the project directory, run:

```bash
streamlit run app.py
```

Streamlit will display a local URL in the terminal (usually `http://localhost:8501`). Open that URL in your browser.

## Note
Download the raw dataset and organize it into the appropriate folder structure.

## Using the Dashboard

1. Open **Project Introduction** to view the project overview and data source.
2. Select **Business Overview** to view the main business KPIs and yearly sales.
3. Open **Sales Analysis**, **Customer Analysis**, **Seller & Product Analysis**, **Delivery Analysis**, or **Customer Experience** from the sidebar.
4. Use the purchase-year or selling-year selector where available to filter the report year.
5. Expand **Database connection** in the sidebar and select **Test SQL Server** to check connectivity.

The reports are designed around delivered-order analysis, as indicated by the dashboard descriptions and report labels.

## Summary of Key Findings and Actionable Recommendations

The following findings are based on the Olist dataset analyses performed for this project.

### Key Findings

1. **Customer retention is a major opportunity**
   - 93,099 customers (96.88%) were one-time customers, while only 2,997 (3.12%) made repeat purchases.
   - Repeat customers spent an average of **R$310.49**, compared with **R$161.49** for one-time customers — approximately **1.92 times more**.

2. **Sales increased year over year**
   - Annual sales increased from approximately **R$6.15 million in 2017** to **R$7.38 million in 2018**.
   - The leading revenue-generating categories were **beleza_saude (R$1.25 million)**, **relogios_presentes (R$1.20 million)**, and **cama_mesa_banho (R$1.03 million)**.

3. **Most delivered orders arrived earlier than the estimated date**
   - 88,649 orders (91.89%) were delivered early, while 7,827 orders (8.11%) were delivered late.
   - Review scores generally tended to be higher when orders arrived further ahead of the estimated delivery date.

4. **Customer reviews were generally positive, but some categories need attention**
   - 57.78% of reviews were five-star ratings, while 11.51% were one-star ratings.
   - The `moveis_escritorio` and `telefonia_fixa` categories had relatively lower average ratings and may warrant further investigation.

5. **Seller performance should be assessed using more than order volume**
   - Sao Paulo had the highest seller presence in the analysis, with 1,849 sellers.
   - High order volume does not necessarily mean the highest revenue or strongest customer experience. Revenue, delivery performance, and ratings should be considered together.

### Actionable Recommendations

| Focus area | Recommended action | Expected business benefit |
|---|---|---|
| Customer retention | Introduce targeted repeat-purchase campaigns, loyalty rewards, and personalized offers for one-time customers. | Encourage repeat purchases and increase customer lifetime value. |
| High-performing categories | Review inventory availability and plan targeted promotions for `beleza_saude`, `relogios_presentes`, and `cama_mesa_banho`. | Support revenue growth in categories with strong sales. |
| Delivery performance | Monitor late deliveries by state, seller, and delivery route; investigate recurring causes and work with logistics partners on corrective actions. | Reduce late deliveries and improve customer satisfaction. |
| Low-rated categories | Review product quality, descriptions, packaging, and customer complaints in `moveis_escritorio` and `telefonia_fixa`. | Address potential sources of dissatisfaction and improve ratings. |
| Seller management | Build a seller scorecard using revenue, order count, delivery performance, and review scores rather than ranking sellers by order volume alone. | Identify reliable, high-value sellers and target support where performance is weak. |
| Customer experience | Track one-star reviews and review-score trends alongside delivery outcomes; prioritize recurring complaint themes. | Detect service issues earlier and improve the overall shopping experience. |

These recommendations are intended as business actions suggested by the observed patterns. Their impact should be monitored over time using repeat-purchase rate, revenue, late-delivery rate, and review-score trends.


