import streamlit as st
import pandas as pd
from google.oauth2.service_account import Credentials
import gspread

# Konfigurasi Page
st.set_page_config(page_title="Data Stok Samindo", layout="wide")

st.title("🏭 APLIKASI DATA STOK SAMINDO")
st.write("Sistem siap digunakan.")

# Kita gunakan fungsi sederhana untuk tes koneksi
try:
    # Jika Anda ingin akses publik tanpa JSON Key, 
    # Anda bisa menggunakan library 'gspread' dengan akses link
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    sh = gc.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
    worksheet = sh.worksheet("produksi")
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    st.success("Data berhasil dimuat dari Google Sheets!")
    st.dataframe(df)
except Exception as e:
    st.info("Menunggu data... Pastikan Secrets sudah diatur dengan benar.")
