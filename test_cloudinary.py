import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.api

# Paksa pembacaan file .env dari folder aktif
load_dotenv(dotenv_path='.env', override=True)

cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
api_key = os.getenv('CLOUDINARY_API_KEY')
api_secret = os.getenv('CLOUDINARY_API_SECRET')

print(f"--- PEMERIKSAAN FILE .ENV ---")
print(f"CLOUDINARY_CLOUD_NAME : {cloud_name}")
print(f"CLOUDINARY_API_KEY    : {api_key}")
print(f"--------------------------------")

if not cloud_name:
    print("❌ ERROR: File .env tidak ditemukan atau variabel CLOUDINARY_CLOUD_NAME masih kosong!")
else:
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret
    )

    try:
        response = cloudinary.api.ping()
        if response.get('status') == 'ok':
            print("✅ Koneksi Cloudinary BERHASIL!")
    except Exception as e:
        print(f"❌ Koneksi Cloudinary GAGAL: {e}")