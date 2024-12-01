import mysql.connector

def connect_to_server():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='pw'
    )

def connect_to_db():
    return mysql.connector.connect(
        host='localhost',
        user='yogaone',
        password='fullsnack',
        database='db_ktp'
    )

def create_database():
    db = connect_to_server()
    myCursor = db.cursor()
    myCursor.execute("CREATE DATABASE IF NOT EXISTS db_ktp")
    print("Database 'db_ktp' telah dibuat.")
    myCursor.close()
    db.close()

def create_table():
    db = connect_to_db()
    myCursor = db.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tb_ktp (
        Nik VARCHAR(16) PRIMARY KEY,
        Nama_Lengkap VARCHAR(50),
        Gol_Darah VARCHAR(2),
        Tempat_Lahir VARCHAR(50),
        Tanggal_Lahir DATE,
        Jenis_Kelamin ENUM('L', 'P'),
        Agama VARCHAR(20),
        Status_Kawin VARCHAR(20),
        Pekerjaan VARCHAR(50),
        Alamat TEXT,
        Kewarganegaraan VARCHAR(3)
    );
    """
    myCursor.execute(create_table_query)
    print("Tabel 'tb_ktp' telah dibuat.")
    myCursor.close()
    db.close()

def inputPenduduk():
    db = connect_to_db()
    myCursor = db.cursor()
    try:
        Nik = input("Masukan NIK Anda (16 digit): ")
        Nama_Lengkap = input("Masukan Nama Anda: ")
        Gol_Darah = input("Masukan Golongan Darah Anda (A/B/AB/O): ").upper()
        if Gol_Darah not in ['A', 'B', 'AB', 'O']:
            print("Golongan Darah hanya boleh A, B, AB, atau O.")
            return
        Tempat_Lahir = input("Masukan Tempat Lahir Anda: ")
        Tanggal_Lahir = input("Masukan Tanggal Lahir Anda (YYYY-MM-DD): ")
        Jenis_Kelamin = input("Masukan Jenis Kelamin Anda (L/P): ").upper()
        if Jenis_Kelamin not in ['L', 'P']:
            print("Jenis Kelamin hanya boleh L atau P.")
            return
        Agama = input("Masukan Agama Anda: ")
        Status_Kawin = input("Masukan Status Kawin Anda: ")
        Pekerjaan = input("Masukan Pekerjaan Anda: ")
        Alamat = input("Masukan Alamat Anda: ")
        Kewarganegaraan = input("Masukan Kewarganegaraan Anda (WNI/WNA): ").upper()
        if Kewarganegaraan not in ['WNI', 'WNA']:
            print("Kewarganegaraan hanya boleh WNI atau WNA.")
            return
        
        tamp = (Nik, Nama_Lengkap, Gol_Darah, Tempat_Lahir, Tanggal_Lahir, Jenis_Kelamin, Agama, Status_Kawin, Pekerjaan, Alamat, Kewarganegaraan)
        sql = """INSERT INTO tb_ktp (Nik, Nama_Lengkap, Gol_Darah, Tempat_Lahir, Tanggal_Lahir, Jenis_Kelamin, Agama, Status_Kawin, Pekerjaan, Alamat, Kewarganegaraan)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        myCursor.execute(sql, tamp)
        db.commit()
        print("Data berhasil disimpan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        myCursor.close()
        db.close()

def main():
    create_database()
    create_table()
    while True:
        print("\nPilih Menu:")
        print("1. Input Data Penduduk")
        print("2. Exit")
        pilih = input("Masukan pilihan: ")
        if pilih == "1":
            inputPenduduk()
        elif pilih == "2":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()