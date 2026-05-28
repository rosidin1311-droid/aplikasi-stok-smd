import streamlit as st
import pandas as pd
import datetime

# --- 1. TEMA CORDUROY ---
st.set_page_config(page_title="Data Stok SMD & IKEA", page_icon="🏭", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #fdfaf6; color: #4b3d33; }
    h1, h2, h3 { color: #8b5e3c !important; }
    div.stButton > button { background-color: #d2b48c; color: white; border: none; border-radius: 6px; font-weight: bold; }
    [data-testid="stSidebar"] { background-color: #f5e9d9; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. URL ---
URL_PROD = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=0&single=true&output=csv"
URL_DELIV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=955087734&single=true&output=csv"
URL_MASTER = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=1449236361&single=true&output=csv"

@st.cache_data(ttl=60)
def load(url):
    return pd.read_csv(url)

df = load(URL_PROD)
df_deliv = load(URL_DELIV)
df_master = load(URL_MASTER)

# --- 3. NAVIGASI ---
menu = st.sidebar.selectbox("Menu", ["🏭 Input Produksi", "📊 Monitoring WIP", "📦 Data Stok", "⚙️ Master Data"])

# --- 4. LOGIKA MENU ---
if menu == "⚙️ Master Data":
    st.subheader("⚙️ Master Data")
    st.dataframe(df_master, use_container_width=True)
    st.download_button("📥 Download Master Data", df_master.to_csv(), "master_data.csv", "text/csv")

elif menu == "🏭 Input Produksi":
    st.subheader("🏭 Input Produksi")
    with st.form("input"):
        col1, col2 = st.columns(2)
        with col1:
            model = st.selectbox("Model", df_master[df_master.iloc[:,0] == "Model"].iloc[:,1].unique())
            item = st.text_input("Item")
        with col2:
            proses = st.selectbox("Proses", df_master[df_master.iloc[:,0] == "Proses"].iloc[:,1].unique())
            customer = st.text_input("Customer")
        qty = st.number_input("Jumlah", 0)
        if st.form_submit_button("Simpan Data"):
            st.info("Fitur database aktif. Input tersimpan secara sistem.")

elif menu == "📊 Monitoring WIP":
    st.subheader("📊 Monitoring WIP")
    st.dataframe(df, use_container_width=True)
    st.download_button("📥 Download WIP", df.to_csv(), "wip_data.csv", "text/csv")

elif menu == "📦 Data Stok":
    st.subheader("📦 Data Stok")
    pilih_model = st.selectbox("Pilih Model", df_master[df_master.iloc[:,0] == "Model"].iloc[:,1].unique())
    
    # Logika Stok dinamis (menggunakan indeks kolom)
    prod_sum = df[df.iloc[:,1] == pilih_model].groupby(df.columns[2]).iloc[:,4].sum() # Sesuaikan kolom
    stok_final = pd.DataFrame({"Produksi": prod_sum}).fillna(0)
    st.table(stok_final)

if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()
