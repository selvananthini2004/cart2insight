import pyodbc
import pandas as pd
import streamlit as st

def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=Guviproject;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
    )

    return pyodbc.connect(conn_str, timeout=30)

@st.cache_data(ttl=3600)
def run_query(query):
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()


def check_connection():
    with get_connection() as conn:
        return pd.read_sql_query("SELECT DB_NAME() AS database_name, @@SERVERNAME AS server_name", conn).iloc[0]
