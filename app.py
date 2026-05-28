import streamlit as st
import pandas as pd
import datetime

# --- KONFIGURASI ---
st.set_page_config(page_title="App Stok", layout="wide")
st.title("🏭 APLIKASI STOK SAMINDO")

# --- URL CSV ---
URL_PROD = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=0&single=true&output=csv"
URL_DELIV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=955087734&single=true&output=csv"
URL_MASTER = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=1449236361&single=true&output=csv"

@st.cache_data(ttl=60)
def load(url):
    return pd.read_csv(url)

# --- LOAD DATA ---
df_prod = load(URL_PROD)
df_deliv = load(URL_DELIV)
df_master = load(URL_MASTER)

# --- MENU APLIKASI ---
menu = st.sidebar.selectbox("Pilih Menu", ["Monitoring", "Master Data", "Input Produksi"])

if menu == "Monitoring":
    st.subheader("Monitoring Produksi")
    st.dataframe(df_prod)
    
elif menu == "Master Data":
    st.subheader("Data Master")
    st.dataframe(df_master)

elif menu == "Input Produksi":
    st.subheader("Input Produksi")
    with st.form("input_form"):
        # Mengambil daftar dari kolom master (index 1)
        model_list = df_master.iloc[:, 1].unique().tolist()
        model = st.selectbox("Pilih Model", model_list)
        qty = st.number_input("Jumlah", 0)
        if st.form_submit_button("Simpan"):
            st.info("Fitur simpan akan segera diaktifkan. Data saat ini dibaca dari Sheets.")

if st.sidebar.button("🔄 Refresh"):
    st.cache_data.clear()
    st.rerun()
