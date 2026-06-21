import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import subprocess
import os
import random
import hashlib
import webbrowser

# Function to authenticate the user
def authenticate_user():
    # Check if account details exist
    if os.path.exists("account_details.txt"):
        with open("account_details.txt", "r") as acc_file:
            stored_username, stored_password_hash = acc_file.read().splitlines()

        # Prompt the user for username and password
        username = simpledialog.askstring("Authentication", "Enter your username:")
        password = simpledialog.askstring("Authentication", "Enter your password:", show='*')

        # Hash the entered password for comparison
        entered_password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Check if the entered credentials match stored values
        if username == stored_username and entered_password_hash == stored_password_hash:
            create_option_selection_ui()
        else:
            messagebox.showerror("Authentication Failed", "Invalid username or password. Please try again.")
    else:
        # If account details don't exist, create a new account
        create_new_account()

# Function to create a new account
def create_new_account():
    username = simpledialog.askstring("New Account", "Create a username:")
    password = simpledialog.askstring("New Account", "Create a password:", show='*')

    # Hash the password before saving
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Save the account details to a file
    with open("account_details.txt", "w") as acc_file:
        acc_file.write(f"{username}\n{password_hash}")

    create_option_selection_ui()


# Function to create the option selection UI (2nd UI)
def create_option_selection_ui():
    welcome_frame.pack_forget()
    option_selection_frame.pack()

# Read all the predefined random keys from random.txt and convert them from hexadecimal to bytes
predefined_keys = []

with open("random.txt", "r") as key_file:
    for line in key_file:
        key_hex = line.strip()
        if key_hex:
            key_bytes = bytes.fromhex(key_hex)
            predefined_keys.append(key_bytes)

# Encryption part
def encryption_process(file_path, key):
    cipher = AES.new(key, AES.MODE_EAX)
    with open(file_path, 'rb') as file:
        plaintext = file.read()
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    with open(file_path + ".ecry", 'wb') as enc_file:
        enc_file.write(cipher.nonce)
        enc_file.write(tag)
        enc_file.write(ciphertext)
    os.remove(file_path)

# Decryption part
def decryption_process(file_path, key):
    with open(file_path, 'rb') as enc_file:
        nonce = enc_file.read(16)
        tag = enc_file.read(16)
        ciphertext = enc_file.read()
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    with open(file_path[:-4], 'wb') as dec_file:
        dec_file.write(plaintext)
    os.remove(file_path)

# Function to create the option selection UI (2nd UI)
def create_option_selection_ui():
    welcome_frame.pack_forget()
    option_selection_frame.pack()

def select_option_1():
    create_option_1_ui()
    option_selection_frame.pack_forget()
    back_button.pack()  # Show the "Back" button

def select_option_2():
    create_option_2_ui()
    option_selection_frame.pack_forget()
    back_button.pack()  # Show the "Back" button

# Function to go back to the option selection UI
def go_back_to_option_selection():
    option1_frame.pack_forget()
    option2_frame.pack_forget()
    option_selection_frame.pack()
    back_button.pack_forget()  # Hide the "Back" button when back to option selection

# Function to create Option 1 UI
def create_option_1_ui():
    option1_frame.pack()
    
    file_label.pack()
    file_path_entry.pack()

    browse_files_button.pack(pady=5)
    encrypt_files_button.pack(side="left", pady=5, anchor="nw")
    upload_button.pack(pady=5)
    open_url_button.pack(pady=5)
    
    back_button.pack(pady=10)  # Show the "Back" button

def enable_encrypt_button():
    encrypt_files_button.config(state="normal")

# Function to create Option 2 UI
def create_option_2_ui():
    option2_frame.pack()
    
    file_label2.pack()
    file_path_entry2.pack()
    
    browse_files_button2.pack(pady=5)
    decrypt_files_button.pack(side="left", pady=5, anchor="nw")
    download_button.pack(pady=5)
    open_url_button2.pack(pady=5)
    
    back_button.pack(pady=10)  # Show the "Back" button

def enable_decrypt_button():
    decrypt_files_button.config(state="normal")

def select_files():
    file_paths = filedialog.askopenfilenames()  # Allow the user to select multiple files
    # Update the file_path_entry to display selected file paths
    file_path_entry.delete(1.0, tk.END)
    for file_path in file_paths:
        file_path_entry.insert(tk.END, file_path + "\n")
    enable_encrypt_button()  # Enable the Encryption button after selecting files

def select_files2():
    file_paths = filedialog.askopenfilenames()  # Allow the user to select multiple files
    # Update the file_path_entry2 to display selected file paths
    file_path_entry2.delete(1.0, tk.END)
    for file_path in file_paths:
        file_path_entry2.insert(tk.END, file_path + "\n")
    enable_decrypt_button()  # Enable the Decryption button after selecting files

def encrypt_files():
    file_paths = file_path_entry.get("1.0", tk.END).splitlines()  # Get selected file paths from the entry
    if not file_paths:
        return  # No files selected

    selected_key = random.choice(predefined_keys)
    for file_path in file_paths:
        if file_path:
            encryption_process(file_path, selected_key)
    file_path_entry.delete(1.0, tk.END)  # Clear the entry field after encryption
    upload_button.config(state="normal")  # Enable the Upload button
    messagebox.showinfo("Encryption", "Files encrypted with a randomly selected key.")

def decrypt_files():
    file_paths = file_path_entry2.get("1.0", tk.END).splitlines()  # Get selected file paths from the entry
    if not file_paths:
        return  # No files selected

    selected_key = random.choice(predefined_keys)
    for file_path in file_paths:
        if file_path and file_path.endswith('.ecry'):
            decryption_process(file_path, selected_key)
    file_path_entry2.delete(1.0, tk.END)  # Clear the entry field after decryption
    download_button.config(state="normal")  # Enable the Download button
    messagebox.showinfo("Decryption", "Files decrypted with a randomly selected key.")

def open_winscp():
    winscp_path = r'C:\Users\samod\AppData\Local\Programs\WinSCP\WinSCP.exe'  
    try:
        subprocess.Popen([winscp_path])
    except FileNotFoundError:
        messagebox.showerror("Error", "WinSCP not found. Please make sure WinSCP is installed and its executable path is set correctly.")

#def open_url():
 #   url = "https://notification.local/view.html"  
  #  webbrowser.open(url)

def open_url():
    url = "https://notification.local/view.html"  
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe" 
    try:
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get('chrome').open(url)
    except Exception as e:
        messagebox.showerror("Error", f"Error opening URL: {str(e)}")


# Main code...
window = tk.Tk()
window.title("Internal Encryption - Golden Key Hospital")
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))

#welcome_frame = tk.Frame(window, bg="cadetblue")
#welcome_frame.pack()

welcome_frame = tk.Frame(window, bg="cadetblue", width=window.winfo_screenwidth(), height=window.winfo_screenheight())
welcome_frame.pack_propagate(False)  # Prevent the frame from shrinking to fit its contents
welcome_frame.pack()

welcome_label = tk.Label(welcome_frame, text="Welcome to Golden Key Hospital", font=("Arial Black", 16), fg=("purple"), bg="pink")
welcome_label.pack(pady=20,anchor='center')

developed_by_label = tk.Label(welcome_frame, text="Developed by Group D", font=("Arial", 8))
developed_by_label.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=10)

# Replace the start_button command with authenticate_user
start_button = tk.Button(welcome_frame, text="Start", command=authenticate_user, borderwidth=0, highlightthickness=0)
start_button.pack(pady=13)

option_selection_frame = tk.Frame(window, bg="cadetblue")
option_var = tk.IntVar()
option_label = tk.Label(option_selection_frame, text="Select an option:", font=("Arial", 12))
option_label.pack(pady=25)

option1_button = tk.Button(option_selection_frame, text="Encryption", command=select_option_1)
option1_button.pack()

option2_button = tk.Button(option_selection_frame, text="Decryption", command=select_option_2)
option2_button.pack()

back_button = tk.Button(window, text="Back", command=go_back_to_option_selection, borderwidth=0, highlightthickness=0)

option1_frame = tk.Frame(window, bg="cadetblue")
option2_frame = tk.Frame(window, bg="cadetblue")

file_label = tk.Label(option1_frame, text="Selected Files:")
file_path_entry = tk.Text(option1_frame, width=50, height=5)
browse_files_button = tk.Button(option1_frame, text="Browse Files", command=select_files, borderwidth=0, highlightthickness=0)
browse_files_icon = tk.PhotoImage(file="/Users/chanuth/Desktop/E C U /3yr(1 sem)/Applied Project/final report/Icons/File.png")
browse_files_icon = browse_files_icon.subsample(15, 15)
browse_files_button.config(image=browse_files_icon, compound="left")

encrypt_files_button = tk.Button(option1_frame, text="Encrypt Files", command=encrypt_files, state="disabled", borderwidth=0, highlightthickness=0)
encrypt_files_icon = tk.PhotoImage(file="/Users/chanuth/Desktop/E C U /3yr(1 sem)/Applied Project/final report/Icons/encrypt.png")
encrypt_files_icon = encrypt_files_icon.subsample(15, 15)
encrypt_files_button.config(image=encrypt_files_icon, compound="left")

upload_icon = tk.PhotoImage(file="/Users/chanuth/Desktop/E C U /3yr(1 sem)/Applied Project/final report/Icons/upload.png")
upload_icon = upload_icon.subsample(18, 18)
upload_button = tk.Button(option1_frame, text="Upload",image=upload_icon, compound="left", command=open_winscp, state="disabled", borderwidth=0, highlightthickness=0)

open_url_button = tk.Button(option1_frame, text="Notifications from Admin", command=open_url, borderwidth=0, highlightthickness=0)
open_url_icon = tk.PhotoImage(file="/Users/chanuth/Desktop/E C U /3yr(1 sem)/Applied Project/final report/Icons/notification.png")
open_url_icon = open_url_icon.subsample(15, 15)
open_url_button.config(image=open_url_icon, compound="left")

# Decryption window
file_label2 = tk.Label(option2_frame, text="Selected Files:")
file_path_entry2 = tk.Text(option2_frame, width=50, height=5)

browse_files_button2 = tk.Button(option2_frame, text="Browse Files", command=select_files2, borderwidth=0, highlightthickness=0)
browse_files_icon2 = tk.PhotoImage(file="/Users/chanuth/Desktop/E C U /3yr(1 sem)/Applied Project/final report/Icons/File.png")
browse_files_icon2 = browse_files_icon2.subsample(15, 15)
browse_files_button2.config(image=browse_files_icon2, compound="left")

decrypt_files_button = tk.Button(option2_frame, text="Decrypt Files", command=decrypt_files, state="disabled", borderwidth=0, highlightthickness=0)
decrypt_files_icon = tk.PhotoImage(file="/Users/chanuth/Desktop/E C U /3yr(1 sem)/Applied Project/final report/Icons/decrypt.png")
decrypt_files_icon = decrypt_files_icon.subsample(15, 15)
decrypt_files_button.config(image=decrypt_files_icon, compound="left")

download_icon = tk.PhotoImage(file="/Users/chanuth/Desktop/E C U /3yr(1 sem)/Applied Project/final report/Icons/download.png")
download_icon = download_icon.subsample(20, 20)
download_button = tk.Button(option2_frame, text="Download", image=download_icon, compound="left", command=open_winscp, state="disabled", borderwidth=0, highlightthickness=0)

open_url_button2 = tk.Button(option2_frame, text="Notifications from Admin", command=open_url, borderwidth=0, highlightthickness=0)
open_url_icon2 = tk.PhotoImage(file="/Users/chanuth/Desktop/E C U /3yr(1 sem)/Applied Project/final report/Icons/notification.png")
open_url_icon2 = open_url_icon.subsample(15, 15)
open_url_button2.config(image=open_url_icon, compound="left")

window.mainloop()
