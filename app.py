from supabase import create_client
import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
import cv2
import numpy as np

SUPABASE_URL = "https://rvuvxwxhaejxfoiygzck.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ2dXZ4d3hoYWVqeGZvaXlnemNrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkxMjAxODYsImV4cCI6MjA3NDY5NjE4Nn0._le34zD9gWBZOk7An4vCNOcH8pjhVZ9IehM6fTcT3Ww"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


st.subheader("Pencarian Barang")

# Opsi input: manual atau scan
input_method = st.radio("Pilih metode input:", ["Manual Input", "Scan Barcode"])

kode_barang = ""

if input_method == "Manual Input":
    kode_barang = st.text_input("Masukan Kode Barang")
else:
    # Fitur scan barcode
    camera_image = st.camera_input("Scan Barcode")
    
    if camera_image is not None:
        # Convert image to OpenCV format
        image = Image.open(camera_image)
        img_array = np.array(image)
        
        # Convert to grayscale for better OCR
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Use pytesseract to read barcode (text)
        try:
            kode_barang = pytesseract.image_to_string(gray).strip()
            st.success(f"Barcode terdeteksi: {kode_barang}")
        except:
            st.error("Gagal membaca barcode. Pastikan barcode jelas dan terang.")

if st.button("Submit"):
    if kode_barang.strip():
        stok = supabase.table("v_stok_barang").select("*").eq("kode_barang", kode_barang).execute().data
        
        if stok:
            df_stok = pd.DataFrame(stok)
            kolom_yang_dihapus = ["id_barang"]
            # Hapus kolom hanya jika ada
            df_stok = df_stok.drop(columns=[col for col in kolom_yang_dihapus if col in df_stok.columns])
            st.dataframe(df_stok, hide_index=True)

            # Ambil id_barang untuk mencari transaksi
            id_barang = stok[0].get('id_barang')
            if id_barang:
                history_transaksi = supabase.table("transaksi").select("*").eq("id_barang", id_barang).execute().data
                df_history_transaksi = pd.DataFrame(history_transaksi)
                st.dataframe(df_history_transaksi, hide_index=True)
        else:
            st.warning("Barang tidak ditemukan!")