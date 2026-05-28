import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Aplikasi Data Stok", layout="wide", page_icon="🏭")

# Styling CSS yang lebih rapi
st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    .main .block-container { padding-top: 2rem; }
    h1, h2 { color: #5D4037; }
    div.stButton > button { background-color: #8B4513; color: white; width: 100%; border-radius: 8px; }
    .stDataFrame { border: 1px solid #D2B48C; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# URL Data (Tetap)
URL_MASTER = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQiAd_-Ro2vWU5lgw9SnDeaz_Ey5-vJrHjA0mS6XGKUDR80dL47YLgFwRgBOt2nTrSymALKSWKrSQ49/pub?gid=574493740&single=true&output=csv"
URL_STOK = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQiAd_-Ro2vWU5lgw9SnDeaz_Ey5-vJrHjA0mS6XGKUDR80dL47YLgFwRgBOt2nTrSymALKSWKrSQ49/pub?gid=1850383861&single=true&output=csv"
URL_DELIVERY = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQiAd_-Ro2vWU5lgw9SnDeaz_Ey5-vJrHjA0mS6XGKUDR80dL47YLgFwRgBOt2nTrSymALKSWKrSQ49/pub?gid=1653497651&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data(url):
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2716/2716057.png", width=80)
    st.title("Corduroy System")
    menu = st.radio("Navigasi", ["📊 Dashboard", "🚚 Delivery", "⚙️ Master Data", "➕ Input Produksi", "📤 Input Delivery"])
    st.markdown("---")
    if st.button("🔄 Refresh Data"):
        st.rerun()

# --- MAIN CONTENT ---
if menu == "📊 Dashboard":
    st.title("📊 Dashboard Stok")
    df_stok = load_data(URL_STOK)
    
    if not df_stok.empty:
        # Contoh Ringkasan (Opsional: sesuaikan dengan nama kolom Anda)
        col1, col2 = st.columns(2)
        col1.metric("Total SKU", len(df_stok))
        col2.metric("Status", "Up to Date")
        
        st.dataframe(df_stok, width=none)
        csv = df_stok.to_csv(index=False)
        st.download_button("📥 Download Laporan Stok", csv, "laporan_stok.csv")
    else:
        st.warning("Data Stok belum tersedia.")

elif menu == "🚚 Delivery":
    st.title("🚚 Delivery Plan")
    df_deliv = load_data(URL_DELIVERY)
    if not df_deliv.empty:
        st.dataframe(df_deliv, width=none)
    else:
        st.info("Belum ada data pengiriman.")

elif menu == "⚙️ Master Data":
    st.title("⚙️ Master Data")
    df_master = load_data(URL_MASTER)
    st.dataframe(df_master, width=none)

elif "Input" in menu:
    st.title(f"{menu}")
    link = "https://docs.google.com/forms/d/e/1FAIpQLScl4iEwLtHHDIsbqqRnhgxlwg90-10HjQEQwEf4FQp8nL7eMg/viewform" if "Produksi" in menu else "https://docs.google.com/forms/d/e/1FAIpQLSf_F65fJlF9vkcquLgQvjUhJ2Yprbb9WvmF896UtTE5IZXbMg/viewform"
    
    st.markdown(f"Silakan klik tombol di bawah untuk mengisi data melalui Google Form:")
    st.link_button("✍️ Buka Form Input", link, type="primary")
