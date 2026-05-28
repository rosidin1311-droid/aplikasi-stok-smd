import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Data Stok SMD", layout="wide")

# --- URL (PASTIKAN LINK SUDAH PUBLISH AS CSV) ---
URLS = {
    "PROD": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=0&single=true&output=csv",
    "MASTER": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=1449236361&single=true&output=csv"
}

@st.cache_data(ttl=60)
def load(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip() # Hilangkan spasi di header
    return df

try:
    df_prod = load(URLS["PROD"])
    df_master = load(URLS["MASTER"])
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

# --- MENU ---
menu = st.sidebar.selectbox("Menu", ["🏭 Input Produksi", "📦 Data Stok", "⚙️ Master Data"])

# --- MENU MASTER (EDITABLE) ---
if menu == "⚙️ Master Data":
    st.subheader("⚙️ Master Data (Customer, Model, Item)")
    # Menampilkan data master yang bisa diedit
    edited_master = st.data_editor(df_master, num_rows="dynamic", use_container_width=True)
    st.download_button("📥 Download Master CSV", edited_master.to_csv(index=False), "master.csv")

# --- MENU INPUT PRODUKSI ---
elif menu == "🏭 Input Produksi":
    st.subheader("🏭 Input Produksi")
    
    # DEBUG: Cek apa isi kolom pertama (index 0)
    # df_master.iloc[:, 0] diharapkan berisi kategori (Customer/Model/Item)
    # df_master.iloc[:, 1] diharapkan berisi nilainya
    
    # Ambil list unik berdasarkan kategori
    models = df_master[df_master.iloc[:, 0] == 'Model'].iloc[:, 1].dropna().unique()
    proses = df_master[df_master.iloc[:, 0] == 'Proses'].iloc[:, 1].dropna().unique()
    
    with st.form("input_prod"):
        m = st.selectbox("Pilih Model", models if len(models) > 0 else ["Belum ada data"])
        p = st.selectbox("Pilih Proses", proses if len(proses) > 0 else ["Belum ada data"])
        item = st.text_input("Nama Item")
        cust = st.text_input("Customer")
        qty = st.number_input("Jumlah OK", min_value=0)
        
        if st.form_submit_button("Simpan Data"):
            st.success(f"Berhasil Input {item} untuk {m} ({cust})")

# --- MENU DATA STOK ---
elif menu == "📦 Data Stok":
    st.subheader("📦 Data Stok")
    models = df_prod.iloc[:, 1].dropna().unique()
    pilih = st.selectbox("Pilih Model", models)
    
    # Filter data produksi yang sudah 'Cek Point'
    stok = df_prod[(df_prod.iloc[:, 1] == pilih) & (df_prod.iloc[:, 3] == "Cek Point")]
    
    if not stok.empty:
        st.dataframe(stok, use_container_width=True)
        st.download_button("📥 Download Stok", stok.to_csv(index=False), "stok.csv")
    else:
        st.warning("Data belum mencapai Cek Point.")

if st.sidebar.button("🔄 Refresh Data"): st.rerun()
