from supabase import create_client

# Ganti dengan URL & KEY dari project Supabase kamu
SUPABASE_URL = "https://rvuvxwxhaejxfoiygzck.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ2dXZ4d3hoYWVqeGZvaXlnemNrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkxMjAxODYsImV4cCI6MjA3NDY5NjE4Nn0._le34zD9gWBZOk7An4vCNOcH8pjhVZ9IehM6fTcT3Ww"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    # Coba ambil semua data dari tabel barang
    response = supabase.table("barang").select("*").execute()
    print("✅ Koneksi berhasil!")
    print("Data dari tabel barang:")
    print(response.data)
except Exception as e:
    print("❌ Koneksi gagal:", e)
