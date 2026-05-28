import streamlit as st
import pandas as pd
import datetime

# --- KONFIGURASI ---
st.set_page_config(page_title="Data Stok Samindo", layout="wide")

# Ganti URL ini dengan link "Publish to web" (CSV) dari Google Sheets Anda
# 1. Buka Sheet > File > Share > Publish to web
# 2. Pilih format: "Comma-separated values (.csv)"
# 3. Copy link yang muncul
URL_PRODUKSI = "LINK_CSV_PRODUKSI_ANDA"
URL_DELIVERY = "LINK_CSV_DELIVERY_ANDA"
URL_MASTER = "LINK_CSV_MASTER_ANDA"

# --- FUNGSI DATA ---
@st.cache_data(ttl=60)
def load_data(url):
    df = pd.read_csv(url)
    return df

# Memuat data
df = load_data(URL_PRODUKSI)
df_deliv = load_data(URL_DELIVERY)
df_master = load_data(URL_MASTER)

# --- TAMPILAN ---
st.title("🏭 APLIKASI DATA STOK SAMINDO")
menu = st.sidebar.selectbox("Menu", ["📊 Monitoring WIP", "📦 Data Stok"])

if menu == "📊 Monitoring WIP":
    st.dataframe(df)
elif menu == "📦 Data Stok":
    st.table(df.groupby("Model")["Jumlah"].sum())
