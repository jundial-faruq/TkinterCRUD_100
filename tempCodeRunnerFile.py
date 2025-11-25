

import tkinter as tk;
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect("nilai_siswa.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_siswa TEXT,
    biologi INTEGER,
    fisika INTEGER,
    inggris INTEGER,
    prediksi_fakultas TEXT
)
""")
conn.commit()

# ===================== DATABASE =====================
conn = sqlite3.connect("nilai_siswa.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_siswa TEXT,
    biologi INTEGER,
    fisika INTEGER,
    inggris INTEGER,
    prediksi_fakultas TEXT
)
""")
conn.commit()


# ===================== FUNGSI PREDIKSI =====================
def hitung_prediksi(bio, fis, ing):
    if bio > fis and bio > ing:
        return "Kedokteran"
    elif fis > bio and fis > ing:
        return "Teknik"
    else:
        return "Bahasa"


# ===================== FUNGSI CRUD =====================
def submit_data():
    nama = ent_nama.get()
    bio = int(ent_bio.get() or 0)
    fis = int(ent_fis.get() or 0)
    ing = int(ent_ing.get() or 0)

    pred = hitung_prediksi(bio, fis, ing)

    c.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, pred))
    conn.commit()

    messagebox.showinfo("Success", "Data berhasil disimpan!")
    tampilkan_data()


def update_data():
    id_data = ent_id.get()
    if id_data == "":
        messagebox.showwarning("Error", "ID harus diisi untuk update!")
        return

    nama = ent_nama.get()
    bio = int(ent_bio.get() or 0)
    fis = int(ent_fis.get() or 0)
    ing = int(ent_ing.get() or 0)
    pred = hitung_prediksi(bio, fis, ing)

    c.execute("""
        UPDATE nilai_siswa
        SET nama_siswa=?, biologi=?, fisika=?, inggris=?, prediksi_fakultas=?
        WHERE id=?
    """, (nama, bio, fis, ing, pred, id_data))
    conn.commit()

    messagebox.showinfo("Success", "Data berhasil diupdate!")
    tampilkan_data()


def delete_data():
    id_data = ent_id.get()
    if id_data == "":
        messagebox.showwarning("Error", "ID harus diisi untuk delete!")
        return

    c.execute("DELETE FROM nilai_siswa WHERE id=?", (id_data,))
    conn.commit()

    messagebox.showinfo("Success", "Data berhasil dihapus!")
    tampilkan_data()


# ===================== FUNGSI TABEL =====================
def tampilkan_data():
    for row in tree.get_children():
        tree.delete(row)

    c.execute("SELECT * FROM nilai_siswa")
    rows = c.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)


def pilih_data(event):
    selected = tree.focus()
    if selected == "":
        return

    values = tree.item(selected, "values")

    ent_id.delete(0, tk.END)
    ent_id.insert(0, values[0])

    ent_nama.delete(0, tk.END)
    ent_nama.insert(0, values[1])

    ent_bio.delete(0, tk.END)
    ent_bio.insert(0, values[2])

    ent_fis.delete(0, tk.END)
    ent_fis.insert(0, values[3])

    ent_ing.delete(0, tk.END)
    ent_ing.insert(0, values[4])


# ===================== GUI TKINTER =====================
root = tk.Tk()
root.title("Aplikasi Prediksi Prodi + Database SQLite")
root.geometry("850x700")

judul = tk.Label(root, text="Aplikasi Prediksi Prodi Pilihan",
                 font=("Montserrat", 20, "bold"))
judul.pack(pady=10)


# ===================== FORM INPUT =====================
frame_form = tk.Frame(root)
frame_form.pack(pady=10)

# ID
tk.Label(frame_form, text="ID (Update/Delete)").grid(row=0, column=0, padx=10, pady=5)
ent_id = tk.Entry(frame_form)
ent_id.grid(row=0, column=1, padx=10, pady=5)

# Nama
tk.Label(frame_form, text="Nama Siswa").grid(row=1, column=0, padx=10, pady=5)
ent_nama = tk.Entry(frame_form)
ent_nama.grid(row=1, column=1, padx=10, pady=5)

# Biologi
tk.Label(frame_form, text="Biologi").grid(row=2, column=0, padx=10, pady=5)
ent_bio = tk.Entry(frame_form)
ent_bio.grid(row=2, column=1, padx=10, pady=5)

# Fisika
tk.Label(frame_form, text="Fisika").grid(row=3, column=0, padx=10, pady=5)
ent_fis = tk.Entry(frame_form)
ent_fis.grid(row=3, column=1, padx=10, pady=5)

# Inggris
tk.Label(frame_form, text="Inggris").grid(row=4, column=0, padx=10, pady=5)
ent_ing = tk.Entry(frame_form)
ent_ing.grid(row=4, column=1, padx=10, pady=5)


# ===================== BUTTON =====================
frame_btn = tk.Frame(root)
frame_btn.pack(pady=10)

btn_submit = tk.Button(frame_btn, text="Submit", width=12, command=submit_data)
btn_submit.grid(row=0, column=0, padx=10)

btn_update = tk.Button(frame_btn, text="Update", width=12, command=update_data)
btn_update.grid(row=0, column=1, padx=10)

btn_delete = tk.Button(frame_btn, text="Delete", width=12, command=delete_data)
btn_delete.grid(row=0, column=2, padx=10)

btn_refresh = tk.Button(frame_btn, text="Refresh Tabel", width=12, command=tampilkan_data)
btn_refresh.grid(row=0, column=3, padx=10)


# ===================== TABEL TREEVIEW =====================
kolom = ("ID", "Nama Siswa", "Biologi", "Fisika", "Inggris", "Prediksi")

tree = ttk.Treeview(root, columns=kolom, show="headings", height=10)

for col in kolom:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(pady=10)

# Klik tabel = isi form
tree.bind("<ButtonRelease-1>", pilih_data)

# Load tabel pertama kali
tampilkan_data()

root.mainloop()
