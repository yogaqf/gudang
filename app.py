from supabase import create_client
import streamlit as st
import pandas as pd

SUPABASE_URL = "https://rvuvxwxhaejxfoiygzck.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ2dXZ4d3hoYWVqeGZvaXlnemNrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkxMjAxODYsImV4cCI6MjA3NDY5NjE4Nn0._le34zD9gWBZOk7An4vCNOcH8pjhVZ9IehM6fTcT3Ww"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.subheader("Pencarian Barang")
kode_barang = st.text_input("Masukan Kode Barang")
if st.button("Submit"):
    stok = supabase.table("v_stok_barang").select("*").eq("kode_barang", kode_barang).execute().data
    df_stok = pd.DataFrame(stok)
    st.write(df_stok)

