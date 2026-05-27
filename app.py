import streamlit as st
import pandas as pd
import os
import datetime

# --- TEMA PROFESSIONAL LIGHT ---
st.markdown("""
    <style>
    /* Background krem lembut (Corduroy style) */
    .stApp {
        background-color: #fdfaf6;
        color: #4b3d33; /* Warna teks cokelat gelap agar nyaman dibaca */
    }
    
    /* Judul dengan warna cokelat tua yang elegan */
    h1, h2, h3 {
        color: #8b5e3c !important; 
    }
    
    /* Tombol warna Senada (Soft Brown) */
    div.stButton > button {
        background-color: #d2b48c;
        color: #4b3d33;
        border: none;
        border-radius: 6px;
        font-weight: bold;
    }
    
    /* Tabel dengan aksen cokelat lembut */
    .stDataFrame, .stTable {
        background-color: #ffffff !important;
        border: 1px solid #d2b48c !important;
    }
    
    /* Sidebar warna cokelat susu/beige */
    [data-testid="stSidebar"] {
        background-color: #f5e9d9;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SETTING LAYOUT ---
st.set_page_config(page_title="Data Stok SMD & IKEA", layout="wide")

DATA_FILE = "data_produksi.csv"
DELIVERY_FILE = "data_delivery.csv"

# Fungsi Inisialisasi
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["Tanggal", "Model", "Item", "Proses", "Jumlah"]).to_csv(DATA_FILE, index=False)
if not os.path.exists(DELIVERY_FILE):
    pd.DataFrame(columns=["Tanggal", "Model", "Item", "Jumlah_Out"]).to_csv(DELIVERY_FILE, index=False)

df = pd.read_csv(DATA_FILE)
df_deliv = pd.read_csv(DELIVERY_FILE)

# --- SIDEBAR ---
st.sidebar.title("Navigasi")
menu = st.sidebar.selectbox("Menu", ["🏭 Input Produksi", "📊 Monitoring WIP", "📦 Data Stok"])
st.sidebar.markdown("---")
st.sidebar.info("Aplikasi Data Stok SMD & IKEA - Versi 1.0")

st.title("🏭 APLIKASI DATA STOK SMD & IKEA")

# --- INPUT PRODUKSI ---
if menu == "🏭 Input Produksi":
    with st.form("input_form"):
        col1, col2 = st.columns(2)
        with col1:
            tgl = st.date_input("Tanggal Produksi", datetime.date.today())
            model = st.selectbox("Pilih Model", ["Master Box (MB)", "Gift Box (GB)", "Pad"])
        with col2:
            item = st.text_input("Nama/Kode Item")
            proses = st.selectbox("Proses", ["Flexo", "Diecut", "Kopek", "Lem Auto", "Cek Point"])
        
        jumlah = st.number_input("Jumlah Output OK", min_value=0)
        
        if st.form_submit_button("Simpan Data"):
            new_data = pd.DataFrame([[tgl, model, item, proses, jumlah]], columns=["Tanggal", "Model", "Item", "Proses", "Jumlah"])
            new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
            st.success(f"Data {item} tersimpan!")

# --- DATA WIP ---
elif menu == "📊 Monitoring WIP":
    st.subheader("Monitoring WIP (Work In Progress)")
    df_wip = df[df["Proses"] != "Cek Point"]
    st.dataframe(df_wip, use_container_width=True)
    
    st.subheader("Ringkasan Total WIP per Proses")
    ringkasan_wip = df_wip.groupby(["Proses"])["Jumlah"].sum()
    st.table(ringkasan_wip)
    
    if st.button("Hapus Data WIP Terakhir"):
        df = df[:-1]
        df.to_csv(DATA_FILE, index=False)
        st.warning("Data terakhir dihapus! Refresh halaman.")
    
    csv_wip = df_wip.to_csv(index=False).encode('utf-8')
    st.download_button("Download Laporan WIP ke Excel", csv_wip, "Laporan_WIP.csv", "text/csv")

# --- DATA STOK ---
elif menu == "📦 Data Stok":
    st.subheader("Ringkasan Stok")
    pilih_model = st.selectbox("Pilih Model untuk Dilihat", ["Master Box (MB)", "Gift Box (GB)", "Pad"])
    
    df_cek = df[(df["Proses"] == "Cek Point") & (df["Model"] == pilih_model)]
    prod_ok = df_cek.groupby("Item")["Jumlah"].sum()
    deliv_out = df_deliv[df_deliv["Model"] == pilih_model].groupby("Item")["Jumlah_Out"].sum()
    
    stok_final = pd.DataFrame({"Produksi": prod_ok, "Delivery": deliv_out}).fillna(0).astype(int)
    stok_final["Sisa Stok"] = stok_final["Produksi"] - stok_final["Delivery"]
    
    total_stok = stok_final["Sisa Stok"].sum()
    st.metric("Total Sisa Stok", total_stok)
    
    st.table(stok_final)
    
    if st.button("Hapus Data Delivery Terakhir"):
        df_deliv = df_deliv[:-1]
        df_deliv.to_csv(DELIVERY_FILE, index=False)
        st.warning("Data delivery terakhir dihapus! Refresh halaman.")
    
    csv_stok = stok_final.to_csv().encode('utf-8')
    st.download_button("Download Laporan Stok ke Excel", csv_stok, "Laporan_Stok.csv", "text/csv")

    st.subheader("Input Outbound")
    col1, col2, col3 = st.columns(3)
    with col1: tgl_deliv = st.date_input("Tanggal Delivery", datetime.date.today())
    with col2: item_deliv = st.text_input("Kode Item yang dikirim")
    with col3: qty_deliv = st.number_input("Jumlah dikirim", min_value=0)
    
    if st.button("Catat Delivery"):
        new_deliv = pd.DataFrame([[tgl_deliv, pilih_model, item_deliv, qty_deliv]], columns=["Tanggal", "Model", "Item", "Jumlah_Out"])
        new_deliv.to_csv(DELIVERY_FILE, mode='a', header=False, index=False)
        st.success("Delivery dicatat!")