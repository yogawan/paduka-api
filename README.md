
# Instalasi Virtual Environment dengan `python3 -m venv`

Panduan ini menjelaskan cara mengatur lingkungan virtual Python menggunakan modul `venv`. Virtual environment memungkinkan Anda mengelola dependensi Python secara terpisah untuk setiap proyek.

## Langkah-langkah Instalasi

### 1. Pastikan Python 3 Terinstal
Pastikan Anda telah menginstal Python 3 di sistem Anda. Cek versi Python dengan menjalankan perintah berikut di terminal:

```bash
python3 --version
```

Jika belum terinstal, unduh dan instal Python 3 dari [python.org](https://www.python.org/downloads/).

### 2. Membuat Virtual Environment
Jalankan perintah berikut untuk membuat virtual environment:

```bash
python3 -m venv .venv
```

- **`.venv`**: Nama folder yang akan digunakan untuk menyimpan virtual environment. Anda dapat mengganti nama ini jika diperlukan.

### 3. Mengaktifkan Virtual Environment
Setelah virtual environment dibuat, Anda perlu mengaktifkannya. Aktivasi berbeda tergantung pada sistem operasi Anda:

#### **Di Linux/MacOS**
```bash
source .venv/bin/activate
```

#### **Di Windows (Command Prompt)**
```cmd
.venv\Scripts\activate
```

#### **Di Windows (PowerShell)**
```powershell
.venv\Scripts\Activate.ps1
```

Setelah aktivasi berhasil, Anda akan melihat nama virtual environment (misalnya, `.venv`) di awal prompt terminal Anda.

### 4. Menginstal Dependensi
Setelah virtual environment aktif, Anda dapat menginstal dependensi yang diperlukan untuk proyek Anda menggunakan `pip`. Misalnya:

```bash
pip install -r requirements.txt
```

### 5. Menonaktifkan Virtual Environment
Jika Anda sudah selesai bekerja di dalam virtual environment, Anda dapat menonaktifkannya dengan menjalankan perintah:

```bash
deactivate
```

## Troubleshooting
Jika Anda menghadapi masalah selama proses instalasi atau penggunaan, berikut adalah beberapa langkah pemecahan masalah:

1. **Python Tidak Ditemukan**  
   Pastikan Python 3 sudah terinstal dan ditambahkan ke variabel lingkungan `PATH`.

2. **Modul `venv` Tidak Tersedia**  
   Di beberapa distribusi Linux, modul `venv` mungkin belum diinstal secara default. Anda dapat menginstalnya dengan perintah berikut:
   ```bash
   sudo apt install python3-venv
   ```

3. **Aktivasi di Windows Gagal**  
   Jika menggunakan PowerShell dan muncul error terkait izin, jalankan perintah berikut untuk mengubah kebijakan eksekusi:
   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   ```

## Referensi
- [Python Documentation - venv](https://docs.python.org/3/library/venv.html)
- [Python Downloads](https://www.python.org/downloads/)
