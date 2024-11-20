# Import library buat database dan GUI
import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')    # Membuka atau membuat file database SQLite
    cursor = conn.cursor()                      # Membuat cursor untuk menjalankan perintah SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (   
            id INTEGER PRIMARY KEY AUTOINCREMENT,   
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')  
    conn.commit()   # Menyimpan perubahan ke database
    conn.close()    # Menutup koneksi database

#Fungsu ini untuk mengambil semua data dari tabel
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db') # Membuka koneksi database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")  # Mengambil semua data dari tabel
    rows = cursor.fetchall() # Menyimpan hasil query ke dalam variabel
    conn.close() #Menutup koneksi database
    return rows #Mengembalikan hasil data

#Fungsi ini untuk menyimpan data siswa ke dalam tabel
def save_to_database(nama, biologi, fisika, inggris, prediksi): 
    conn = sqlite3.connect('nilai_siswa.db') # Membuka koneksi database
    cursor = conn.cursor()
    #memasukkan query sql ke data baru
    cursor.execute(''' 
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))  #masukan data ke tabel
    conn.commit() #Menyimpan perubahan ke database
    conn.close() #menutup koneksi database 

def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db') # Membuka database
    cursor = conn.cursor()
    #memasukkan query sql update data berdasarkan ID
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id)) #Mengupdate data
    conn.commit() #Menyimpan perubahan ke database
    conn.close()    #menutup koneksi database 

def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db') #Membuka database
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,)) #Untuk hapus data
    conn.commit() #menyimpan perubahan ke database
    conn.close() #menutup koneksi database

#Fungsi buat hitung fakultas berdasarkan nilai tertinggi
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:  # Jika nilai Biologi lebih tinggi atau sama dengan Fisika dan Inggris
        return "Kedokteran"                     # Prediksi fakultas adalah kedokteran jika Biologi tertinggi
    elif fisika > biologi and fisika > inggris: # Jika nilai Fisika lebih tinggi atau sama dengan Biologi dan Inggris
        return "Teknik"                         # Prediksi fakultas adalah teknik jika Fisika tertinggi
    elif inggris > biologi and inggris > fisika:#Jika nilai Inggris lebih tinggi atau sama dengan Biologi dan Fisika
        return "Bahasa"                         #Prediksi fakultas adalah bahasa jika Inggris tertinggi
    else:
        return "Tidak Diketahui" # Jika tidak ada nilai tertinggi yang jelas

# Fungsi buat menambahkan data baru ke database dari form input
def submit():
    try:
        nama = nama_var.get() #Ambil nama siswa 
        biologi = int(biologi_var.get()) #Mengambil nilai biologi
        fisika = int(fisika_var.get()) #Mengambil nilai fisika 
        inggris = int(inggris_var.get()) #mengambil nilai inggris
        
        #mengecek kalo nama kosong
        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")
        
        prediksi = calculate_prediction(biologi, fisika, inggris) # Prediksi fakultas berdasarkan nilai
        save_to_database(nama, biologi, fisika, inggris, prediksi) # Simpen data ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}") # Menampilkan pesan sukses
        clear_inputs() #Kosongkan input form
        populate_table() #Update tabel GUI
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

#Fungsi untuk membuat update data 
def update():
    try:
        if not selected_record_id.get():  
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get()) # Ambil ID data yang dipilih
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris) # Hitung ulang prediksi fakultas
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Update data di database

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs() #membersihkan input
        populate_table() #update tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

#Fungsi untuk menghapus data 
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get()) # Ambil ID data yang mau dihapus
        delete_database(record_id) # Hapus data dari database
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs() # Kosongkan input form
        populate_table() # Update tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi buat kosongkan form input
def clear_inputs():
    nama_var.set("") # Mengosongkan input nama
    biologi_var.set("") # Mengosongkan input biologi 
    fisika_var.set("") # Mengosongkan input fisika
    inggris_var.set("") # Mengosongkan input inggris
    selected_record_id.set("") # Kosongkan ID data yang dipilih

 #Fungsi buat isi ulang tabel dengan data terbaru dari database
def populate_table():
    # Hapus semua isi tabel di GUI
    for row in tree.get_children(): 
        tree.delete(row)
    # Ambil data dari database
    for row in fetch_data():
        tree.insert('', 'end', values=row)

def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0] #mengambil item yang dipilih
        selected_row = tree.item(selected_item)['values'] #mengambil nilai dari item 

        #mengisi form dengan data yang dipilih
        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel input data tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center') 

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

populate_table()

root.mainloop()