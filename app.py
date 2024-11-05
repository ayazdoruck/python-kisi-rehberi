import tkinter as tk
from tkinter import messagebox
import json

rehber_dizi = []
add_form_open = False

def load_contacts():
    global rehber_dizi
    try:
        with open("rehber.json", "r") as file:
            rehber_dizi = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        rehber_dizi = []

def save_contacts():
    with open("rehber.json", "w") as file:
        json.dump(rehber_dizi, file, indent=4)

def update_listbox():
    listbox.delete(0, tk.END)
    for i, kisi in enumerate(rehber_dizi):
        listbox.insert(tk.END, f"ID {i}: {kisi['ad']} {kisi['soyad']} - {kisi['no']}")

def open_add_contact_form():
    global add_form_open
    if add_form_open:
        return
    add_form_open = True

    form = tk.Toplevel(root)
    form.title("Yeni Kişi Ekle")
    form.configure(bg="#2B2B2B")

    tk.Label(form, text="Ad:", bg="#2B2B2B", fg="white", font=("Inter", 12)).grid(row=0, column=0, padx=10, pady=5)
    ad_entry = tk.Entry(form, bg="#3B3B3B", fg="white", insertbackground='white', font=("Inter", 12))
    ad_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form, text="Soyad:", bg="#2B2B2B", fg="white", font=("Inter", 12)).grid(row=1, column=0, padx=10, pady=5)
    soyad_entry = tk.Entry(form, bg="#3B3B3B", fg="white", insertbackground='white', font=("Inter", 12))
    soyad_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form, text="Numara:", bg="#2B2B2B", fg="white", font=("Inter", 12)).grid(row=2, column=0, padx=10, pady=5)
    no_entry = tk.Entry(form, bg="#3B3B3B", fg="white", insertbackground='white', font=("Inter", 12))
    no_entry.grid(row=2, column=1, padx=10, pady=5)

    def add_contact():
        ad = ad_entry.get()
        soyad = soyad_entry.get()
        try:
            no = int(no_entry.get())
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz numara. Lütfen tekrar deneyin.")
            return

        rehber_dizi.append({"ad": ad, "soyad": soyad, "no": no})
        save_contacts()
        update_listbox()
        messagebox.showinfo("Başarılı", "Kişi başarıyla eklendi!")
        close_add_form(form)

    form.protocol("WM_DELETE_WINDOW", lambda: close_add_form(form))
    tk.Button(form, text="Kaydet", command=add_contact, bg="#4D4D4D", fg="white", font=("Inter", 12), activebackground="#5A5A5A").grid(row=3, column=0, columnspan=2, pady=10)

def close_add_form(form):
    global add_form_open
    add_form_open = False
    form.destroy()

def delete_contact():
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Uyarı", "Silmek için bir kişi seçin.")
        return

    if messagebox.askyesno("Onay", "Bu kişiyi silmek istediğinize emin misiniz?"):
        rehber_dizi.pop(selected_index[0])
        save_contacts()
        update_listbox()
        messagebox.showinfo("Başarılı", "Kişi başarıyla silindi!")

def open_edit_contact_form():
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Uyarı", "Düzenlemek için bir kişi seçin.")
        return

    id = selected_index[0]
    kisi = rehber_dizi[id]

    form = tk.Toplevel(root)
    form.title("Kişi Düzenle")
    form.configure(bg="#2B2B2B")

    tk.Label(form, text="Ad:", bg="#2B2B2B", fg="white", font=("Inter", 12)).grid(row=0, column=0, padx=10, pady=5)
    ad_entry = tk.Entry(form, bg="#3B3B3B", fg="white", insertbackground='white', font=("Inter", 12))
    ad_entry.insert(0, kisi["ad"])
    ad_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form, text="Soyad:", bg="#2B2B2B", fg="white", font=("Inter", 12)).grid(row=1, column=0, padx=10, pady=5)
    soyad_entry = tk.Entry(form, bg="#3B3B3B", fg="white", insertbackground='white', font=("Inter", 12))
    soyad_entry.insert(0, kisi["soyad"])
    soyad_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form, text="Numara:", bg="#2B2B2B", fg="white", font=("Inter", 12)).grid(row=2, column=0, padx=10, pady=5)
    no_entry = tk.Entry(form, bg="#3B3B3B", fg="white", insertbackground='white', font=("Inter", 12))
    no_entry.insert(0, kisi["no"])
    no_entry.grid(row=2, column=1, padx=10, pady=5)

    def edit_contact():
        yeni_ad = ad_entry.get()
        yeni_soyad = soyad_entry.get()
        try:
            yeni_no = int(no_entry.get())
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz numara. Lütfen tekrar deneyin.")
            return

        kisi["ad"] = yeni_ad
        kisi["soyad"] = yeni_soyad
        kisi["no"] = yeni_no
        save_contacts()
        update_listbox()
        messagebox.showinfo("Başarılı", "Kişi bilgileri güncellendi!")
        form.destroy()

    tk.Button(form, text="Kaydet", command=edit_contact, bg="#4D4D4D", fg="white", font=("Inter", 12), activebackground="#5A5A5A").grid(row=3, column=0, columnspan=2, pady=10)

root = tk.Tk()
root.title("Rehber Uygulaması")
root.iconphoto(False, tk.PhotoImage(file='icon.png'))
root.configure(bg="#2B2B2B")

frame = tk.Frame(root, bg="#2B2B2B")
frame.pack(pady=10)

listbox = tk.Listbox(frame, width=50, height=15, bg="#3B3B3B", fg="white", selectbackground="#5A5A5A", font=("Inter", 12))
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

button_frame = tk.Frame(root, bg="#2B2B2B")
button_frame.pack(pady=10)

icon_add = tk.PhotoImage(file="icon_add.png")
icon_delete = tk.PhotoImage(file="icon_delete.png")
icon_edit = tk.PhotoImage(file="icon_edit.png")

add_button = tk.Button(button_frame, image=icon_add, command=open_add_contact_form, borderwidth=0, highlightthickness=0, bg="#2B2B2B", activebackground="#3B3B3B")
add_button.grid(row=0, column=0, padx=5)

delete_button = tk.Button(button_frame, image=icon_delete, command=delete_contact, borderwidth=0, highlightthickness=0, bg="#2B2B2B", activebackground="#3B3B3B")
delete_button.grid(row=0, column=1, padx=5)

edit_button = tk.Button(button_frame, image=icon_edit, command=open_edit_contact_form, borderwidth=0, highlightthickness=0, bg="#2B2B2B", activebackground="#3B3B3B")
edit_button.grid(row=0, column=2, padx=5)

load_contacts()
update_listbox()

footer_label = tk.Label(root, text="Ayaz Doruk Şenel", bg="#2B2B2B", fg="#616169", font=("Inter", 12))
footer_label.pack(side=tk.BOTTOM, pady=(10, 0))

root.geometry("500x520")
root.resizable(False, False)
root.mainloop()
