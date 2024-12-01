from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app, origins="http://localhost:5173")

# Koneksi
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='yogaone',
        password='fullsnack',
        database='db_ktp'
    )
    return connection

# Get by NIK
@app.route('/api/ktp/<nik>', methods=['GET'])
def get_ktp(nik):
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM tb_ktp WHERE Nik = %s"
        cursor.execute(query, (nik,))
        result = cursor.fetchone()
        
        if result:
            return jsonify(result), 200
        else:
            return jsonify({'message': 'Data KTP tidak ditemukan'}), 404

    except Error as e:
        return jsonify({'message': f'Terjadi kesalahan: {e}'}), 500
    finally:
        if connection:
            connection.close()

# GET
@app.route('/api/ktp', methods=['GET'])
def get_all_ktp():
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM tb_ktp"
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            return jsonify(results), 200
        else:
            return jsonify({'message': 'Tidak ada data KTP ditemukan'}), 404

    except Error as e:
        return jsonify({'message': f'Terjadi kesalahan: {e}'}), 500
    finally:
        if connection:
            connection.close()

# POST
@app.route('/api/ktp', methods=['POST'])
def add_ktp():
    data = request.get_json()

    # Cek apakah semua field diperlukan ada
    required_fields = ['Nik', 'Nama_Lengkap', 'Gol_Darah', 'Tempat_Lahir', 'Tanggal_Lahir', 'Jenis_Kelamin', 'Agama', 'Status_Kawin', 'Pekerjaan', 'Alamat', 'Kewarganegaraan']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Semua field diperlukan'}), 400

    # Cek format tanggal (jika diperlukan)
    try:
        Tanggal_Lahir = data['Tanggal_Lahir']
        # Validasi tanggal jika perlu
        from datetime import datetime
        datetime.strptime(Tanggal_Lahir, "%Y-%m-%d")  # Pastikan format YYYY-MM-DD
    except ValueError:
        return jsonify({'message': 'Format tanggal tidak valid, harus YYYY-MM-DD'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO tb_ktp (Nik, Nama_Lengkap, Gol_Darah, Tempat_Lahir, Tanggal_Lahir, Jenis_Kelamin, Agama, Status_Kawin, Pekerjaan, Alamat, Kewarganegaraan)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['Nik'],
            data['Nama_Lengkap'],
            data['Gol_Darah'],
            data['Tempat_Lahir'],
            data['Tanggal_Lahir'],
            data['Jenis_Kelamin'],
            data['Agama'],
            data['Status_Kawin'],
            data['Pekerjaan'],
            data['Alamat'],
            data['Kewarganegaraan']
        ))
        connection.commit()

        return jsonify({'message': 'Data KTP berhasil ditambahkan'}), 201

    except Error as e:
        print(f"Database Error: {e}")  # Log kesalahan database
        return jsonify({'message': f'Terjadi kesalahan: {e}'}), 500
    finally:
        if connection:
            connection.close()



if __name__ == '__main__':
    app.run(debug=True)
