import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- KONEKSI ---
# Kita gunakan cara ini agar tidak bentrok dengan sistem Streamlit
def get_data():
    # Catatan: Karena kita belum pakai JSON key, 
    # untuk tes awal kita pakai cara pembacaan yang lebih sederhana 
    # atau pastikan Google Sheet sudah 'Anyone with the link'
    st.write("Aplikasi sedang berjalan...")
    return pd.DataFrame() # Sementara kosong untuk test

st.title("Aplikasi Stok Samindo")
df = get_data()
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
