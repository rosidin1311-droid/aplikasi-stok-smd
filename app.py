import streamlit as st
import pandas as pd
import datetime

# --- KONFIGURASI ---
st.set_page_config(page_title="Data Stok Samindo", layout="wide")

# Ganti URL ini dengan link "Publish to web" (CSV) dari Google Sheets Anda
# 1. Buka Sheet > File > Share > Publish to web
# 2. Pilih format: "Comma-separated values (.csv)"
# 3. Copy link yang muncul
URL_PRODUKSI = "https://docs.google.com/spreadsheets/d/1fUlZzcHCHNgUYDwgvgcrn2e5B46HuWiREMIvQ_G1o28/edit?gid=0#gid=0"
URL_DELIVERY = "https://docs.google.com/spreadsheets/d/1fUlZzcHCHNgUYDwgvgcrn2e5B46HuWiREMIvQ_G1o28/edit?gid=955087734#gid=955087734"
URL_MASTER = "https://docs.google.com/spreadsheets/d/1fUlZzcHCHNgUYDwgvgcrn2e5B46HuWiREMIvQ_G1o28/edit?gid=1449236361#gid=1449236361"

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
