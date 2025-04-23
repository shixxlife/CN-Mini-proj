import socket  
import random
import smtplib  # For sending emails
import os
import json
import time
from dotenv import load_dotenv # For loading environment variables
from mutagen.mp3 import MP3
import bcrypt  # For password hashing and verification

SERVER_IP = "localhost"
SERVER_PORT = 5000
BUFFER_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create UDP socket
server_socket.bind((SERVER_IP, SERVER_PORT))  #Bind sockets to address and port

print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

load_dotenv()

def send_message(message, client_address):   #function to send messages to client 
    server_socket.sendto(message.encode(), client_address)

def recieve_message():  #function to receive messages from client 
    response, _ = server_socket.recvfrom(BUFFER_SIZE)
    return response.decode()

EMAIL = os.getenv("EMAIL")
EMAIL_PWD = os.getenv("EMAIL_PWD")
email_server = smtplib.SMTP("smtp.gmail.com", 587) #connect to gmail smtp server
email_server.starttls()# Start TLS encryption
email_server.login(EMAIL, EMAIL_PWD)

music_folder_path = r"path to music files" 


while True:
    try:
        data, client_address = server_socket.recvfrom(BUFFER_SIZE)
        text = data.decode()

        if text == "register":
            name = recieve_message()  #get username 
            email = recieve_message() #get email address 
            pswd = recieve_message() #get password

            hashed = bcrypt.hashpw(pswd.encode(), bcrypt.gensalt()).decode()  #hash password for security

            print(name, email, hashed)
            otp = random.randint(10000, 99999)

            print(otp)

            email_server.sendmail(EMAIL, email, f"Your OTP is {otp}")  #send OTP via email

            client_otp = recieve_message()
            print(client_otp)
            register_msg = "failed"

            if int(client_otp) == otp:
                register_msg = "confirmed"
                obj = {'name': name, 'pswd': hashed, 'email': email}

                if os.path.exists("data.json"):
                    with open("data.json", 'r') as file:
                        data = json.load(file) #load existing data
                else:
                    data = []

                data.append(obj) #add new user to data
                with open("data.json", 'w') as file:
                    json.dump(data, file, indent=2)
    
            send_message(register_msg, client_address)

        elif text == "login":  #handle user login 
            login_name = recieve_message() #load user data
            login_pwd = recieve_message()

            with open('data.json', 'r') as file:
                json_obj = json.load(file)
                login_msg = "failed"
                for obj in json_obj:
                    if obj["name"] == login_name and bcrypt.checkpw(login_pwd.encode(), obj["pswd"].encode()):
                        login_msg = "confirmed"
                        break
                send_message(login_msg, client_address)
        
        elif text == "song":  #handle song list request 
            music_files = [] 
            music_titles = []

            if not os.path.exists(music_folder_path): #check if music folder exists
                print("Error", f"Folder not found: {music_folder_path}")
                music_files = []
                music_titles = ["No music files found"]

            else:
                for file in os.listdir(music_folder_path):  #loop through files in directory 
                    if file.endswith('.mp3'): #check if file is MP3
                        music_files.append(os.path.join(music_folder_path, file))
                        music_titles.append(os.path.splitext(file)[0])
                   
                if not music_files:
                    music_titles = ["No music files found"]
            
            send_message(str(music_files), client_address)
            send_message(str(music_titles), client_address)

        elif text == "get_length":  #handle song length request 
            song_path = recieve_message()
            try:
                audio = MP3(song_path)
                print(audio.info.length, type(audio.info.length))
                send_message(str(audio.info.length), client_address) #send length to client
            except Exception as e:
                print(f"Error getting song length: {e}")
                send_message("0", client_address)


        elif text == "stream_song":  #handle song streaming request 
            song_path = recieve_message()
            try:
                with open(song_path, 'rb') as file:
                    send_message("start_streaming", client_address)
                    chunk_size = 4096 #set size for data chunks
                
                    while True:
                        chunk = file.read(chunk_size) #read chunk from file
                        if not chunk:
                            break
                        server_socket.sendto(chunk, client_address) #send chunk to client 
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
