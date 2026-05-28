import streamlit as st
import pandas as pd
import datetime

# --- KONFIGURASI TEMA ---
st.set_page_config(page_title="Data Stok SMD", page_icon="🏭", layout="wide")

# --- URL CSV ---
URL_PROD = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=0&single=true&output=csv"
URL_DELIV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=955087734&single=true&output=csv"
URL_MASTER = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=1449236361&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = load_data(URL_PROD)
df_deliv = load_data(URL_DELIV)
df_master = load_data(URL_MASTER)

# --- FUNGSI NAVIGASI ---
st.title("🏭 APLIKASI DATA STOK SAMINDO")
menu = st.sidebar.selectbox("Menu", ["🏭 Input Produksi", "📊 Monitoring WIP", "📦 Data Stok", "⚙️ Master Data"])

# --- MENU MASTER ---
if menu == "⚙️ Master Data":
    st.dataframe(df_master)

# --- MENU INPUT ---
elif menu == "🏭 Input Produksi":
    # Mengambil unik data dari kolom 1 (Kategori) dan kolom 2 (Nama)
    kategori_col = df_master.columns[0]
    data_col = df_master.columns[1]
    
    models = df_master[df_master[kategori_col] == "Model"][data_col].unique().tolist()
    proses = df_master[df_master[kategori_col] == "Proses"][data_col].unique().tolist()
    
    with st.form("input"):
        m = st.selectbox("Model", models)
        p = st.selectbox("Proses", proses)
        qty = st.number_input("Jumlah", 0)
        if st.form_submit_button("Simpan"):
            st.warning("Input langsung ke Google Sheets saja.")

# --- MENU STOK ---
elif menu == "📦 Data Stok":
    # Asumsi kolom: 0=Model, 1=Item, 2=Jumlah
    m_col, i_col, q_col = df.columns[1], df.columns[2], df.columns[4]
    d_col, dq_col = df_deliv.columns[0], df_deliv.columns[2]
    
    pilih_m = st.selectbox("Pilih Model", df[m_col].unique())
    
    # Hitung
    prod = df[df[m_col] == pilih_m].groupby(i_col)[q_col].sum()
    deliv = df_deliv[df_deliv[d_col] == pilih_m].groupby(df_deliv.columns[1])[dq_col].sum()
    
    res = pd.DataFrame({"Produksi": prod, "Delivery": deliv}).fillna(0)
    res["Sisa"] = res["Produksi"] - res["Delivery"]
    st.table(res)

if st.sidebar.button("🔄 Refresh"):
    st.cache_data.clear()
    st.rerun()
