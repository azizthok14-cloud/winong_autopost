import os
import mysql.connector
import requests
import cloudinary
import cloudinary.uploader
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env', override=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_winong')

# Konfigurasi Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Helper Koneksi Database TiDB Cloud
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 4000)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        ssl_verify_cert=False
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_momen():
    nama_member = request.form.get('nama_member')
    caption = request.form.get('caption')
    file_media = request.files.get('media')

    if not nama_member or not caption or not file_media:
        return jsonify({'status': 'error', 'message': 'Semua kolom wajib diisi!'}), 400

    try:
        # 1. Upload File ke Cloudinary
        upload_result = cloudinary.uploader.upload(
            file_media,
            resource_type="auto",
            folder="winong_posts"
        )
        
        media_url = upload_result.get('secure_url')
        resource_type = upload_result.get('resource_type')  # 'image' atau 'video'
        
        # 2. Format Caption
        final_caption = f"{caption}\n\n📸 Momen oleh: {nama_member}\n#TheWinong #WinongCommunity"

        # 3. Simpan Metadata ke TiDB Cloud
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO posts (nama_member, caption, media_url, media_type, status_posting) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nama_member, final_caption, media_url, resource_type, 'approved'))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'status': 'success',
            'message': '✅ Momen berhasil tersimpan di TiDB & Cloudinary!',
            'url': media_url
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': f"Terjadi kesalahan: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Server Flask The Winong berjalan di http://127.0.0.1:5000")
    app.run(debug=True, port=5000)