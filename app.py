import streamlit as st
import pandas as pd

# Cara termudah: Menggunakan link publik
# Ganti LINK_SHEET_ANDA dengan URL Google Sheet Anda
url = "LINK_GOOGLE_SHEET_ANDA"
url = url.replace("/edit#gid=", "/export?format=csv&gid=")

try:
    df = pd.read_csv(url)
    st.write("Data Berhasil Dimuat!")
    st.dataframe(df)
except Exception as e:
    st.write("Belum terkoneksi, pastikan link sudah benar.")
