from cryptography.fernet import Fernet
import os

def generate_key():
    key = Fernet.generate_key()
    with open("Secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("Secret.key", "rb").read()

def encrypt(file_path, key):
    f = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
        encrypted_data = f.encrypt(file_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

def decrypt(file_path, key):
    f = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
        try:
            decrypted_data = f.decrypt(encrypted_data)
        except InvalidToken:
            print("Invalid key")
            return
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

print("*************************************************************************************************************************")
print("*************************************************************************************************************************")
print("************************************** E N C R Y P T I O N  &  D E C R Y P T I O N **************************************")
print("*************************************************************************************************************************")
print("*************************************************************************************************************************")

print("\nEnter 'E' to encrypt or 'D' decrypt the file ")
choice = input("--> ").lower()

if choice == 'e':
    file_input = input("Enter the file name (including file extension) or full file path to encrypt: ")
    if os.path.exists(file_input):
        if os.path.isfile(file_input):
            generate_key()
            key = load_key()
            encrypt(file_input, key)
            print("File Encrypted Successfully!!!")
        else:
            print(f"'{file_input}' is not a valid file path.")
    else:
        print(f"File or path '{file_input}' not found. Please check and try again.")

elif choice == "d":
    file_input = input("Enter the file name (including file extension) or full file path to decrypt: ")
    if os.path.exists(file_input):
        if os.path.isfile(file_input):
            key = load_key()
            decrypt(file_input, key)
            print("File Decrypted Successfully!!!")
        else:
            print(f"'{file_input}' is not a valid file path.")
    else:
        print(f"File or path '{file_input}' not found. Please check and try again.")

else:
    print("Invalid choice. Please enter 'E' to encrypt a file or 'D' to decrypt a file")
