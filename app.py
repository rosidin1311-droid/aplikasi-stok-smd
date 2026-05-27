import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Stok Samindo", layout="wide")
st.title("🏭 APLIKASI DATA STOK SAMINDO")

# Masukkan link CSV hasil 'Publish to web' tadi di sini
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?output=csv"

try:
    # Membaca data langsung sebagai tabel
    df = pd.read_csv(CSV_URL)
    st.success("Data berhasil dimuat!")
    st.dataframe(df, width=1000)
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
