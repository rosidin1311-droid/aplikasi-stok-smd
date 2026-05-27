import subprocess
import sys

# Memastikan gspread terinstall
subprocess.check_call([sys.executable, "-m", "pip", "install", "gspread", "pandas"])

import streamlit as st
import pandas as pd
import gspread

# Konfigurasi Halaman
st.set_page_config(page_title="Data Stok SMD", layout="wide")

# Koneksi
conn = st.connection("gsheets", type=GSheetsConnection)

# Ambil Data
try:
    df = conn.read(worksheet="produksi", ttl=0)
    st.title("Aplikasi Stok Samindo")
    st.write("Data berhasil dimuat!")
    st.dataframe(df)
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
