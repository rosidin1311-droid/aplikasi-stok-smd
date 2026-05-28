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

# --- 2. URL CSV (GANTI DENGAN LINK PUBLISH TO WEB ANDA) ---
URL_PROD = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?output=csv"
URL_DELIV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?output=csv"
URL_MASTER = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?output=csv"

# --- FUNGSI AMBIL DATA (DITAMBAH DEBUG) ---
@st.cache_data(ttl=60)
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip() # Menghapus spasi di awal/akhir nama kolom
    return df

df = load_data(URL_PROD)
df_deliv = load_data(URL_DELIV)
df_master = load_data(URL_MASTER)

# --- DEBUG: TAMPILKAN KOLOM ---
# Hapus tanda pagar (#) di bawah ini jika ingin melihat nama kolom yang terbaca di layar
# st.write("Kolom Delivery terbaca:", df_deliv.columns.tolist())

# --- 4. SIDEBAR NAVIGASI ---
st.sidebar.title("NAVIGASI")
menu = st.sidebar.selectbox("Pilih Menu", ["🏭 Input Produksi", "📊 Monitoring WIP", "📦 Data Stok", "⚙️ Master Data"])

st.title("🏭 APLIKASI DATA STOK SAMINDO")
st.divider()

# --- 5. LOGIKA MENU ---
if menu == "⚙️ Master Data":
    st.subheader("⚙️ Master Data")
    st.dataframe(df_master, width='stretch')

# --- 6. LOGIKA MENU INPUT PRODUKSI (DIPERBAIKI) ---
elif menu == "🏭 Input Produksi":
    st.subheader("🏭 Form Input Hasil Produksi")
    
    # Cek apakah kolom yang dibutuhkan ada
    if "Kategori" in df_master.columns and "Nama_Data" in df_master.columns:
        list_model = df_master[df_master["Kategori"] == "Model"]["Nama_Data"].unique().tolist()
        list_proses = df_master[df_master["Kategori"] == "Proses"]["Nama_Data"].unique().tolist()
    else:
        list_model = []
        list_proses = []
        

    with st.form("input_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            tgl = st.date_input("Tanggal", datetime.date.today())
            model = st.selectbox("Model", list_model)
        with col2:
            item = st.text_input("Nama/Kode Item")
            proses = st.selectbox("Proses", list_proses)
        jumlah = st.number_input("Jumlah OK", min_value=0)
        
        # INI TOMBOL SUBMIT YANG TADI KURANG
        submit = st.form_submit_button("Simpan Data")
        
        if submit:
            st.warning("Karena menggunakan CSV, harap input data langsung di Google Sheets Anda.")

elif menu == "📊 Monitoring WIP":
    st.subheader("📊 Monitoring WIP")
    df_wip = df[df["Proses"] != "Cek Point"]
    st.dataframe(df_wip, width='stretch')
    st.table(df_wip.groupby("Proses")["Jumlah"].sum())

elif menu == "📦 Data Stok":
    st.subheader("📦 Data Stok")
    
    # Mengambil nama kolom secara dinamis (index 0=Model, 1=Item, 2=Jumlah_Out)
    col_model_deliv = df_deliv.columns[0]
    col_item_deliv = df_deliv.columns[1]
    col_qty_deliv = df_deliv.columns[2] # Kolom ke-3 yang tadi error
    
    col_kat = df_master.columns[0]
    col_val = df_master.columns[1]
    
    pilih_model = st.selectbox("Pilih Model", df_master[df_master[col_kat]=="Model"][col_val].unique())
    
    # Hitung Produksi
    df_cek = df[(df["Proses"] == "Cek Point") & (df["Model"] == pilih_model)]
    prod_ok = df_cek.groupby("Item")["Jumlah"].sum()
    
    # Hitung Delivery (Menggunakan kolom dinamis)
    deliv_filtered = df_deliv[df_deliv[col_model_deliv] == pilih_model]
    deliv_out = deliv_filtered.groupby(col_item_deliv)[col_qty_deliv].sum()
    
    stok_final = pd.DataFrame({"Produksi": prod_ok, "Delivery": deliv_out}).fillna(0).astype(int)
    stok_final["Sisa Stok"] = stok_final["Produksi"] - stok_final["Delivery"]
    st.table(stok_final)

# --- TOMBOL REFRESH ---
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()
