import tkinter as tk;
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

root = tk.Tk()
root.geometry("800x800")
root.title("Aplikasi Prediksi Prodi")

judul = tk.Label(root, text="Prediksi Fakultas", font="Montserrat 20 bold")
judul.pack(pady=10, ipadx=20)

data_entries = {}

labels = ["Nama Siswa", "Biologi", "Fisika", "Inggris"]
for label in labels:
    lbl = tk.Label(root, text=label, font=("Montserrat", 12))
    lbl.pack(pady=5)
    ent = tk.Entry(root)
    ent.pack(pady=5)
    data_entries[label.lower().replace(" ", "_")] = ent

hasil_label = tk.Label(root, text="", font=("Montserrat", 14, "bold"))
hasil_label.pack(pady=20)


def prediksi():
    nama = data_entries["nama_siswa"].get()
    biologi = int(data_entries["biologi"].get() or 0)
    fisika = int(data_entries["fisika"].get() or 0)
    inggris = int(data_entries["inggris"].get() or 0)

    # Tentukan prediksi
    if biologi > fisika and biologi > inggris:
        pred = "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        pred = "Teknik"
    else:
        pred = "Bahasa"

    # Simpan ke database
    c.execute(
        "INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) VALUES (?, ?, ?, ?, ?)",
        (nama, biologi, fisika, inggris, pred)
    )
    conn.commit()

    hasil_label.config(text=f"Prediksi: {pred}")


# ================= SUBMIT BUTTON =================
submit_btn = tk.Button(root, text="Submit", font=("Montserrat", 12), command=prediksi)
submit_btn.pack(pady=15)

root.mainloop()
