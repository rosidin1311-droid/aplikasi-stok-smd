import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Corduroy Production Tracker", layout="wide", page_icon="🏭")

# Styling CSS agar tampilannya lebih "Premium"
st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    div[data-testid="stSidebar"] { background-color: #FAFAFA; border-right: 1px solid #E0E0E0; }
    h1 { color: #5D4037; }
    .stButton>button { border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# URL Data
URL_MASTER = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQiAd_-Ro2vWU5lgw9SnDeaz_Ey5-vJrHjA0mS6XGKUDR80dL47YLgFwRgBOt2nTrSymALKSWKrSQ49/pub?gid=574493740&single=true&output=csv"
URL_STOK = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQiAd_-Ro2vWU5lgw9SnDeaz_Ey5-vJrHjA0mS6XGKUDR80dL47YLgFwRgBOt2nTrSymALKSWKrSQ49/pub?gid=1850383861&single=true&output=csv"
URL_DELIVERY = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQiAd_-Ro2vWU5lgw9SnDeaz_Ey5-vJrHjA0mS6XGKUDR80dL47YLgFwRgBOt2nTrSymALKSWKrSQ49/pub?gid=1653497651&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data(url):
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

# --- SIDEBAR PROFESIONAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2716/2716057.png", width=60)
    st.markdown("### **Corduroy System**")
    st.caption("Aplikasi Data Stok Tae Won")
    st.divider()
    
    # Navigasi Modern
    menu = st.segmented_control(
        "Menu Utama",
        options=["📊 Dashboard", "🚚 Delivery", "⚙️ Master Data", "➕ Input Produksi", "📤 Input Delivery"],
        selection_mode="single",
        default="📊 Dashboard",
        label_visibility="collapsed"
    )
    
    st.divider()
    st.info("Status: Live (Google Sheets)")
    st.markdown("© 2026 Tae Won Production")

# --- MAIN CONTENT ---
# Header bar di bagian atas konten utama
col_title, col_refresh = st.columns([0.8, 0.2])
with col_title:
    st.title(menu)
with col_refresh:
    st.write("") # Spacer
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

st.divider()

# Logika Konten
if menu == "📊 Dashboard":
    df_stok = load_data(URL_STOK)
    if not df_stok.empty:
        st.dataframe(df_stok, width=1000)
        csv = df_stok.to_csv(index=False)
        st.download_button("📥 Download Laporan", csv, "laporan_stok.csv")
    else:
        st.warning("Data belum tersedia.")

elif menu == "🚚 Delivery":
    df_deliv = load_data(URL_DELIVERY)
    if not df_deliv.empty:
        st.dataframe(df_deliv, width=1000)
    else:
        st.info("Belum ada data pengiriman.")

elif menu == "⚙️ Master Data":
    df_master = load_data(URL_MASTER)
    st.dataframe(df_master, width=1000)

elif "Input" in menu:
    link = "https://docs.google.com/forms/d/e/1FAIpQLScl4iEwLtHHDIsbqqRnhgxlwg90-10HjQEQwEf4FQp8nL7eMg/viewform" if "Produksi" in menu else "https://docs.google.com/forms/d/e/1FAIpQLSf_F65fJlF9vkcquLgQvjUhJ2Yprbb9WvmF896UtTE5IZXbMg/viewform"
    st.info(f"Silakan lengkapi form {menu.replace('➕', '').replace('📤', '')} pada link berikut:")
    st.link_button("✍️ Buka Google Form", link, type="primary")
