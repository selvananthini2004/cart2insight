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
Raw data  - [Click here to download data](https://drive.google.com/drive/folders/15T53qM0tcIsSs3REAcrDqdHzQ5wif6lc)

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
