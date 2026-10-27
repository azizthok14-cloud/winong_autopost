import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

print("Sedang mencoba menghubungkan ke TiDB Cloud...")

try:
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 4000)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        ssl_verify_cert=False
    )
    
    if conn.is_connected():
        print("✅ Koneksi TiDB Cloud BERHASIL!")
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE(), NOW();")
        db_name, server_time = cursor.fetchone()
        print(f" ── Database Aktif : {db_name}")
        print(f" ── Waktu Server   : {server_time}")
        cursor.close()
        conn.close()
except Exception as e:
    print(f"❌ Koneksi TiDB GAGAL!\nPesan Error: {e}")