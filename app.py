from supabase import create_client
import streamlit as st
import pandas as pd

SUPABASE_URL = "https://rvuvxwxhaejxfoiygzck.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ2dXZ4d3hoYWVqeGZvaXlnemNrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkxMjAxODYsImV4cCI6MjA3NDY5NjE4Nn0._le34zD9gWBZOk7An4vCNOcH8pjhVZ9IehM6fTcT3Ww"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


st.subheader("Pencarian Barang")

# Opsi input: manual atau scan

kode_barang = ""

kode_barang = st.text_input("Masukan Kode Barang")

if st.button("Submit"):
    if kode_barang.strip():
        stok = supabase.table("v_stok_barang").select("*").eq("kode_barang", kode_barang).execute().data
        if stok:
            df_stok = pd.DataFrame(stok)
            kolom_yang_dihapus = ["id_barang"]
            # Hapus kolom hanya jika ada
            df_stok = df_stok.drop(columns=[col for col in kolom_yang_dihapus if col in df_stok.columns])
            st.dataframe(df_stok, hide_index=True)


            st.subheader("History Transaksi")
            # Ambil id_barang untuk mencari transaksi
            kode_barang = stok[0].get('kode_barang')
            if kode_barang:
                history_transaksi = (
                supabase.table("v_transaksi_stok").select("*").eq("kode_barang", kode_barang).execute().data)

                df_history_transaksi = pd.DataFrame(history_transaksi)

                kolom_urutan = ["tanggal", "id_transaksi","keterangan", "kode_barang", "jenis", "jumlah","masuk","keluar","stok"]
                def format_number(x):
                    if pd.isna(x):      # kalau None/NaN
                        return ""
                    if float(x).is_integer():  
                        return str(int(x))  # tampilkan tanpa .0
                    return str(x)  # kalau ada desimal, biarkan
                
                df_history_transaksi["masuk"] = df_history_transaksi["masuk"].apply(format_number)
                df_history_transaksi["keluar"] = df_history_transaksi["keluar"].apply(format_number)
                df_history_transaksi["stok"] = df_history_transaksi["stok"].apply(format_number)
                df_history_transaksi = df_history_transaksi[kolom_urutan]
                df_history_transaksi = df_history_transaksi.fillna("")


            # format kolom tanggal jadi DD-MM-YYYY
            if "tanggal" in df_history_transaksi.columns:
                df_history_transaksi["tanggal"] = pd.to_datetime(df_history_transaksi["tanggal"]).dt.strftime("%d-%m-%Y")

                df_history_transaksi = df_history_transaksi.drop(columns=["id_transaksi","kode_barang","jumlah"])
            st.dataframe(
                df_history_transaksi.style.set_properties(**{'text-align': 'center'}).
                set_table_styles([{"selector": "th", "props": [("text-align", "center")]}]),
                hide_index=True)

        else:
            st.warning("Barang tidak ditemukan!")



