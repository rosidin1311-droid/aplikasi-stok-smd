import streamlit as st
import pandas as pd

# Konfigurasi Tema Corduroy
st.set_page_config(page_title="Corduroy System", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    h1, h2, h3 { color: #5D4037; font-family: sans-serif; }
    div[data-testid="stForm"] { background-color: #EDE0C6; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI MOCKUP DATA (Simulasi Koneksi) ---
def get_master():
    # Ini nantinya load dari Google Sheets
    return pd.DataFrame({
        "Customer": ["PT A", "PT B"],
        "Model": ["Axio", "Bolt"],
        "Item": ["Bolt-A", "Bolt-B"],
        "Alur": ["Cut,Sew,QC", "Cut,QC"]
    })

master_df = get_master()

# --- SIDEBAR ---
menu = st.sidebar.radio("Navigasi", ["🏭 Input Produksi", "📦 Data Stok & Delivery", "⚙️ Master Data"])

# --- 1. MASTER DATA ---
if menu == "⚙️ Master Data":
    st.subheader("⚙️ Setup Master Data")
    edited_master = st.data_editor(master_df, num_rows="dynamic", use_container_width=True)
    if st.download_button("📥 Download Master Data", edited_master.to_csv(index=False), "master.csv"):
        st.success("Download berhasil!")

# --- 2. INPUT PRODUKSI ---
elif menu == "🏭 Input Produksi":
    st.subheader("🏭 Input Progres Produksi")
    
    with st.form("input_prod"):
        col1, col2 = st.columns(2)
        # Menghubungkan dropdown dengan Master Data
        cust = col1.selectbox("Pilih Customer", master_df["Customer"].unique())
        model = col1.selectbox("Pilih Model", master_df[master_df["Customer"]==cust]["Model"].unique())
        item = col2.selectbox("Pilih Item", master_df[master_df["Model"]==model]["Item"].unique())
        proses = col2.selectbox("Proses", ["Cut", "Sew", "QC"])
        qty = st.number_input("Jumlah OK", min_value=0)
        
        if st.form_submit_button("Simpan Progress"):
            st.success(f"Berhasil mencatat {qty} pcs untuk {item}")

# --- 3. DATA STOK & DELIVERY ---
elif menu == "📦 Data Stok & Delivery":
    st.subheader("📦 Inventory & Plan Delivery")
    
    # Bagian Data Stok
    st.markdown("### Saldo Stok")
    stok_df = pd.DataFrame({"Customer": ["PT A"], "Model": ["Axio"], "Item": ["Bolt-A"], "Stok": [100]})
    edited_stok = st.data_editor(stok_df, use_container_width=True)
    st.download_button("📥 Download Stok", edited_stok.to_csv(index=False), "stok.csv")
    
    st.divider()
    
    # Bagian Delivery (Terhubung dengan Master Data)
    st.markdown("### Plan Delivery")
    with st.form("add_deliv"):
        c1, c2 = st.columns(2)
        cust_deliv = c1.selectbox("Customer (Ref Master)", master_df["Customer"].unique())
        model_deliv = c1.selectbox("Model (Ref Master)", master_df[master_df["Customer"]==cust_deliv]["Model"].unique())
        item_deliv = c2.selectbox("Item (Ref Master)", master_df[master_df["Model"]==model_deliv]["Item"].unique())
        tgl = c2.date_input("Tanggal Kirim")
        
        if st.form_submit_button("Tambah ke List Delivery"):
            st.info(f"Rencana kirim {item_deliv} untuk {cust_deliv} ditambahkan.")
            
    # Tabel Delivery
    deliv_df = pd.DataFrame({"Tanggal": ["2026-06-01"], "Customer": ["PT A"], "Item": ["Bolt-A"], "Qty": [50], "Status": ["Pending"]})
    edited_deliv = st.data_editor(deliv_df, use_container_width=True)
    st.download_button("📥 Download Delivery", edited_deliv.to_csv(index=False), "delivery.csv")
