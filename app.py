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

# --- KONEKSI ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FUNGSI AMBIL DATA ---
def get_data(ws): return conn.read(worksheet=ws, ttl=0)

df = get_data("produksi")
df_deliv = get_data("delivery")
df_master = get_data("master_data")

st.title("🏭 APLIKASI DATA STOK SAMINDO")

# --- NAVIGASI ---
menu = st.sidebar.selectbox("Menu", ["🏭 Input Produksi", "📊 Monitoring WIP", "📦 Data Stok", "⚙️ Master Data"])

# --- MENU MASTER DATA ---
if menu == "⚙️ Master Data":
    st.subheader("⚙️ Kelola Master Data")
    st.dataframe(df_master, use_container_width=True)
    with st.form("tambah_master"):
        kategori = st.selectbox("Kategori", ["Customer", "Model", "Item", "Proses"])
        input_data = st.text_input("Nama Data Baru")
        if st.form_submit_button("Tambah ke Master"):
            new_master = pd.DataFrame([[kategori, input_data]], columns=["Kategori", "Nama_Data"])
            conn.update(worksheet="master_data", data=pd.concat([df_master, new_master], ignore_index=True))
            st.success("Data berhasil ditambahkan! Silakan refresh.")

# --- MENU INPUT PRODUKSI ---
elif menu == "🏭 Input Produksi":
    # Mengambil pilihan dinamis dari Master Data
    list_model = df_master[df_master["Kategori"] == "Model"]["Nama_Data"].tolist()
    list_proses = df_master[df_master["Kategori"] == "Proses"]["Nama_Data"].tolist()
    
    with st.form("input_form"):
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
            conn.update(worksheet="produksi", data=pd.concat([df, new_data], ignore_index=True))
            st.success("Data tersimpan!")

# --- MENU WIP & STOK ---
elif menu == "📊 Monitoring WIP":
    st.subheader("Monitoring WIP")
    df_wip = df[df["Proses"] != "Cek Point"]
    st.dataframe(df_wip, width='stretch')
    st.table(df_wip.groupby("Proses")["Jumlah"].sum())

elif menu == "📦 Data Stok":
    pilih_model = st.selectbox("Pilih Model", df_master[df_master["Kategori"] == "Model"]["Nama_Data"].tolist())
    df_cek = df[(df["Proses"] == "Cek Point") & (df["Model"] == pilih_model)]
    prod_ok = df_cek.groupby("Item")["Jumlah"].sum()
    deliv_out = df_deliv[df_deliv["Model"] == pilih_model].groupby("Item")["Jumlah_Out"].sum()
    stok_final = pd.DataFrame({"Produksi": prod_ok, "Delivery": deliv_out}).fillna(0).astype(int)
    stok_final["Sisa Stok"] = stok_final["Produksi"] - stok_final["Delivery"]
    st.table(stok_final)
