import sqlite3

def connect_to_db():
    return sqlite3.connect("db_ktp.sqlite")

def create_table():
    db = connect_to_db()
    cursor = db.cursor()
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
    db.commit()
    print("Tabel 'tb_ktp' telah dibuat.")
    cursor.close()
    db.close()

def inputPenduduk():
    db = connect_to_db()
    cursor = db.cursor()
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
        Provinsi = input("Masukan Provinsi Anda: ")
        Kabupaten = input("Masukan Kabupaten Anda: ")
        Kecamatan = input("Masukan Kecamatan Anda: ")
        Kelurahan = input("Masukan Kelurahan Anda: ")
        Dusun = input("Masukan Dusun Anda: ")
        Kewarganegaraan = input("Masukan Kewarganegaraan Anda (WNI/WNA): ").upper()
        if Kewarganegaraan not in ['WNI', 'WNA']:
            print("Kewarganegaraan hanya boleh WNI atau WNA.")
            return

        tamp = (Nik, Nama_Lengkap, Gol_Darah, Tempat_Lahir, Tanggal_Lahir, Jenis_Kelamin, Agama, Status_Kawin, Pekerjaan, Provinsi, Kabupaten, Kecamatan, Kelurahan, Dusun, Kewarganegaraan)
        sql = """INSERT INTO tb_ktp (Nik, Nama_Lengkap, Gol_Darah, Tempat_Lahir, Tanggal_Lahir, Jenis_Kelamin, Agama, Status_Kawin, Pekerjaan, Provinsi, Kabupaten, Kecamatan, Kelurahan, Dusun, Kewarganegaraan)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(sql, tamp)
        db.commit()
        print("Data berhasil disimpan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        cursor.close()
        db.close()

def main():
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