import streamlit as st
import pandas as pd
import datetime

# --- 1. KONFIGURASI TEMA CORDUROY ---
st.set_page_config(page_title="Data Stok SMD & IKEA", page_icon="🏭", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #fdfaf6; color: #4b3d33; }
    h1, h2, h3 { color: #8b5e3c !important; }
    div.stButton > button { background-color: #d2b48c; color: white; border: none; border-radius: 6px; font-weight: bold; }
    [data-testid="stSidebar"] { background-color: #f5e9d9; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. URL CSV (PASTIKAN SUDAH PUBLISH TO WEB) ---
URL_PROD = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=0&single=true&output=csv"
URL_DELIV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=955087734&single=true&output=csv"
URL_MASTER = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=1449236361&single=true&output=csv"

# --- 3. FUNGSI AMBIL DATA ---
@st.cache_data(ttl=60)
def load_data(url):
    try:
        # Menambahkan parameter agar lebih toleran terhadap format file
        df = pd.read_csv(url, on_bad_lines='skip', engine='python')
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca CSV: {e}")
        return pd.DataFrame() # Mengembalikan dataframe kosong agar aplikasi tidak mati

# Ambil data
df = load_data(URL_PROD)
df_deliv = load_data(URL_DELIV)
df_master = load_data(URL_MASTER)

# Pastikan Tanggal urut terbaru
if "Tanggal" in df.columns:
    df["Tanggal"] = pd.to_datetime(df["Tanggal"])
    df = df.sort_values(by="Tanggal", ascending=False)

# --- 4. TAMPILAN APLIKASI ---
st.title("🏭 APLIKASI DATA STOK SAMINDO")
menu = st.sidebar.selectbox("Menu", ["🏭 Input Produksi", "📊 Monitoring WIP", "📦 Data Stok", "⚙️ Master Data"])

# --- MENU MASTER DATA ---
if menu == "⚙️ Master Data":
    st.subheader("⚙️ Master Data")
    st.dataframe(df_master, width=1000)

# --- MENU INPUT PRODUKSI ---
elif menu == "🏭 Input Produksi":
    st.subheader("🏭 Form Input")
    with st.form("input_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            tgl = st.date_input("Tanggal", datetime.date.today())
            model = st.selectbox("Model", df_master[df_master.iloc[:,0]=="Model"].iloc[:,1].unique())
        with col2:
            item = st.text_input("Nama/Kode Item")
            proses = st.selectbox("Proses", df_master[df_master.iloc[:,0]=="Proses"].iloc[:,1].unique())
        jumlah = st.number_input("Jumlah OK", min_value=0)
        if st.form_submit_button("Simpan Data"):
            st.warning("Mohon input data langsung di file Google Sheets untuk tersimpan permanen.")

# --- MENU MONITORING WIP ---
elif menu == "📊 Monitoring WIP":
    st.subheader("📊 Monitoring WIP")
    df_wip = df[df["Proses"] != "Cek Point"]
    st.dataframe(df_wip, width=1000)
    st.table(df_wip.groupby("Proses")["Jumlah"].sum())

# --- MENU DATA STOK ---
elif menu == "📦 Data Stok":
    st.subheader("📦 Data Stok")
    pilih_model = st.selectbox("Pilih Model", df_master[df_master.iloc[:,0]=="Model"].iloc[:,1].unique())
    
    # Filter Data
    df_cek = df[(df["Proses"] == "Cek Point") & (df["Model"] == pilih_model)]
    prod_ok = df_cek.groupby("Item")["Jumlah"].sum()
    
    # Ambil kolom Delivery secara dinamis (Model, Item, Jumlah_Out)
    deliv_filtered = df_deliv[df_deliv.iloc[:,0] == pilih_model]
    deliv_out = deliv_filtered.groupby(df_deliv.columns[1])[df_deliv.columns[2]].sum()
    
    stok_final = pd.DataFrame({"Produksi": prod_ok, "Delivery": deliv_out}).fillna(0).astype(int)
    stok_final["Sisa Stok"] = stok_final["Produksi"] - stok_final["Delivery"]
    st.table(stok_final)

# Tombol Refresh
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()
