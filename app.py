import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# --- KONFIGURASI TEMA CORDUROY ---
st.set_page_config(page_title="Data Stok SMD & IKEA", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #fdfaf6; color: #4b3d33; }
    h1, h2, h3 { color: #8b5e3c !important; }
    div.stButton > button { background-color: #d2b48c; color: #4b3d33; border: none; border-radius: 6px; font-weight: bold; }
    [data-testid="stSidebar"] { background-color: #f5e9d9; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI KONEKSI ---
# Menggunakan cache_resource agar koneksi tidak dibuat ulang setiap saat
@st.cache_resource
def get_connection():
    return st.connection("gsheets", type=GSheetsConnection)

conn = get_connection()

# --- FUNGSI DATA ---
@st.cache_data(ttl=60) # Data di-refresh setiap 60 detik
def load_all_data():
    return {
        "produksi": conn.read(worksheet="produksi", usecols=list(range(5)), ttl=0),
         produksi_df["Tanggal"] = pd.to_datetime(produksi_df["Tanggal"])
         produksi_df = produksi_df.sort_values(by="Tanggal", ascending=False)
    	"delivery": conn.read(worksheet="delivery", usecols=list(range(4)), ttl=0),
        "master": conn.read(worksheet="master_data", usecols=list(range(2)), ttl=0)
    }

data = load_all_data()
df, df_deliv, df_master = data["produksi"], data["delivery"], data["master"]

st.title("🏭 APLIKASI DATA STOK SAMINDO")

# --- NAVIGASI ---
menu = st.sidebar.selectbox("Menu", ["🏭 Input Produksi", "📊 Monitoring WIP", "📦 Data Stok", "⚙️ Master Data"])

# --- MENU MASTER DATA ---
if menu == "⚙️ Master Data":
    st.subheader("⚙️ Kelola Master Data")
    st.dataframe(df_master, use_container_width=True)
    with st.form("tambah_master", clear_on_submit=True):
        kategori = st.selectbox("Kategori", ["Customer", "Model", "Item", "Proses"])
        input_data = st.text_input("Nama Data Baru")
        if st.form_submit_button("Tambah ke Master"):
            new_master = pd.DataFrame([[kategori, input_data]], columns=["Kategori", "Nama_Data"])
            updated_df = pd.concat([df_master, new_master], ignore_index=True)
            conn.update(worksheet="master_data", data=updated_df)
            st.success("Data berhasil ditambahkan! Silakan refresh.")

# --- MENU INPUT PRODUKSI ---
elif menu == "🏭 Input Produksi":
    list_model = df_master[df_master["Kategori"] == "Model"]["Nama_Data"].unique().tolist()
    list_proses = df_master[df_master["Kategori"] == "Proses"]["Nama_Data"].unique().tolist()
    
    with st.form("input_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            tgl = st.date_input("Tanggal", datetime.date.today())
            model = st.selectbox("Pilih Model", list_model)
        with col2:
            item = st.text_input("Nama/Kode Item")
            proses = st.selectbox("Pilih Proses", list_proses)
        jumlah = st.number_input("Jumlah Output OK", min_value=0)
        
        if st.form_submit_button("Simpan Data"):
            new_data = pd.DataFrame([[str(tgl), model, item, proses, jumlah]], 
                                    columns=["Tanggal", "Model", "Item", "Proses", "Jumlah"])
            updated_df = pd.concat([df, new_data], ignore_index=True)
            conn.update(worksheet="produksi", data=updated_df)
            st.success("Data tersimpan!")

# --- MENU MONITORING & STOK ---
elif menu == "📊 Monitoring WIP":
    st.subheader("Monitoring WIP")
    df_wip = df[df["Proses"] != "Cek Point"]
    st.dataframe(df_wip, use_container_width=True)
    st.table(df_wip.groupby("Proses")["Jumlah"].sum())

elif menu == "📦 Data Stok":
    pilih_model = st.selectbox("Pilih Model", df_master[df_master["Kategori"] == "Model"]["Nama_Data"].unique().tolist())
    df_cek = df[(df["Proses"] == "Cek Point") & (df["Model"] == pilih_model)]
    prod_ok = df_cek.groupby("Item")["Jumlah"].sum()
    deliv_out = df_deliv[df_deliv["Model"] == pilih_model].groupby("Item")["Jumlah_Out"].sum()
    stok_final = pd.DataFrame({"Produksi": prod_ok, "Delivery": deliv_out}).fillna(0).astype(int)
    stok_final["Sisa Stok"] = stok_final["Produksi"] - stok_final["Delivery"]
    st.table(stok_final)
