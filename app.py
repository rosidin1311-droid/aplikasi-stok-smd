import streamlit as st
import pandas as pd

# Konfigurasi Tema Corduroy
st.set_page_config(page_title="Corduroy Tracker", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    h1, h2, h3 { color: #5D4037; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { background-color: #8B4513; color: white; }
    </style>
    """, unsafe_allow_html=True)

# URL dari Google Sheets yang sudah di-Publish to Web (Format CSV)
URL_MASTER = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQiAd_-Ro2vWU5lgw9SnDeaz_Ey5-vJrHjA0mS6XGKUDR80dL47YLgFwRgBOt2nTrSymALKSWKrSQ49/pub?gid=574493740&single=true&output=csv"
URL_STOK = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQiAd_-Ro2vWU5lgw9SnDeaz_Ey5-vJrHjA0mS6XGKUDR80dL47YLgFwRgBOt2nTrSymALKSWKrSQ49/pub?gid=1850383861&single=true&output=csv"
# Tambahkan variabel ini di bagian konfigurasi URL
URL_DELIVERY = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQiAd_-Ro2vWU5lgw9SnDeaz_Ey5-vJrHjA0mS6XGKUDR80dL47YLgFwRgBOt2nTrSymALKSWKrSQ49/pub?gid=1653497651&single=true&output=csv"

# Di dalam menu "🚚 Delivery Plan" pada kode Anda:
elif menu == "🚚 Delivery Plan":
    st.subheader("🚚 Data Pengiriman")
    df_deliv = get_csv(URL_DELIVERY)
    st.dataframe(df_deliv, use_container_width=True)


# Fungsi Load
@st.cache_data(ttl=60)
def get_csv(url):
    return pd.read_csv(url)

st.title("🏭 Corduroy Production Tracker")

# Sidebar Menu
menu = st.sidebar.radio("Menu Utama", ["📊 Dashboard Stok", "🚚 Delivery Plan", "⚙️ Master Data", "➕ Input Produksi"])

if menu == "📊 Dashboard Stok":
    st.subheader("📦 Monitoring Stok Ready")
    df_stok = get_csv(URL_STOK)
    st.dataframe(df_stok, use_container_width=True)
    if st.download_button("📥 Download Stok", df_stok.to_csv(), "stok.csv"):
        st.success("Download Selesai")

elif menu == "🚚 Delivery Plan":
    st.subheader("🚚 Rencana Pengiriman")
    df_deliv = get_csv(URL_DELIVERY)
    st.dataframe(df_deliv, use_container_width=True)

elif menu == "⚙️ Master Data":
    st.subheader("⚙️ Master Data Referensi")
    df_master = get_csv(URL_MASTER)
    st.dataframe(df_master, use_container_width=True)

elif menu == "➕ Input Produksi":
    st.subheader("🏭 Input Produksi")
    st.info("Gunakan form di bawah untuk mencatat produksi agar sinkron dengan database.")
    # Link ke Google Form yang sudah Anda buat
    st.link_button("✍️ Buka Form Input Produksi", "URL_GOOGLE_FORM_ANDA_DI_SINI")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()
