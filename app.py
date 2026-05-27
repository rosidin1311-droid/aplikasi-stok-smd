import streamlit as st
import pandas as pd

# Cara termudah: Menggunakan link publik
# Ganti LINK_SHEET_ANDA dengan URL Google Sheet Anda
url = "https://docs.google.com/spreadsheets/d/1fUlZzcHCHNgUYDwgvgcrn2e5B46HuWiREMIvQ_G1o28/edit?gid=0#gid=0"
url = url.replace("/edit#gid=", "/export?format=csv&gid=")

try:
    df = pd.read_csv(url)
    st.write("Data Berhasil Dimuat!")
    st.dataframe(df)
except Exception as e:
    st.write("Belum terkoneksi, pastikan link sudah benar.")
