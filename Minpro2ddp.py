import os
import sys
from prettytable import PrettyTable
import pwinput

# ==============================================================================
# DATASET & DATABASE (DICTIONARY & LIST)
# ==============================================================================

# Data Pengguna (Login System)
USERS = {
    "admin": {"password": "admin082", "role": "admin"},
    "user": {"password": "user147", "role": "user"}
}

# Database Menu Kopi (Nested Dictionary)
data_kopi = {
    "1": {"nama": "Cappucino", "kafein_mg": 75, "harga": 25000},
    "2": {"nama": "Iced Americano", "kafein_mg": 120, "harga": 22000},
    "3": {"nama": "Espresso (Double Shot)", "kafein_mg": 126, "harga": 25000},
    "4": {"nama": "Kopi Tubruk", "kafein_mg": 100, "harga": 8000}
}

# List Penyimpanan Riwayat Transaksi Konsumsi User
riwayat_konsumsi = []


# ==============================================================================
# UTILITY FUNCTIONS & VALIDASI INPUT (ERROR HANDLING)
# ==============================================================================

def bersihkan_layar():
    """Menggunakan library 'os' untuk membersihkan terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def input_integer(prompt):
    """Validasi input angka bulat positif menggunakan try-except"""
    while True:
        try:
            nilai = int(input(prompt))
            if nilai < 0:
                print(" Error: Nilai tidak boleh negatif!")
                continue
            return nilai
        except ValueError:
            print(" Error: Input harus berupa angka bulat!")


def input_pilihan(prompt, valid_options):
    """Validasi input pilihan menu sesuai opsi yang tersedia"""
    while True:
        pilihan = input(prompt).strip()
        if pilihan in valid_options:
            return pilihan
        print(" Error: Pilihan tidak valid, silakan coba lagi!")


# ==============================================================================
# AUTHENTICATION SYSTEM (LOGIN USER & ADMIN)
# ==============================================================================

def system_login():
    """Fungsi login multi-role dengan masking password menggunakan 'pwinput'"""
    bersihkan_layar()
    print("=============================================")
    print("   SYSTEM LOGIN - KALKULATOR COFFEE & KAFEIN  ")
    print("=============================================")
    
    percobaan = 0
    while percobaan < 3:
        username = input("Username : ").strip()
        # Menggunakan library pwinput untuk menyembunyikan input password
        password = pwinput.pwinput(prompt="Password : ", mask="*").strip()
        
        if username in USERS and USERS[username]["password"] == password:
            print(f"\n Login berhasil! Selamat datang, {username} ({USERS[username]['role'].upper()}).")
            input("\nTekan Enter untuk melanjutkan...")
            return USERS[username]["role"], username
        else:
            percobaan += 1
            print(f" Username atau password salah! Sisa percobaan: {3 - percobaan}\n")
    
    print(" Akses ditolak. Program berhenti.")
    sys.exit()


# ==============================================================================
# TAMPILAN DATA (PRETTYTABLE)
# ==============================================================================

def tampilkan_menu_kopi():
    """Menampilkan daftar menu kopi menggunakan library 'PrettyTable'"""
    tabel = PrettyTable()
    tabel.field_names = ["ID", "Nama Kopi", "Kafein (mg)", "Harga (Rp)"]
    
    for id_kopi, detail in data_kopi.items():
        tabel.add_row([id_kopi, detail["nama"], f"{detail['kafein_mg']} mg", f"Rp {detail['harga']:,}"])
    
    print("\n=== DAFTAR MENU KOPI & KANDUNGAN KAFEIN ===")
    print(tabel)


# ==============================================================================
# FITUR ROLE USER (KALKULATOR & RIWAYAT)
# ==============================================================================

def hitung_efisiensi():
    """Menghitung total kafein dan estimasi pengeluaran konsumsi kopi"""
    bersihkan_layar()
    tampilkan_menu_kopi()
    
    pilihan = input_pilihan("\nPilih ID Kopi yang dikonsumsi: ", data_kopi.keys())
    jumlah = input_integer("Berapa cangkir yang diminum hari ini? ")
    
    kopi_pilihan = data_kopi[pilihan]
    total_kafein = kopi_pilihan["kafein_mg"] * jumlah
    total_biaya = kopi_pilihan["harga"] * jumlah
    
    # Batas aman konsumsi kafein harian dewasa (FDA = 400 mg)
    status = "Aman (Di bawah 400mg)" if total_kafein <= 400 else " Warning: Melebihi Batas Harian (400mg)!"
    
    catatan = {
        "nama": kopi_pilihan["nama"],
        "jumlah": jumlah,
        "total_kafein": total_kafein,
        "total_biaya": total_biaya,
        "status": status
    }
    riwayat_konsumsi.append(catatan)
    
    print("\n" + "=" * 50)
    print(" HASIL ANALISIS KONSUMSI ")
    print("=" * 50)
    print(f"Kopi Dipilih : {kopi_pilihan['nama']}")
    print(f"Jumlah Porsi : {jumlah} cangkir")
    print(f"Total Kafein : {total_kafein} mg")
    print(f"Status       : {status}")
    print(f"Total Biaya  : Rp {total_biaya:,}")
    print("=" * 50)


def lihat_riwayat():
    """Menampilkan riwayat transaksi konsumsi dalam bentuk PrettyTable"""
    bersihkan_layar()
    if not riwayat_konsumsi:
        print("\n Belum ada riwayat konsumsi tersimpan.")
        return
    
    tabel = PrettyTable()
    tabel.field_names = ["No", "Nama Kopi", "Porsi", "Total Kafein", "Total Biaya", "Status Health"]
    
    for idx, r in enumerate(riwayat_konsumsi, 1):
        tabel.add_row([idx, r["nama"], r["jumlah"], f"{r['total_kafein']} mg", f"Rp {r['total_biaya']:,}", r["status"]])
    
    print("\n=== RIWAYAT KONSUMSI KAFEIN USER ===")
    print(tabel)


# ==============================================================================
# FITUR ROLE ADMIN (CRUD LENGKAP)
# ==============================================================================

def tambah_menu():
    """CREATE: Menambah menu kopi baru ke dictionary"""
    bersihkan_layar()
    print("\n--- TAMBAH MENU KOPI BARU ---")
    new_id = str(len(data_kopi) + 1)
    nama = input("Masukkan nama kopi baru    : ").strip()
    kafein = input_integer("Masukkan kadar kafein (mg) : ")
    harga = input_integer("Masukkan harga kopi (Rp)   : ")
    
    data_kopi[new_id] = {"nama": nama, "kafein_mg": kafein, "harga": harga}
    print(f"\n Menu '{nama}' berhasil ditambahkan dengan ID {new_id}!")


def ubah_menu():
    """UPDATE: Memperbarui data menu kopi yang sudah ada"""
    bersihkan_layar()
    tampilkan_menu_kopi()
    pilihan = input_pilihan("\nPilih ID menu yang ingin diubah: ", data_kopi.keys())
    
    print(f"\nMengubah menu ID [{pilihan}] - '{data_kopi[pilihan]['nama']}'")
    nama = input("Nama baru (tekan enter jika tidak diubah)   : ").strip()
    kafein_str = input("Kafein/mg (tekan enter jika tidak diubah) : ").strip()
    harga_str = input("Harga/Rp (tekan enter jika tidak diubah)  : ").strip()
    
    if nama:
        data_kopi[pilihan]["nama"] = nama
    if kafein_str.isdigit():
        data_kopi[pilihan]["kafein_mg"] = int(kafein_str)
    if harga_str.isdigit():
        data_kopi[pilihan]["harga"] = int(harga_str)
        
    print(f"\n Menu ID {pilihan} berhasil diperbarui!")


def hapus_menu():
    """DELETE: Menghapus menu kopi dari dictionary"""
    bersihkan_layar()
    tampilkan_menu_kopi()
    pilihan = input_pilihan("\nPilih ID menu yang ingin dihapus: ", data_kopi.keys())
    
    nama_kopi = data_kopi[pilihan]["nama"]
    del data_kopi[pilihan]
    print(f"\n Menu '{nama_kopi}' berhasil dihapus!")


# ==============================================================================
# ALUR UTAMA PROGRAM (MAIN FUNCTION)
# ==============================================================================

def main():
    role, username = system_login()
    
    while True:
        bersihkan_layar()
        print("=========================================")
        print(f" MENU UTAMA ({role.upper()}: {username})")
        print("=========================================")
        
        # MENU UNTUK ROLE USER
        if role == "user":
            print("1. Hitung Konsumsi & Efisiensi Kafein")
            print("2. Lihat Daftar Menu Kopi")
            print("3. Lihat Riwayat Konsumsi")
            print("4. Keluar Program")
            
            pilihan = input_pilihan("\nPilih menu (1-4): ", ["1", "2", "3", "4"])
            if pilihan == "1":
                hitung_efisiensi()
            elif pilihan == "2":
                bersihkan_layar()
                tampilkan_menu_kopi()
            elif pilihan == "3":
                lihat_riwayat()
            elif pilihan == "4":
                print("\nTerima kasih telah menggunakan Kalkulator Kafein!")
                break
            
            input("\nTekan Enter untuk kembali ke menu...")
                
        # MENU UNTUK ROLE ADMIN (CRUD)
        elif role == "admin":
            print("1. Lihat Semua Menu Kopi (Read)")
            print("2. Tambah Menu Kopi Baru (Create)")
            print("3. Ubah Data Menu Kopi (Update)")
            print("4. Hapus Menu Kopi (Delete)")
            print("5. Keluar Program")
            
            pilihan = input_pilihan("\nPilih menu (1-5): ", ["1", "2", "3", "4", "5"])
            if pilihan == "1":
                bersihkan_layar()
                tampilkan_menu_kopi()
            elif pilihan == "2":
                tambah_menu()
            elif pilihan == "3":
                ubah_menu()
            elif pilihan == "4":
                hapus_menu()
            elif pilihan == "5":
                print("\nTerima kasih telah menggunakan sistem admin!")
                break
                
            input("\nTekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()
