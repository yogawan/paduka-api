from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)
DATABASE = 'db_ktp.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tb_ktp (
            Nik TEXT PRIMARY KEY,
            Nama_Lengkap TEXT,
            Gol_Darah TEXT,
            Tempat_Lahir TEXT,
            Tanggal_Lahir TEXT,
            Jenis_Kelamin TEXT,
            Agama TEXT,
            Status_Kawin TEXT,
            Pekerjaan TEXT,
            Provinsi TEXT,
            Kabupaten TEXT,
            Kecamatan TEXT,
            Kelurahan TEXT,
            Dusun TEXT,
            Kewarganegaraan TEXT
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        conn.close()

@app.route('/api/ktp', methods=['GET'])
def get_all_penduduk():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_ktp")
    rows = cursor.fetchall()
    conn.close()

    data = [dict(row) for row in rows]
    return jsonify(data), 200

@app.route('/api/ktp', methods=['POST'])
def add_penduduk():
    try:
        data = request.get_json()
        required_fields = [
            "Nik", "Nama_Lengkap", "Gol_Darah", "Tempat_Lahir", "Tanggal_Lahir",
            "Jenis_Kelamin", "Agama", "Status_Kawin", "Pekerjaan", "Provinsi",
            "Kabupaten", "Kecamatan", "Kelurahan", "Dusun", "Kewarganegaraan"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"'{field}' is required."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO tb_ktp (Nik, Nama_Lengkap, Gol_Darah, Tempat_Lahir, Tanggal_Lahir,
                            Jenis_Kelamin, Agama, Status_Kawin, Pekerjaan, Provinsi,
                            Kabupaten, Kecamatan, Kelurahan, Dusun, Kewarganegaraan)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            data['Nik'], data['Nama_Lengkap'], data['Gol_Darah'], data['Tempat_Lahir'],
            data['Tanggal_Lahir'], data['Jenis_Kelamin'], data['Agama'],
            data['Status_Kawin'], data['Pekerjaan'], data['Provinsi'],
            data['Kabupaten'], data['Kecamatan'], data['Kelurahan'],
            data['Dusun'], data['Kewarganegaraan']
        ))
        conn.commit()
        conn.close()

        return jsonify({"message": "Data successfully added."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
