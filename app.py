import streamlit as st
import pandas as pd

st.set_page_config(page_title="App Stok", layout="wide")
st.title("🏭 APLIKASI STOK SAMINDO - MODE DEBUG")

# URL yang Anda berikan
URL_PROD = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=0&single=true&output=csv"
URL_DELIV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=955087734&single=true&output=csv"
URL_MASTER = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=1449236361&single=true&output=csv"

@st.cache_data(ttl=60)
def load(url):
    return pd.read_csv(url)

try:
    df_prod = load(URL_PROD)
    df_deliv = load(URL_DELIV)
    df_master = load(URL_MASTER)

    menu = st.sidebar.selectbox("Pilih Menu", ["Lihat Master", "Lihat Produksi"])

    if menu == "Lihat Master":
        st.write("Data Master Terbaca:")
        st.dataframe(df_master)
    else:
        st.write("Data Produksi Terbaca:")
        st.dataframe(df_prod)

except Exception as e:
    st.error(f"Error: {e}")
