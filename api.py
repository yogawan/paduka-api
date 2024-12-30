from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import sqlite3
import os
import secrets

app = Flask(__name__)
CORS(app)

secret_key = secrets.token_hex(32)
print(secret_key)
app.config['JWT_SECRET_KEY'] = secret_key
jwt = JWTManager(app)

DATABASE = 'db_ktp.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        cursor = conn.cursor()

        create_table_ktp = """
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

        create_table_users = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """

        create_table_user_data = """
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,

            Nik TEXT NOT NULL,
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

            NewProvinsi TEXT,
            NewKabupaten TEXT,
            NewKecamatan TEXT,
            NewKelurahan TEXT,
            NewDusun TEXT,

            Kewarganegaraan TEXT,
            Status TEXT DEFAULT 'Sedang di Review',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """

        cursor.execute(create_table_ktp)
        cursor.execute(create_table_users)
        cursor.execute(create_table_user_data)
        conn.commit()
        conn.close()



# Admin Side
@app.route('/api/ktp', methods=['GET'])
# @jwt_required()
def get_all_penduduk():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_ktp")
    rows = cursor.fetchall()
    conn.close()

    data = [dict(row) for row in rows]
    return jsonify(data), 200

@app.route('/api/ktp', methods=['POST'])
# @jwt_required()
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

# Review
@app.route('/api/userdata/<int:id>', methods=['PUT'])
def update_user_data(id):
    try:
        data = request.get_json()  # Ambil data dari request
        print(f"Data received for update: {data}")  # Log data yang diterima
        
        if not data:
            return jsonify({"error": "No data provided for update."}), 400

        # Ambil koneksi database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Buat query update secara dinamis berdasarkan field yang dikirimkan
        fields_to_update = []
        values = []

        for key, value in data.items():
            fields_to_update.append(f"{key} = ?")
            values.append(value)

        if not fields_to_update:
            return jsonify({"error": "No valid fields to update."}), 400

        # Tambahkan ID untuk WHERE clause
        values.append(id)

        # Query update
        query = f"UPDATE user_data SET {', '.join(fields_to_update)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
        conn.close()

        return jsonify({"message": "User data updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# User Side
# Register
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        cursor.execute(query, (username, password))
        conn.commit()
        conn.close()

        return jsonify({"message": "User registered successfully."}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Login
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Buat token akses JWT
            access_token = create_access_token(identity=username)
            return jsonify({"message": "Login successful.", "token": access_token}), 200
        else:
            return jsonify({"error": "Invalid username or password."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST by User
@app.route('/api/userdata', methods=['POST'])
@jwt_required()
def post_user_data():
    try:
        # Ambil data dari request
        data = request.get_json()
        username = get_jwt_identity()  # Ambil username dari token JWT

        # Validasi data yang diperlukan
        required_fields = [
            "Nik", "Nama_Lengkap", "Gol_Darah", "Tempat_Lahir", "Tanggal_Lahir",
            "Jenis_Kelamin", "Agama", "Status_Kawin", "Pekerjaan", "Provinsi",
            "Kabupaten", "Kecamatan", "Kelurahan", "Dusun", "NewProvinsi",
            "NewKabupaten", "NewKecamatan", "NewKelurahan", "NewDusun", "Kewarganegaraan"
        ]

        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"'{field}' is required."}), 400

        # Simpan data ke database
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO user_data (
            username, Nik, Nama_Lengkap, Gol_Darah, Tempat_Lahir, Tanggal_Lahir,
            Jenis_Kelamin, Agama, Status_Kawin, Pekerjaan, Provinsi, Kabupaten,
            Kecamatan, Kelurahan, Dusun, NewProvinsi, NewKabupaten, NewKecamatan,
            NewKelurahan, NewDusun, Kewarganegaraan
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            username, data["Nik"], data["Nama_Lengkap"], data["Gol_Darah"],
            data["Tempat_Lahir"], data["Tanggal_Lahir"], data["Jenis_Kelamin"],
            data["Agama"], data["Status_Kawin"], data["Pekerjaan"], data["Provinsi"],
            data["Kabupaten"], data["Kecamatan"], data["Kelurahan"], data["Dusun"],
            data["NewProvinsi"], data["NewKabupaten"], data["NewKecamatan"],
            data["NewKelurahan"], data["NewDusun"], data["Kewarganegaraan"]
        ))
        conn.commit()
        conn.close()

        return jsonify({"message": "Data successfully added with status 'Sedang di Review'."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET user data
@app.route('/api/userdata', methods=['GET'])
@jwt_required()
def get_user_data():
    try:
        username = get_jwt_identity()  # Ambil username dari token JWT

        # Ambil data milik pengguna dari database
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        SELECT id, username, Nik, Nama_Lengkap, Gol_Darah, Tempat_Lahir, Tanggal_Lahir,
               Jenis_Kelamin, Agama, Status_Kawin, Pekerjaan, Provinsi, Kabupaten,
               Kecamatan, Kelurahan, Dusun, NewProvinsi, NewKabupaten, NewKecamatan,
               NewKelurahan, NewDusun, Kewarganegaraan, Status, created_at
        FROM user_data 
        WHERE username = ? 
        ORDER BY created_at DESC
        """
        cursor.execute(query, (username,))
        rows = cursor.fetchall()
        conn.close()

        # Konversi data ke format JSON
        data = [dict(row) for row in rows]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET all
@app.route('/api/alluserdata', methods=['GET'])
def get_all_userdata():
    try:
        # Ambil semua data dari tabel user_data
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        SELECT id, username, Nik, Nama_Lengkap, Gol_Darah, Tempat_Lahir, Tanggal_Lahir,
               Jenis_Kelamin, Agama, Status_Kawin, Pekerjaan, Provinsi, Kabupaten,
               Kecamatan, Kelurahan, Dusun, NewProvinsi, NewKabupaten, NewKecamatan,
               NewKelurahan, NewDusun, Kewarganegaraan, Status, created_at
        FROM user_data
        ORDER BY created_at DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        # Konversi data ke format JSON
        data = [dict(row) for row in rows]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET userprofile
@app.route('/api/user/username', methods=['GET'])
@jwt_required()
def get_logged_in_username():
    try:
        # Ambil username dari token JWT
        username = get_jwt_identity()

        # Ambil username dari database untuk memastikan user ada
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT username FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return jsonify({"username": row["username"]}), 200
        else:
            return jsonify({"error": "User not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)