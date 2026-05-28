import streamlit as st
import pandas as pd

# --- TEMA & CONFIG ---
st.set_page_config(page_title="Data Stok SMD", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #fdfaf6; color: #4b3d33; }
    h1 { color: #8b5e3c; }
    [data-testid="stSidebar"] { background-color: #f5e9d9; }
    </style>
    """, unsafe_allow_html=True)

# --- URL CSV ---
URLS = {
    "PROD": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=0&single=true&output=csv",
    "DELIV": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=955087734&single=true&output=csv",
    "MASTER": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=1449236361&single=true&output=csv"
}

@st.cache_data(ttl=60)
def load(url):
    return pd.read_csv(url)

df = load(URLS["PROD"])
df_deliv = load(URLS["DELIV"])
df_master = load(URLS["MASTER"])

menu = st.sidebar.selectbox("Menu", ["🏭 Input Produksi", "📦 Data Stok", "⚙️ Master Data"])

# --- MENU MASTER ---
if menu == "⚙️ Master Data":
    st.subheader("⚙️ Master Data")
    st.dataframe(df_master, use_container_width=True)

# --- MENU INPUT ---
elif menu == "🏭 Input Produksi":
    st.subheader("🏭 Input Produksi")
    # Memastikan kolom pertama berisi 'Model' dan 'Proses'
    model_list = df_master[df_master.iloc[:,0] == "Model"].iloc[:,1].dropna().unique()
    proses_list = df_master[df_master.iloc[:,0] == "Proses"].iloc[:,1].dropna().unique()
    
    with st.form("input"):
        m = st.selectbox("Pilih Model", model_list)
        p = st.selectbox("Pilih Proses", proses_list)
        item = st.text_input("Nama Item")
        qty = st.number_input("Jumlah OK", 0)
        if st.form_submit_button("Simpan"):
            st.info("Data siap disinkronisasi.")

# --- MENU DATA STOK (FIXED) ---
elif menu == "📦 Data Stok":
    st.subheader("📦 Data Stok (Barang Selesai Proses)")
    # Mengambil list model dari data produksi
    model_list = df.iloc[:, 1].dropna().unique()
    pilih_m = st.selectbox("Pilih Model untuk Cek Stok", model_list)
    
    # Logika: Ambil baris dimana Model == pilih_m DAN Proses == 'Cek Point' (atau kolom proses di index 3)
    # Sesuaikan angka 3 dengan kolom 'Proses' di file produksi Anda
    stok_df = df[(df.iloc[:, 1] == pilih_m) & (df.iloc[:, 3] == "Cek Point")]
    
    if not stok_df.empty:
        # Menampilkan tabel hasil produksi yang sudah di 'Cek Point'
        st.table(stok_df)
    else:
        st.warning("Belum ada data produksi yang selesai (Cek Point) untuk model ini.")

if st.sidebar.button("🔄 Refresh"):
    st.rerun()
