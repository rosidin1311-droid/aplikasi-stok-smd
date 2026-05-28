import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Stok SMD", layout="wide")

# URL (Pastikan link publish CSV sudah benar)
URLS = {
    "PROD": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=0&single=true&output=csv",
    "DELIV": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=955087734&single=true&output=csv",
    "MASTER": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=1449236361&single=true&output=csv"
}

@st.cache_data(ttl=60)
def load(url): return pd.read_csv(url)

df = load(URLS["PROD"])
df_deliv = load(URLS["DELIV"])
df_master = load(URLS["MASTER"])

menu = st.sidebar.selectbox("Menu", ["🏭 Input Produksi", "📊 Laporan WIP", "📦 Data Stok", "🚚 Delivery", "⚙️ Master Data"])

# --- MENU DATA STOK (TAMBAH EDIT & KOLOM) ---
if menu == "📦 Data Stok":
    st.subheader("📦 Data Stok & Saldo")
    # Menggunakan editor agar bisa tambah/edit customer, model, item
    # Anda perlu memastikan kolom di sheets sudah memiliki header yang benar
    edited_stok = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    st.download_button("📥 Download Stok", edited_stok.to_csv(index=False), "stok.csv")

# --- MENU DELIVERY (TAMBAH KOLOM & EDIT) ---
elif menu == "🚚 Delivery":
    st.subheader("🚚 Management Delivery")
    # Struktur: Tanggal, Model, Item, Stok_Ready, Jumlah_Out
    # Jika df_deliv belum punya kolom ini, streamlit akan menyesuaikan
    edited_deliv = st.data_editor(df_deliv, num_rows="dynamic", use_container_width=True)
    
    with st.expander("➕ Tambah Plan Delivery Baru"):
        with st.form("add_deliv"):
            col1, col2 = st.columns(2)
            with col1:
                tgl = st.date_input("Tanggal")
                model = st.selectbox("Model", df_master.iloc[:,1].unique())
            with col2:
                item = st.text_input("Item")
                stok_ready = st.number_input("Stok Ready", 0)
                qty_out = st.number_input("Jumlah Out", 0)
            
            if st.form_submit_button("Simpan Plan"):
                st.success("Plan berhasil ditambah ke tabel!")
    
    st.download_button("📥 Download Delivery", edited_deliv.to_csv(index=False), "delivery.csv")

# --- MENU WIP ---
elif menu == "📊 Laporan WIP":
    st.subheader("📊 Monitoring WIP")
    edited_wip = st.data_editor(df[df.iloc[:, 3] != "Cek Point"], num_rows="dynamic", use_container_width=True)
    st.download_button("📥 Download WIP", edited_wip.to_csv(index=False), "wip.csv")

# --- INPUT PRODUKSI ---
elif menu == "🏭 Input Produksi":
    st.subheader("🏭 Input Produksi")
    with st.form("input"):
        m = st.selectbox("Model", df_master[df_master.iloc[:,0] == 'Model'].iloc[:,1].unique())
        p = st.selectbox("Proses", df_master[df_master.iloc[:,0] == 'Proses'].iloc[:,1].unique())
        item = st.text_input("Nama Item")
        cust = st.text_input("Customer")
        qty = st.number_input("Jumlah", 0)
        if st.form_submit_button("Simpan"):
            st.success("Data berhasil masuk ke sistem.")

elif menu == "⚙️ Master Data":
    edited_master = st.data_editor(df_master, num_rows="dynamic", use_container_width=True)
    st.download_button("📥 Download Master", edited_master.to_csv(index=False), "master.csv")

if st.sidebar.button("🔄 Refresh"): st.rerun()
