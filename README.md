# MEDICARE-PRO
Encryption / Decryption Application with an Integrity Monitor — Python + AES + PowerShell + SFTP VS Unencrypted Patient Files

# BRIEF DESCRIPTION:
Healthcare staff regularly move patient records between devices using whatever's convenient — email, USB drives, messaging apps — with no encryption and no way to tell afterward if a file was altered in transit. MediCare Pro is a desktop client that puts a security layer in front of that workflow: it encrypts files with AES before they leave the machine, hands the encrypted file off to SFTP for transfer, decrypts it on the receiving end, and runs a separate PowerShell-based integrity monitor that compares transferred files against a known-good baseline and flags an admin if anything's changed. Built for clinical staff who are not IT professionals, so the interface stays deliberately minimal.

IMPORTANT: READ THE FULL REPORT AND USER MANUAL IN /docs FOR DESIGN RATIONALE, DIAGRAMS, AND THE INTEGRITY MONITOR SCRIPT

# SYSTEM TYPE:
DESKTOP CLIENT FOR ENCRYPTED CLINICAL FILE EXCHANGE

# PRIMARY FUNCTION

The application authenticates a user locally, then offers two paths: encrypt a file and push it out over SFTP, or pull an encrypted file down and decrypt it. A companion PowerShell script runs independently of the GUI, hashing watched files on a schedule and alerting an admin role through an HTML notification page if a file's hash no longer matches its baseline. The solution is catered toward doctors, not system administrators — every security control is wrapped behind a single button (Encrypt, Upload, Decrypt, Download).

# PURPOSE & GOALS

## Primary Goals:
Give clinical staff a way to encrypt and exchange patient files without requiring any cryptography knowledge — the user picks files and clicks a button, the application handles AES encryption, key selection, and the SFTP hand-off.
Replace ad hoc sharing over email/USB/chat apps with a single SFTP-based transfer path, and give an admin role visibility into whether transferred files have been tampered with, rather than relying on staff to check manually.
Keep the system buildable entirely from open building blocks the team already had access to during the course — Python, PowerShell, IIS — rather than a commercial DLP or encryption suite.

# FEATURES
The encryption core is built in Python using PyCryptodome's AES implementation in EAX mode, which gives you both confidentiality and an authentication tag, so a decrypt operation also catches whether the ciphertext was modified. Rather than generating a new key per file, the application draws from a pool of pre-shared keys (Random_key.txt) using random.choice() — a deliberate simplification for the project scope, see Limitations.

Authentication is local: on first run the app creates a username/password pair, hashes the password with SHA-256, and stores it in a flat file. Every subsequent launch checks the entered credentials against that stored hash before unlocking the main menu.

File transfer is delegated entirely to WinSCP over SFTP rather than reinventing a transfer protocol. The "Upload" and "Download" buttons just launch WinSCP pointed at the right files — SFTP was chosen over plain FTP specifically because it encrypts data in transit, which matters more here than transfer speed.

The integrity monitor is a standalone PowerShell script (Integrity.ps1), not part of the GUI process. It walks a watched directory, hashes each file, and compares the hash against a stored baseline — new files, modified files, and deleted files are each logged separately. When it detects a mismatch, the admin is expected to manually push a notification, which staff can read via the "Notifications from Admin" button — an HTML page served through IIS and a small server.js backend.

The GUI itself is plain Tkinter — no animations, no nested menus, three screens deep at most (welcome → menu → encryption/decryption). That was an explicit design constraint: the target user is a doctor, not a developer.

# HIGH LEVEL ARCHITECTURE

## KEY COMPONENTS

Tkinter GUI client (MediCare_Pro.py) — login, file selection, and the encrypt/decrypt/upload/download controls.
PyCryptodome AES module — EAX-mode encryption/decryption against a pre-shared key pool.
Local SHA-256 credential store — flat-file username/password-hash pair, created on first run.
WinSCP / SFTP — handles the actual file transfer; the app just shells out to it.
PowerShell integrity monitor (Integrity.ps1) — baseline hashing and drift detection, run independently of the GUI.
IIS + server.js notification page — where the admin's integrity alerts surface to staff.


# SOFTWARE ARCHITECTURE

Three tiers: a presentation tier (the Tkinter GUI), an application tier (encryption/decryption, integrity monitoring, SFTP integration), and a data tier (stored file hashes).

<img width="883" height="578" alt="image" src="https://github.com/user-attachments/assets/90c5d766-85e3-457e-8085-9ebb55ae7e03" />

# APPLICATION SCREENS

<img width="838" height="515" alt="image" src="https://github.com/user-attachments/assets/9b759179-c417-48d8-96fe-922dba99cdc0" />

Encryption window — browse files, encrypt (produces a .ecry file and deletes the plaintext original), upload via WinSCP.

<img width="831" height="522" alt="image" src="https://github.com/user-attachments/assets/5f14674a-e973-40f5-9ff9-46ca6a19682f" />

Decryption window — download via WinSCP or browse to an existing .ecry file, decrypt back to the original.


# FILE SHARING / INTEGRITY FLOW

How a file actually moves through the system, and where the integrity monitor sits relative to that flow:

<img width="797" height="1035" alt="image" src="https://github.com/user-attachments/assets/d8d4c61c-1886-4e5b-9b60-59592591e017" />

A sender encrypts a file and uploads it to the server over SFTP. A recipient locates the encrypted file on the server, downloads it, and decrypts it locally. Independently of both, an admin role watches the server for integrity drift and pushes a notification if a transferred file doesn't match its expected hash — that notification is what staff see when they click "Notifications from Admin."

# LIMITATIONS

This was built and assessed as a capstone proof-of-concept, not hardened against attack. Worth knowing before reusing any of it:

Key reuse, not per-file keys. random.choice() picks one key from a small pre-shared pool rather than generating a unique key per file or session. The same key can decrypt multiple unrelated files, and that pool has to reach every client out-of-band.
Unsalted, single-round SHA-256 for passwords, stored in a local flat file with no rate limiting on login attempts.
Hardcoded, machine-specific paths for icons, the background image, the WinSCP executable, and the Chrome executable — see Setup below.
No automated tests.
Notification channel is a fixed local/intranet URL, not a configurable endpoint.


# SETUP

bashgit clone https://github.com/<your-username>/medicare-pro.git
cd medicare-pro
pip install -r requirements.txt

## Before running, you'll need to:

Replace the hardcoded paths in MediCare_Pro.py — the background image, the icon set (Browse_file_icon, encrypt_file_icon, Upload_icon, HTML_Url_icon, decrypt_file_icon, download_icon), the WinSCP executable, the Chrome executable, and the user guide path currently all point at one developer's local filesystem.
Supply your own icon set and background image — not included in this repo.
Create Random_key.txt in the working directory, one hex-encoded AES key per line. This holds the actual encryption keys, so it's gitignored — never commit it.

bash   python3 -c "import secrets; print(secrets.token_hex(32))" >> Random_key.txt

Requires Python 3.9+, python3-tk on Linux, WinSCP, and Chrome (the notification button launches Chrome specifically).

bashpython MediCare_Pro.py

# TEAM
Samod Kankanamgamage
Chanuth Wickramasinghe
Kavindu Pitigalagewage
Nivedha Ravindra
George Ranasinghearachchilage
