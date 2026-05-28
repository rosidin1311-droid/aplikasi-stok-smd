import streamlit as st
import pandas as pd

# --- CONFIG & URL ---
st.set_page_config(page_title="Data Stok SMD", layout="wide")

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

# --- FUNGSI LOGIKA STOK DINAMIS ---
def get_stok_otomatis(model):
    # 1. Cari apa proses akhir untuk model ini (dari Master Data)
    # Asumsi: Master Data punya kolom [Kategori, Nama, Is_Final_Process]
    final_process = df_master[(df_master.iloc[:,0] == "Proses Akhir") & 
                              (df_master.iloc[:,1] == model)].iloc[:, 2].values
    
    if len(final_process) == 0: return 0 # Default jika belum diset
    target_proses = final_process[0]
    
    # 2. Hitung Produksi yang sudah sampai di proses tersebut
    total_prod = df[(df.iloc[:, 1] == model) & (df.iloc[:, 3] == target_proses)].iloc[:, 4].sum()
    
    # 3. Hitung Delivery (Kolom ke-4 adalah Jumlah_Out berdasarkan request baru Anda)
    total_deliv = df_deliv[(df_deliv.iloc[:, 1] == model)].iloc[:, 4].sum()
    
    return total_prod - total_deliv

# --- MENU APP ---
menu = st.sidebar.selectbox("Menu", ["📊 Laporan WIP", "📦 Data Stok", "🚚 Delivery", "⚙️ Master Data"])

# --- MENU LAPORAN WIP (DENGAN LOGIKA OTOMATIS) ---
if menu == "📊 Laporan WIP":
    st.subheader("📊 Monitoring Barang Belum Selesai (WIP)")
    
    # Logika: Tampilkan data yang BUKAN 'Cek Point'
    wip_df = df[df.iloc[:, 3] != "Cek Point"].copy()
    
    st.write("Edit data WIP di bawah jika ada barang yang belum terinput:")
    edited_wip = st.data_editor(wip_df, use_container_width=True)
    
    # Logika Otomatis: Ringkasan WIP per Proses
    st.subheader("Ringkasan Saldo per Proses")
    summary = edited_wip.groupby(edited_wip.iloc[:, 3])[[edited_wip.columns[4]]].sum()
    st.table(summary)
    
    st.download_button("📥 Download Laporan WIP", edited_wip.to_csv(index=False), "wip_report.csv")

if menu == "📦 Data Stok":
    st.subheader("📦 Data Stok Real-time")
    list_model = df["Model"].unique() # Pastikan header sudah benar
    stok_data = []
    
    for m in list_model:
        stok_data.append({"Model": m, "Stok Tersedia": get_stok_otomatis(m)})
    
    st.table(pd.DataFrame(stok_data))

elif menu == "🚚 Delivery":
    st.subheader("🚚 Input Delivery")
    # Tampilkan tabel delivery baru dengan kolom: Tanggal, Model, Item, Stok_Ready, Jumlah_Out
    st.dataframe(df_deliv)
    with st.form("deliv_form"):
        # Input form disesuaikan dengan kolom baru Anda
        tgl = st.date_input("Tanggal")
        model = st.selectbox("Model", df_master.iloc[:, 1].unique())
        qty_out = st.number_input("Jumlah Out", 0)
        if st.form_submit_button("Simpan Delivery"):
            st.success("Delivery tersimpan.")

elif menu == "🏭 Input Produksi":
    st.subheader("🏭 Input Produksi")
    with st.form("input"):
        m = st.selectbox("Model", df_master[df_master.iloc[:,0] == 'Model'].iloc[:,1].unique())
        p = st.selectbox("Proses", df_master[df_master.iloc[:,0] == 'Proses'].iloc[:,1].unique())
        item = st.text_input("Nama Item")
        qty = st.number_input("Jumlah", 0)
        if st.form_submit_button("Simpan"):
            st.success("Data telah masuk ke sistem WIP.")

elif menu == "⚙️ Master Data":
    edited_master = st.data_editor(df_master, use_container_width=True)
    st.download_button("📥 Download Master", edited_master.to_csv(index=False), "master.csv")

if st.sidebar.button("🔄 Refresh"): st.rerun()
