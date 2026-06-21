import tkinter as tk
from tkinter import simpledialog,filedialog,messagebox
from tkinter import Tk, Frame, Label, Button, PhotoImage
import subprocess
from Crypto.Cipher import AES
import os, random, hashlib, webbrowser

# User Authentication

def authenticate_user():
    # Check whther the account exist
    if os.path.exists("user_account.txt"):
        with open("user_account.txt", "r") as acc_file:
            store_Username, store_Password_hash = acc_file.read().splitlines()
        
        # Ask user to enter the username and password
        Username = simpledialog.askstring("User Authentication", "Enter the Username: " )
        Password = simpledialog.askstring("User Authentication", "Enter the Password: " , show = '*' )
        
        #convert the entered passowrd to hash value for compare
        entered_Password_hash = hashlib.sha256(Password.encode()).hexdigest()

        #Check the entered and store usernames and passwords hash value matches
        if Username == store_Username and entered_Password_hash == store_Password_hash:
            Option_selection_window()
        else:
            messagebox.showerror("User Authentication Failed", "Invalid Username or Passowrd!! Please Try again.")

    else:
        #if the account dosent exixst, Create a new user account
        create_new_useraccount()            

def create_new_useraccount():

    # Ask user to enter a username and password to create a useraccount
    Username = simpledialog.askstring("Create New Account", "Enter the Username: " )
    Password = simpledialog.askstring("Create New Account", "Enter the Password: " , show = '*' )

    #convert the entered passowrd to hash value for compare
    Password_hash = hashlib.sha256(Password.encode()).hexdigest()

    #save the created user account details to a text file.
    with open("user_account.txt","w") as acc_file:
        acc_file.write(f"{Username}\n{Password_hash}")
    #Once the account is created , auto direct to the option selction window
    Option_selection_window()    


# ---------------------------------- Encryption / Decryption ------------------------------------

#Read all the random keys that arw in the random txt file and convert them to bytes form hexadecimal
random_key = []
with open("Random_key.txt","r") as Rankey_file:
    for line in Rankey_file:
        Rankey_hex = line.strip()
        if Rankey_hex:
            Rankey_bytes = bytes.fromhex(Rankey_hex)
            random_key.append(Rankey_bytes)


#Encryption Function 

def file_Encryption(file_path,Rankey):
    cipher = AES.new(Rankey, AES.MODE_EAX)
    with open(file_path, 'rb') as file:
        plaintext = file.read()
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)  
    with open(file_path + ".ecry", 'wb') as encry_file:
        encry_file.write(cipher.nonce)
        encry_file.write(tag)
        encry_file.write(ciphertext)
    os.remove(file_path)    

# Decryption Function

def file_decryption(file_path,Rankey):
    with open(file_path,'rb') as encry_file:
        nonce = encry_file.read(16)
        tag = encry_file.read(16)
        ciphertext = encry_file.read()

    cipher = AES.new(Rankey, AES.MODE_EAX, nonce=nonce) 
    plaintext = cipher.decrypt_and_verify(ciphertext,tag)

    with open(file_path[:-4],'wb') as decry_file:
        decry_file.write(plaintext)
    os.remove(file_path)       


def Option_selection_window():
    Welcome_frame.pack_forget()
    Option_selection_frame.pack()

def Select_Option_1():
    option_1_UI()
    Option_selection_frame.pack_forget()
    back_button.pack() 

def Select_Option_2():
    option_2_UI()
    Option_selection_frame.pack_forget()
    back_button.pack() 

#function to go back to the option selction window   
def back_option():
    encryption_frame.pack_forget()
    decryption_frame.pack_forget()
    Option_selection_frame.pack()
    back_button.pack_forget()  # Hides the back button when clicked the back button and go to the option selection window

#Function to create Option1 windowUI (encryption option )

def option_1_UI():
    encryption_frame.pack()

    file_label.pack()
    file_path_entry.pack()

    Browse_file_button.pack(pady=5)
    encrypt_file_button.pack(side="left", pady=5, anchor = "nw")
    Upload_button.pack(pady=5)
    HTML_Url_button.pack(pady=5)
    back_button.pack(pady=10)


def enable_encrypt_button():
    encrypt_file_button.config(state="normal")


def option_2_UI():
    decryption_frame.pack()

    file_label2.pack()
    file_path_entry2.pack()

    Browse_file_button2.pack(pady=5)
    decrypt_file_button.pack(side="left", pady=5, anchor = "nw")
    download_button.pack(pady=5)
    HTML_Url_button2.pack(pady=5)
    back_button.pack(pady=10)


def enable_decrypt_button():
    decrypt_file_button.config(state="normal")


def Select_file1():
    #Allow user to select multiple files
    file_paths = filedialog.askopenfilenames()   
    #update the file path entry to display the selected file path
    file_path_entry.delete(1.0, tk.END)
    for file_path in file_paths:
        file_path_entry.insert(tk.END, file_path + "\n")
    
    #enable the encryption button only after user select the files
    enable_encrypt_button()


def Select_file2():
    #Allow user to select multiple files
    file_paths = filedialog.askopenfilenames()   
    #update the file path entry to display the selected file path
    file_path_entry2.delete(1.0, tk.END)
    for file_path in file_paths:
        file_path_entry2.insert(tk.END, file_path + "\n")
    
    #enable the decryption button only after user select the files
    enable_decrypt_button()


#file encryption process

def File_encryption_process():
    #set the file path from the input field
    file_paths = file_path_entry.get("1.0", tk.END).splitlines()
    #check whther the file path is enetred
    if not file_paths:
        return
    #randomly select an key for encryption
    Random_selected_key = random.choice(random_key)
    #itreate through each file path, to check for files has a .encry extension
    for file_path in file_paths:
        if file_path:
            file_Encryption(file_path,Random_selected_key)
    file_path_entry.delete(1.0, tk.END) 
    #once the file is encrypt only the upload button will enabled  
    Upload_button.config(state="normal")  
    #once the file is encrypted, a sucessfull message will be printed
    messagebox.showinfo("Encryption", "Files successfully encrypted with a randmoly seletced key")


def File_decryption_process():
    #set the file path from the input field
    file_paths = file_path_entry2.get("1.0", tk.END).splitlines()
    #check whther the file path is enetred
    if not file_paths:
        return
    
    #randomly select an key for decryption
    Random_selected_key = random.choice(random_key)
    #itreate through each file path, to check for files has a .encry extension
    for file_path in file_paths:
        if file_path and file_path.endswith('.ecry'):
            file_decryption(file_path,Random_selected_key )
    file_path_entry2.delete(1.0, tk.END)   
    download_button.config(state="normal")
    #once the file is encrypted, a sucessfull message will be printed  
    messagebox.showinfo("Decryption", "Files successfully decrypted with a randmoly seletced key")   


#function to open WinSCP
def Open_WinSCP():
    WinSCP_path = r'C:\Users\samod\AppData\Local\Programs\WinSCP\WinSCP.exe'    #path to WinSCP
    #Opeing the WinSCP using subprocess
    try:
        subprocess.Popen([WinSCP_path])
    #error message will be printed, if the WinSCP didnt get opned    
    except FileNotFoundError:
        messagebox.showerror("Error","WinSCP not Found!!. Please make sure WinSCP installed and Works properly " )


#function to open HTML url in Chrome
def HTML_Url(): 
    #URL path 
    url = "https://notification.local/view.html"  
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"  #path to chrome executable
    try:
        #regiestring chrome as the deafult browser to Open the URL
        webbrowser.register('chrome',None, webbrowser.BackgroundBrowser(chrome_path))       
        webbrowser.get('chrome').open(url)
    
    #error message will be printed, if Chromw didnt get opned    
    except Exception as excep:
        messagebox.showerror("Error,"f"Eroor Occured while Opening URL: {str(excep)}")

#function to get the Tinker window to the screen
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

#function to open the user guide
def User_guide():
    User_guide_path = '/Users/samodtharushaka/Downloads/MediCare Pro/User Manual.docx'
    os.system(f'open "{User_guide_path}"')


# ------------------------------------- UI Design Code -----------------------------------

#Create the main Window
window = tk.Tk()
window.title("MediCare Pro")
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))

#set the backgorund image
Background_image = tk.PhotoImage(file = "/Users/samodtharushaka/Downloads/MediCare Pro/Icons/Back10.png")
Background_label = tk.Label(window, image = Background_image)
Background_label.place(relwidth = 1, relheight = 1)

#Welcome Frame
Welcome_frame = tk.Frame(window, bg="", width = window.winfo_screenwidth(), height = window.winfo_screenheight())
Welcome_frame.pack_propagate(False)
Welcome_frame.pack()

# ---------- Welcome Frame component --------------
Background_label_Welcome = tk.Label(Welcome_frame, image = Background_image )
Background_label_Welcome.place (relwidth = 1, relheight = 1)

Welcome_label_1 = tk.Label(Welcome_frame, text = "W E L C O M E ", font=("Arial Black", 50), fg=("White"), bg="cadetblue", anchor="center")
Welcome_label_1.pack(pady = 160, anchor = 'center')
Welcome_label_2 = tk.Label(Welcome_frame, text = " -- GOLDEN KEY HOSPITAL --", font=("Arial Black", 30), fg=("White"), bg="cadetblue", anchor="center")
Welcome_label_2.pack(pady=70, anchor = 'center')

User_guide_button = tk.Button(Welcome_frame, text = "User Guide", font=("Arial", 14), command=User_guide, borderwidth = 0, highlightthickness = 0)
User_guide_button.pack(side=tk.BOTTOM, anchor = tk.SW, padx = 10 , pady = 1)

Copyright_label = tk.Label(Welcome_frame, text = "© Copyright 2023-2030 Golden Key Hospital", font = ("Arial",12))
Copyright_label.pack(side=tk.BOTTOM, anchor = tk.SE, padx = 1, pady = 1)

developed_label = tk.Label(Welcome_frame, text = "Developed by Group D", font = ("Arial",12))
developed_label.pack(side=tk.BOTTOM, anchor = tk.SE, padx = 10, pady = 10)

login_button = tk.Button(Welcome_frame, text = "Login", font=("Arial", 20), command=authenticate_user, borderwidth = 0, highlightthickness = 0)
login_button.pack(side=tk.TOP, anchor = 'center')

# ----------- Option Selection Frame -----------------

Option_selection_frame = tk.Frame(window, bg = 'cadetblue', width = window.winfo_screenwidth(), height = window.winfo_screenheight())
Option_selection_frame.pack_propagate(False)
Option_selection_frame.pack()

# ----------- Option Selection Frame components  -----------------

Background_label_Option_selection_frame = tk.Label(Option_selection_frame, image = Background_image)
Background_label_Option_selection_frame.place(relwidth = 1 , relheight = 1)
 
inner_frame = tk.Frame(Option_selection_frame, width = 500, height = 500, bg = '#F3F4F9')
inner_frame.pack_propagate(False)
inner_frame.pack(pady = 200)

Option_selection_label = tk.Label(inner_frame, text = "Select an Option: ", font=("Arial Black ", 16), borderwidth = 0, highlightthickness = 0)
Option_selection_label.pack(pady = 25)

encryption_button = tk.Button(inner_frame,  text = "Encryption", font=("Arial", 20), command = Select_Option_1, borderwidth = 0, highlightthickness = 0, width = 15, height = 10)
encryption_button.pack(padx =(20,20), pady = 10, side="left", anchor = 'center')

decryption_button = tk.Button(inner_frame,  text = "Decryption", font=("Arial", 20), command = Select_Option_2, borderwidth = 0, highlightthickness = 0, width = 15, height = 10)
decryption_button.pack(padx = (20,20), pady = 10, side ="right", anchor = "center")

# -------- Encryption Frame creation ---------

encryption_frame = tk.Frame(window, bg = "cadetblue")
encryption_frame.pack(fill=tk.BOTH, expand = True)

Background_label_encryption_frame = tk.Label(encryption_frame, image = Background_image)
Background_label_encryption_frame.place(relwidth = 1 , relheight = 1)

# -------- Inner Frame creation ---------
inner_frame2 = tk.Frame(encryption_frame, width = 500, height = 400, bg = '#F3F4F9')
inner_frame2.pack_propagate(False)
inner_frame2.pack(pady = 200)


# -------- decryption Frame creation ---------
decryption_frame = tk.Frame(window, bg = "cadetblue")
decryption_frame.pack(fill=tk.BOTH, expand = True)

Background_label_decryption_frame = tk.Label(decryption_frame, image = Background_image)
Background_label_decryption_frame.place(relwidth = 1 , relheight = 1)

# -------- Inner Frame 3 creation ---------
inner_frame3 = tk.Frame(decryption_frame, width = 500 ,height = 400, bg = '#F3F4F9')
inner_frame3.pack_propagate(False)
inner_frame3.pack(pady = 200)

# -------- Button Frame creation ---------
Button_frame_encryption = tk.Frame(inner_frame2)
Button_frame_encryption.pack(side="bottom")

Button_frame_decryption = tk.Frame(inner_frame3)
Button_frame_decryption.pack(side="bottom")


# -------- Encryption Frame Components---------

file_label = tk. Label(inner_frame2, text = "Selected Files : ")
file_label.pack()

file_path_entry = tk.Text(inner_frame2, width = 50 , height = 5, bd = 1 , highlightbackground = 'black')
file_path_entry.pack()

Browse_file_button = tk. Button(inner_frame2, text = "Browse Files ", command = Select_file1, borderwidth = 0, highlightthickness = 0 )
Browse_file_icon = tk.PhotoImage(file = "/Users/samodtharushaka/Downloads/MediCare Pro/Icons/File.png")
Browse_file_icon = Browse_file_icon.subsample(15, 15)
Browse_file_button.config (image = Browse_file_icon, compound = 'left')
Browse_file_button.pack(padx=(20,20))

Common_Button_frame_1 = tk.Frame(inner_frame2)
Common_Button_frame_1.pack(side='bottom')


encrypt_file_icon = tk.PhotoImage(file = "/Users/samodtharushaka/Downloads/MediCare Pro/Icons/encrypt.png")
encrypt_file_icon = encrypt_file_icon.subsample(14,14)
encrypt_file_button = tk.Button(Common_Button_frame_1, text = "Encrypt Files ", image = encrypt_file_icon, compound = "top" ,command = File_encryption_process, state = "disabled" ,borderwidth = 0, highlightthickness = 0 )
encrypt_file_button.pack(side="left", padx=(20,40), pady=(0,250))


Upload_icon = tk.PhotoImage(file="/Users/samodtharushaka/Downloads/MediCare Pro/Icons/upload.png")
Upload_icon = Upload_icon.subsample(12,14)
Upload_button = tk.Button(Common_Button_frame_1, text = "Upload ",image = Upload_icon, compound = "top" ,command = Open_WinSCP, state = "disabled" ,borderwidth = 0, highlightthickness = 0 )
Upload_button.pack(side = "right", padx = (40,20), pady = (0,250))

HTML_Url_icon = tk.PhotoImage(file = "/Users/samodtharushaka/Downloads/MediCare Pro/Icons/notification.png")
HTML_Url_icon = HTML_Url_icon.subsample(15,15)
HTML_Url_button = tk.Button(inner_frame2, text = "Notifications from Admin ",image = HTML_Url_icon, compound = "left" ,command = HTML_Url,borderwidth = 0, highlightthickness = 0 )
HTML_Url_button.pack(side = "left", padx = (150,20), pady = (400,100), anchor = 'center')

back_button_option1 = tk.Button(Button_frame_encryption, text = "Back", command = back_option , borderwidth = 0, highlightthickness = 0)
back_button_option1.pack(side = "bottom")


# ----------- Decryption Frame Components ------------------

file_label2 = tk. Label(inner_frame3, text = "Selected Files : ")
file_label2.pack()

file_path_entry2 = tk.Text(inner_frame3, width = 50 , height = 5, bd = 1 , highlightbackground = 'black')
file_path_entry2.pack()

Browse_file_button2 = tk. Button(inner_frame3, text = "Browse Files ", command = Select_file2, borderwidth = 0, highlightthickness = 0 )
Browse_file_icon2 = tk.PhotoImage(file = "/Users/samodtharushaka/Downloads/MediCare Pro/Icons/File.png")
Browse_file_icon2 = Browse_file_icon.subsample(15, 15)
Browse_file_button2.config (image = Browse_file_icon, compound = 'left')
Browse_file_button2.pack(padx=(20,20))

Common_Button_frame_2 = tk.Frame(inner_frame3)
Common_Button_frame_2.pack(side='bottom')

decrypt_file_icon = tk.PhotoImage(file = "/Users/samodtharushaka/Downloads/MediCare Pro/Icons/decrypt4.png")
decrypt_file_icon = encrypt_file_icon.subsample(20,20)
decrypt_file_button = tk.Button(Common_Button_frame_2, text = "Decrypt Files ", image = encrypt_file_icon, compound = "top" ,command = File_decryption_process, state = "disabled" ,borderwidth = 0, highlightthickness = 0 )
decrypt_file_button.pack(side="left", padx=(20,40), pady=(0,250))

download_icon = tk.PhotoImage(file="/Users/samodtharushaka/Downloads/MediCare Pro/Icons/download.png")
download_icon = download_icon.subsample(20,20)
download_button = tk.Button(Common_Button_frame_2, text = "Download ",image = download_icon, compound = "top" ,command = Open_WinSCP,borderwidth = 0, highlightthickness = 0 )
download_button.pack(side = "right", padx = (40,20), pady = (0,250))

HTML_Url_button2 = tk.Button(inner_frame3, text = "Notifications from Admin ", command = HTML_Url, borderwidth = 0, highlightthickness = 0 )
HTML_Url_icon_decryption = tk.PhotoImage(file = "/Users/samodtharushaka/Downloads/MediCare Pro/Icons/notification.png")
HTML_Url_icon_decryption = HTML_Url_icon_decryption.subsample(15,15)
HTML_Url_button2.config(image = HTML_Url_icon_decryption, compound = "left")
HTML_Url_button2.pack(side = 'left', padx = (150,20), pady = (400,100), anchor = 'center')

back_button = tk.Button(Button_frame_decryption, text = "Back", command = back_option, borderwidth = 0, highlightthickness = 0)
back_button.pack(side = "bottom")

window.mainloop() 