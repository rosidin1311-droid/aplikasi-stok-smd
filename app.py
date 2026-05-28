import streamlit as st
import pandas as pd

# --- TEMA & CONFIG ---
st.set_page_config(page_title="Data Stok SMD", layout="wide")
st.markdown("""<style>.stApp { background-color: #fdfaf6; } h1 { color: #8b5e3c; }</style>""", unsafe_allow_html=True)

# --- URL CSV ---
URLS = {
    "PROD": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=0&single=true&output=csv",
    "DELIV": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=955087734&single=true&output=csv",
    "MASTER": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxAA8vyucxniOE_DKmYp6LmnxOw6EO676Xp0iEaOeKX7BKeVa2aVvOabU2Quf1Mccqsk8QUIh0UN-Q/pub?gid=1449236361&single=true&output=csv"
}

@st.cache_data(ttl=60)
def load(url): return pd.read_csv(url)

df = load(URLS["PROD"])
df_master = load(URLS["MASTER"])

menu = st.sidebar.selectbox("Menu", ["🏭 Input Produksi", "📊 Monitoring WIP", "📦 Data Stok", "⚙️ Master Data"])

# --- MENU MASTER (WITH EDIT) ---
if menu == "⚙️ Master Data":
    st.subheader("⚙️ Master Data (Editable)")
    edited_df = st.data_editor(df_master, num_rows="dynamic")
    st.download_button("📥 Download Master CSV", edited_df.to_csv(index=False), "master.csv", "text/csv")

# --- MENU INPUT PRODUKSI ---
elif menu == "🏭 Input Produksi":
    st.subheader("🏭 Input Produksi")
    model_list = df_master[df_master.iloc[:,0] == "Model"].iloc[:,1].dropna().unique()
    proses_list = df_master[df_master.iloc[:,0] == "Proses"].iloc[:,1].dropna().unique()
    
    with st.form("input_form"):
        m = st.selectbox("Pilih Model", model_list)
        p = st.selectbox("Pilih Proses", proses_list)
        item = st.text_input("Nama Item")
        qty = st.number_input("Jumlah OK", min_value=0)
        submitted = st.form_submit_button("Simpan Data")
        if submitted:
            st.success(f"Data {item} untuk {m} berhasil diproses!")

# --- MENU MONITORING WIP & DATA STOK (WITH DOWNLOAD) ---
elif menu == "📊 Monitoring WIP":
    st.subheader("📊 Monitoring WIP")
    st.dataframe(df, use_container_width=True)
    st.download_button("📥 Download WIP CSV", df.to_csv(index=False), "wip.csv", "text/csv")

elif menu == "📦 Data Stok":
    st.subheader("📦 Data Stok (Cek Point)")
    pilih_m = st.selectbox("Pilih Model", df.iloc[:, 1].dropna().unique())
    stok_df = df[(df.iloc[:, 1] == pilih_m) & (df.iloc[:, 3] == "Cek Point")]
    
    if not stok_df.empty:
        st.table(stok_df)
        st.download_button("📥 Download Stok CSV", stok_df.to_csv(index=False), "stok.csv", "text/csv")
    else:
        st.warning("Tidak ada data selesai proses (Cek Point).")

if st.sidebar.button("🔄 Refresh"): st.rerun()
