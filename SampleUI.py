import tkinter as tk
from tkinter import filedialog

def login():
    if name_entry.get() == "dewhaan" and password_entry.get() == "Dewhaan24":
        login_frame.pack_forget()
        show_main_menu()

def show_main_menu():
    main_menu_frame.pack(expand=True, fill="both")

def show_encryption_page():
    main_menu_frame.pack_forget()
    encryption_frame.pack(expand=True, fill="both")

def select_file_and_encrypt():
    file_path = filedialog.askopenfilename()
    if file_path:
        encrypt_file(file_path)

def encrypt_file(file_path):
    # Implement encryption logic here
    pass

root = tk.Tk()
root.title("Medical File Encryption App")
root.configure(bg="white")

login_frame = tk.Frame(root, bg="white")
main_menu_frame = tk.Frame(root, bg="white")
encryption_frame = tk.Frame(root, bg="white")

# ... (Rest of the code)

# Main Menu Page
encrypt_button = tk.Button(main_menu_frame, text="Encrypt", command=show_encryption_page, bg="blue", fg="white")
decrypt_button = tk.Button(main_menu_frame, text="Decrypt", command=show_main_menu, bg="blue", fg="white")
integrity_button = tk.Button(main_menu_frame, text="Check Integrity", command=show_main_menu, bg="blue", fg="white")

encrypt_button.pack(padx=20, pady=20, fill="x")
decrypt_button.pack(padx=20, pady=20, fill="x")
integrity_button.pack(padx=20, pady=20, fill="x")

# ... (Rest of the code)
# Login Page
login_label = tk.Label(login_frame, text="Login", font=("Helvetica", 16), bg="white")
name_label = tk.Label(login_frame, text="Name:", bg="white")
password_label = tk.Label(login_frame, text="Password:", bg="white")
name_entry = tk.Entry(login_frame)
password_entry = tk.Entry(login_frame, show="*")
login_button = tk.Button(login_frame, text="Login", command=login, bg="#417285", fg="white")

login_label.pack(pady=20)
name_label.pack()
name_entry.pack(pady=5)
password_label.pack()
password_entry.pack(pady=10)
login_button.pack()

# Main Menu Page
encrypt_button = tk.Button(main_menu_frame, text="Encrypt", command=show_encryption_page, bg="#417285", fg="white")
decrypt_button = tk.Button(main_menu_frame, text="Decrypt", command=show_main_menu, bg="#417285", fg="white")
integrity_button = tk.Button(main_menu_frame, text="Check Integrity", command=show_main_menu, bg="#417285", fg="white")

encrypt_button.pack(padx=20, pady=20, fill="x")
decrypt_button.pack(padx=20, pady=20, fill="x")
integrity_button.pack(padx=20, pady=20, fill="x")

login_frame.pack(expand=True, fill="both")

# Encryption Page
encryption_label = tk.Label(encryption_frame, text="Encryption", font=("Helvetica", 16), bg="white")
select_file_button = tk.Button(encryption_frame, text="Select File", command=select_file_and_encrypt, bg="#417285", fg="white")
encrypt_button = tk.Button(encryption_frame, text="Encrypt", command=encrypt_file, bg="#417285", fg="white")

encryption_label.pack(pady=20)
select_file_button.pack(padx=20, pady=10, fill="x")
encrypt_button.pack(padx=20, pady=10, fill="x")

root.mainloop()
