import streamlit as st
import pandas as pd

# Konfigurasi Halaman & Tema Corduroy
st.set_page_config(page_title="Corduroy Production Tracker", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    h1, h2, h3 { color: #5D4037; font-family: sans-serif; }
    .stButton>button { background-color: #8B4513; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# GANTI LINK DI BAWAH DENGAN LINK HASIL "PUBLISH TO WEB" DARI GOOGLE SHEET ANDA
URL_MASTER = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQiAd_-Ro2vWU5lgw9SnDeaz_Ey5-vJrHjA0mS6XGKUDR80dL47YLgFwRgBOt2nTrSymALKSWKrSQ49/pub?gid=574493740&single=true&output=csv"
URL_STOK = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQiAd_-Ro2vWU5lgw9SnDeaz_Ey5-vJrHjA0mS6XGKUDR80dL47YLgFwRgBOt2nTrSymALKSWKrSQ49/pub?gid=1850383861&single=true&output=csv"
URL_DELIVERY = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQiAd_-Ro2vWU5lgw9SnDeaz_Ey5-vJrHjA0mS6XGKUDR80dL47YLgFwRgBOt2nTrSymALKSWKrSQ49/pub?gid=1653497651&single=true&output=csv"

# Fungsi untuk memuat data dengan Error Handling
@st.cache_data(ttl=60)
def load_data(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Gagal memuat data. Pastikan link sudah benar dan sudah di-Publish to Web. Error: {e}")
        return pd.DataFrame()

st.title("🏭 Corduroy Production Tracker")

# Sidebar Menu
menu = st.sidebar.radio("Menu Utama", ["📊 Dashboard Stok", "🚚 Delivery Plan", "⚙️ Master Data", "➕ Input Produksi", "📤 Input Delivery"])

# Logika Navigasi
if menu == "📊 Dashboard Stok":
    st.subheader("📦 Monitoring Stok Ready")
    df_stok = load_data(URL_STOK)
    if not df_stok.empty:
        st.dataframe(df_stok, width='stretch')
        csv = df_stok.to_csv(index=False)
        st.download_button("📥 Download Laporan Stok", csv, "laporan_stok.csv")
    else:
        st.warning("Data Stok belum tersedia.")

elif menu == "🚚 Delivery Plan":
    st.subheader("🚚 Data Pengiriman")
    df_deliv = load_data(URL_DELIVERY)
    if not df_deliv.empty:
        st.dataframe(df_deliv, width='stretch')
    else:
        st.info("Belum ada data pengiriman.")

elif menu == "⚙️ Master Data":
    st.subheader("⚙️ Master Data Referensi")
    df_master = load_data(URL_MASTER)
    st.dataframe(df_master, width='stretch')

elif menu == "➕ Input Produksi":
    st.subheader("🏭 Input Produksi")
    st.info("Gunakan form di bawah untuk mencatat hasil produksi harian.")
    st.link_button("✍️ Buka Form Input Produksi", "https://docs.google.com/forms/d/e/1FAIpQLScl4iEwLtHHDIsbqqRnhgxlwg90-10HjQEQwEf4FQp8nL7eMg/viewform")

elif menu == "📤 Input Delivery":
    st.subheader("📤 Input Delivery")
    st.info("Gunakan form di bawah untuk mencatat pengiriman barang.")
    st.link_button("✍️ Buka Form Input Delivery", "https://docs.google.com/forms/d/e/1FAIpQLSf_F65fJlF9vkcquLgQvjUhJ2Yprbb9WvmF896UtTE5IZXbMg/viewform")

# Tombol Refresh
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()
