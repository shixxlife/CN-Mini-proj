import socket
import random
import smtplib
import os
import json
import time
from dotenv import load_dotenv
from mutagen.mp3 import MP3
import bcrypt

SERVER_IP = "localhost"
SERVER_PORT = 5000
BUFFER_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

load_dotenv()

def send_message(message, client_address):
    server_socket.sendto(message.encode(), client_address)

def recieve_message():
    response, _ = server_socket.recvfrom(BUFFER_SIZE)
    return response.decode()

EMAIL = os.getenv("EMAIL")
EMAIL_PWD = os.getenv("EMAIL_PWD")
email_server = smtplib.SMTP("smtp.gmail.com", 587)
email_server.starttls()
email_server.login(EMAIL, EMAIL_PWD)

music_folder_path = r"D:\Advaith\clg_stuff\2nd year\SEM 4\cn\proj\songs"


while True:
    try:
        data, client_address = server_socket.recvfrom(BUFFER_SIZE)
        text = data.decode()

        if text == "register":
            name = recieve_message()
            email = recieve_message()
            pswd = recieve_message()

            hashed = bcrypt.hashpw(pswd.encode(), bcrypt.gensalt()).decode()

            print(name, email, hashed)
            otp = random.randint(10000, 99999)

            print(otp)

            email_server.sendmail(EMAIL, email, f"Your OTP is {otp}")

            client_otp = recieve_message()
            print(client_otp)
            register_msg = "failed"

            if int(client_otp) == otp:
                register_msg = "confirmed"
                obj = {'name': name, 'pswd': hashed, 'email': email}

                if os.path.exists("data.json"):
                    with open("data.json", 'r') as file:
                        data = json.load(file)
                else:
                    data = []

                data.append(obj)
                with open("data.json", 'w') as file:
                    json.dump(data, file, indent=2)
    
            send_message(register_msg, client_address)

        elif text == "login":
            login_name = recieve_message()
            login_pwd = recieve_message()

            with open('data.json', 'r') as file:
                json_obj = json.load(file)
                login_msg = "failed"
                for obj in json_obj:
                    if obj["name"] == login_name and bcrypt.checkpw(login_pwd.encode(), obj["pswd"].encode()):
                        login_msg = "confirmed"
                        break
                send_message(login_msg, client_address)
        
        elif text == "song":
            music_files = []
            music_titles = []

            if not os.path.exists(music_folder_path):
                print("Error", f"Folder not found: {music_folder_path}")
                music_files = []
                music_titles = ["No music files found"]

            else:
                for file in os.listdir(music_folder_path):
                    if file.endswith('.mp3'):
                        music_files.append(os.path.join(music_folder_path, file))
                        music_titles.append(os.path.splitext(file)[0])
                   
                if not music_files:
                    music_titles = ["No music files found"]
            
            send_message(str(music_files), client_address)
            send_message(str(music_titles), client_address)

        elif text == "get_length":
            song_path = recieve_message()
            try:
                audio = MP3(song_path)
                print(audio.info.length, type(audio.info.length))
                send_message(str(audio.info.length), client_address)
            except Exception as e:
                print(f"Error getting song length: {e}")
                send_message("0", client_address)


        elif text == "stream_song":
            song_path = recieve_message()
            try:
                with open(song_path, 'rb') as file:
                    send_message("start_streaming", client_address)
                    chunk_size = 4096
                
                    while True:
                        chunk = file.read(chunk_size)
                        if not chunk:
                            break
                        server_socket.sendto(chunk, client_address)
                        time.sleep(0.001)

                    send_message("end_streaming", client_address)
                    
            except Exception as e:
                print(f"Error streaming song: {e}")
                send_message(f"error: {str(e)}", client_address)


        else:
            pass


    except KeyboardInterrupt:
        print("Server shutting down...")
        break

server_socket.close()