import socket
import tkinter as tk
from tkinter import messagebox, ttk, font
import time
import tempfile
import threading
import pygame

SERVER_IP = "localhost"
SERVER_PORT = 5000
BUFFER_SIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_message(message):
    client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

def recieve_message():
    response, _ = client_socket.recvfrom(BUFFER_SIZE)
    return response.decode()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Streaming App")
        self.root.geometry("900x750")

        self.bg_color = "#f5f5f5"
        self.primary_color = "#3498db"
        self.secondary_color = "black"
        self.accent_color = "#e74c3c"
        self.text_color = "#333333"
        
        self.root.configure(bg=self.bg_color)
        
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=12)
        self.small_font = font.Font(family="Helvetica", size=10)
        
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.otp_var = tk.StringVar()

        self.current_user = ""
        self.current_email = ""
        self.timer_id = None

        self.logo_frame = tk.Frame(self.root, bg=self.bg_color)
        self.logo_frame.pack(pady=20)
        
        self.logo_label = tk.Label(self.logo_frame, text="🎵 MusicStream", 
                                   font=("Helvetica", 24, "bold"), 
                                   fg=self.primary_color, bg=self.bg_color)
        self.logo_label.pack()
        
        self.show_main_page()

    def create_styled_button(self, parent, text, command, primary=True, width=15):
        if primary:
            return tk.Button(parent, text=text, command=command, 
                          bg="red", fg="black", 
                          font=self.normal_font, relief=tk.FLAT,
                          activebackground=self.secondary_color,
                          width=width, cursor="hand2")
        else:
            return tk.Button(parent, text=text, command=command, 
                          bg=self.secondary_color, fg="white", 
                          font=self.normal_font, relief=tk.FLAT,
                          activebackground=self.accent_color,
                          width=width, cursor="hand2")
    
    def create_styled_entry(self, parent, textvariable, show=None, width=25):
        entry = tk.Entry(parent, textvariable=textvariable, font=self.normal_font,
                      bg="white", fg=self.text_color, show=show,
                      width=width, relief=tk.SOLID, bd=1)
        return entry
    
    def show_main_page(self):
        self.clear_window()
        
        self.logo_frame.pack(pady=20)
        
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(pady=30)
        
        welcome_label = tk.Label(content_frame, text="Welcome to Music Streaming", 
                               font=self.title_font, fg=self.secondary_color, bg=self.bg_color)
        welcome_label.pack(pady=10)
        
        description = tk.Label(content_frame, text="Stream your favorite music anytime, anywhere.", 
                             font=self.small_font, fg=self.text_color, bg=self.bg_color)
        description.pack(pady=5)
        
        button_frame = tk.Frame(content_frame, bg=self.bg_color)
        button_frame.pack(pady=30)
        
        register_btn = self.create_styled_button(button_frame, "Register", self.show_register_page)
        register_btn.pack(pady=10)
        
        login_btn = self.create_styled_button(button_frame, "Login", self.show_login_page, primary=False)
        login_btn.pack(pady=10)

        footer = tk.Label(self.root, text="© 2025 MusicStream", 
                        font=self.small_font, fg=self.secondary_color, bg=self.bg_color)
        footer.pack(side=tk.BOTTOM, pady=10)
    
    def show_register_page(self):
        self.clear_window()

        self.logo_frame.pack(pady=10)

        back_btn = tk.Button(self.root, text="← Back", command=self.show_main_page,
                          bg=self.bg_color, fg=self.secondary_color, 
                          font=self.small_font, relief=tk.FLAT,
                          activebackground=self.bg_color, bd=0,
                          cursor="hand2")
        back_btn.place(x=20, y=20)

        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(pady=10)
        
        title = tk.Label(content_frame, text="Create Account", 
                       font=self.title_font, fg=self.secondary_color, bg=self.bg_color)
        title.pack(pady=10)
        

        form_frame = tk.Frame(content_frame, bg=self.bg_color)
        form_frame.pack(pady=10)

        name_label = tk.Label(form_frame, text="Full Name:", 
                            font=self.normal_font, fg=self.text_color, bg=self.bg_color,
                            anchor="w")
        name_label.grid(row=0, column=0, sticky="w", pady=5)
        name_entry = self.create_styled_entry(form_frame, self.name_var)
        name_entry.grid(row=0, column=1, pady=5, padx=10)
        
        email_label = tk.Label(form_frame, text="Email:", 
                             font=self.normal_font, fg=self.text_color, bg=self.bg_color,
                             anchor="w")
        email_label.grid(row=1, column=0, sticky="w", pady=5)
        email_entry = self.create_styled_entry(form_frame, self.email_var)
        email_entry.grid(row=1, column=1, pady=5, padx=10)
        
        pwd_label = tk.Label(form_frame, text="Password:", 
                           font=self.normal_font, fg=self.text_color, bg=self.bg_color,
                           anchor="w")
        pwd_label.grid(row=2, column=0, sticky="w", pady=5)
        pwd_entry = self.create_styled_entry(form_frame, self.password_var, show="*")
        pwd_entry.grid(row=2, column=1, pady=5, padx=10)
        
        register_btn = self.create_styled_button(content_frame, "Continue", self.send_register_info)
        register_btn.pack(pady=20)
    
    def send_register_info(self):
        loading_label = tk.Label(self.root, text="Sending registration...", 
                               font=self.small_font, fg=self.primary_color, bg=self.bg_color)
        loading_label.pack(pady=10)
        self.root.update()

        if not self.email_var.get().endswith("@gmail.com"):
            messagebox.showerror("Error", "Please enter valid google email")
            self.email_var.set("")
            loading_label.destroy()
            return
        
        if len(self.password_var.get()) < 6:
            messagebox.showerror("Error", "Password must be atleast 6 characters long")
            self.password_var.set("")
            loading_label.destroy()
            return
        
        send_message("register")
        send_message(self.name_var.get())
        send_message(self.email_var.get())
        send_message(self.password_var.get())

        self.current_user = self.name_var.get()
        self.current_email = self.email_var.get()

        loading_label.config(text="OTP sent to your email")
        self.root.update()
        time.sleep(1)
        loading_label.destroy()

        self.clear_labels()
        self.show_otp_page()
    
    def show_otp_page(self):
        self.clear_window()
        self.logo_frame.pack(pady=20)
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(pady=20)
        
        title = tk.Label(content_frame, text="Verify Your Email", 
                       font=self.title_font, fg=self.secondary_color, bg=self.bg_color)
        title.pack(pady=10)
        
        instruction = tk.Label(content_frame, 
                             text=f"We've sent an OTP to {self.current_email}\nPlease enter it below to verify your account.", 
                             font=self.small_font, fg=self.text_color, bg=self.bg_color)
        instruction.pack(pady=10)
        
        otp_frame = tk.Frame(content_frame, bg=self.bg_color)
        otp_frame.pack(pady=10)
        
        otp_label = tk.Label(otp_frame, text="Enter OTP:", 
                           font=self.normal_font, fg=self.text_color, bg=self.bg_color)
        otp_label.pack(side=tk.LEFT, padx=5)
        
        otp_entry = self.create_styled_entry(otp_frame, self.otp_var, width=10)
        otp_entry.pack(side=tk.LEFT, padx=5)
        
        verify_btn = self.create_styled_button(content_frame, "Verify", self.verify_otp)
        verify_btn.pack(pady=20)
        
        resend_btn = tk.Button(content_frame, text="Resend OTP", 
                              font=self.small_font, fg=self.primary_color, bg=self.bg_color,
                              relief=tk.FLAT, activebackground=self.bg_color, bd=0,
                              cursor="hand2")
        resend_btn.pack()
    
    def verify_otp(self):
        loading_label = tk.Label(self.root, text="Verifying...", 
                               font=self.small_font, fg=self.primary_color, bg=self.bg_color)
        loading_label.pack(pady=10)
        self.root.update()
        
        send_message(self.otp_var.get())
        response = recieve_message()
        
        loading_label.destroy()
        
        if response == "confirmed":
            success_label = tk.Label(self.root, text="Registration successful!", 
                                   font=self.normal_font, fg="green", bg=self.bg_color)
            success_label.pack(pady=10)
            self.root.update()
            time.sleep(1.5)
            self.show_home_page()
        else:
            messagebox.showerror("Error", "OTP verification failed")
            self.show_main_page()
        
        self.clear_labels()
    
    def show_login_page(self):
        self.clear_window()

        self.logo_frame.pack(pady=10)

        back_btn = tk.Button(self.root, text="← Back", command=self.show_main_page,
                          bg=self.bg_color, fg=self.secondary_color, 
                          font=self.small_font, relief=tk.FLAT,
                          activebackground=self.bg_color, bd=0,
                          cursor="hand2")
        back_btn.place(x=20, y=20)

        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(pady=30)
        
        title = tk.Label(content_frame, text="Sign In", 
                       font=self.title_font, fg=self.secondary_color, bg=self.bg_color)
        title.pack(pady=10)

        form_frame = tk.Frame(content_frame, bg=self.bg_color)
        form_frame.pack(pady=10)

        user_label = tk.Label(form_frame, text="Username:", 
                            font=self.normal_font, fg=self.text_color, bg=self.bg_color,
                            anchor="w")
        user_label.grid(row=0, column=0, sticky="w", pady=5)
        user_entry = self.create_styled_entry(form_frame, self.name_var)
        user_entry.grid(row=0, column=1, pady=5, padx=10)
        user_entry.focus()

        pwd_label = tk.Label(form_frame, text="Password:", 
                           font=self.normal_font, fg=self.text_color, bg=self.bg_color,
                           anchor="w")
        pwd_label.grid(row=1, column=0, sticky="w", pady=5)
        pwd_entry = self.create_styled_entry(form_frame, self.password_var, show="*")
        pwd_entry.grid(row=1, column=1, pady=5, padx=10)

        login_btn = self.create_styled_button(content_frame, "Sign In", self.send_login_info)
        login_btn.pack(pady=20)

        forgot_btn = tk.Button(content_frame, text="Forgot Password?", 
                             font=self.small_font, fg=self.primary_color, bg=self.bg_color,
                             relief=tk.FLAT, activebackground=self.bg_color, bd=0,
                             cursor="hand2")
        forgot_btn.pack()
    
    def send_login_info(self):
        loading_label = tk.Label(self.root, text="Signing in...", 
                               font=self.small_font, fg=self.primary_color, bg=self.bg_color)
        loading_label.pack(pady=10)
        self.root.update()
        
        send_message("login")
        send_message(self.name_var.get())
        send_message(self.password_var.get())

        self.current_user = self.name_var.get()

        response = recieve_message()
        
        loading_label.destroy()
        
        if response == "confirmed":
            success_label = tk.Label(self.root, text="Login successful!", 
                                   font=self.normal_font, fg="green", bg=self.bg_color)
            success_label.pack(pady=10)
            self.root.update()
            time.sleep(1)
            self.show_home_page()
        else:
            messagebox.showerror("Error", "Invalid username or password")
        
        self.clear_labels()
    

    def show_home_page(self):
        self.clear_window()
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg=self.secondary_color, height=50)
        header_frame.pack(fill=tk.X)
        
        header_logo = tk.Label(header_frame, text="🎵 MusicStream", 
                            font=("Helvetica", 14, "bold"), fg="white", bg=self.secondary_color)
        header_logo.pack(side=tk.LEFT, padx=20, pady=10)
        
        logout_btn = tk.Button(header_frame, text="Logout", command=self.show_logout_main_page,
                            bg=self.primary_color, fg="black", relief=tk.FLAT,
                            activebackground=self.accent_color, cursor="hand2")
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        welcome_frame = tk.Frame(main_frame, bg=self.bg_color)
        welcome_frame.pack(fill=tk.X, pady=20, padx=20)
        
        welcome_msg = tk.Label(welcome_frame, text=f"Welcome, {self.current_user}!", 
                            font=self.title_font, fg=self.secondary_color, bg=self.bg_color)
        welcome_msg.pack(anchor="w")

        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        library_frame = tk.Frame(content_frame, bg=self.bg_color, width=600)
        library_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        library_label = tk.Label(library_frame, text="Music Library", 
                                font=self.normal_font, fg=self.secondary_color, bg=self.bg_color)
        library_label.pack(pady=10, anchor="w")
        
        list_container = tk.Frame(library_frame, bg=self.bg_color)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.song_listbox = tk.Listbox(list_container, bg="white", fg=self.text_color,
                                     font=self.normal_font, height=15,
                                     selectbackground=self.primary_color,
                                     selectforeground="white",
                                     activestyle="none", bd=1, relief=tk.SOLID)
        self.song_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.song_listbox.yview)
        self.song_listbox.config(yscrollcommand=scrollbar.set)
        
        self.song_listbox.bind("<Double-1>", lambda event: self.set_selected_song())
        
        player_frame = tk.Frame(content_frame, bg=self.bg_color, width=400, relief=tk.RIDGE, bd=1)
        player_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        now_playing_label = tk.Label(player_frame, text="Now Playing", 
                                    font=self.normal_font, fg=self.secondary_color, bg=self.bg_color)
        now_playing_label.pack(pady=10)
        
        self.current_song_var = tk.StringVar()
        self.current_song_var.set("No song playing")
        
        current_song_display = tk.Label(player_frame, textvariable=self.current_song_var,
                                      font=("Helvetica", 14, "bold"), fg=self.primary_color, 
                                      bg=self.bg_color, wraplength=350)
        current_song_display.pack(pady=10)
        
        slider_frame = tk.Frame(player_frame, bg=self.bg_color)
        slider_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.time_elapsed_var = tk.StringVar()
        self.time_elapsed_var.set("0:00")
        time_elapsed_label = tk.Label(slider_frame, textvariable=self.time_elapsed_var,
                                    font=self.small_font, fg=self.text_color, bg=self.bg_color)
        time_elapsed_label.pack(side=tk.LEFT)
        
        self.song_length_var = tk.StringVar()
        self.song_length_var.set("0:00")
        song_length_label = tk.Label(slider_frame, textvariable=self.song_length_var,
                                   font=self.small_font, fg=self.text_color, bg=self.bg_color)
        song_length_label.pack(side=tk.RIGHT)
        
        self.progress_slider = ttk.Scale(player_frame, from_=0, to=100, 
                                      orient=tk.HORIZONTAL, length=350) # command = self.seek_position
        self.progress_slider.pack(fill=tk.X, padx=20)
        
        controls_frame = tk.Frame(player_frame, bg=self.bg_color)
        controls_frame.pack(pady=20)
        
        prev_btn = tk.Button(controls_frame, text="⏮", font=("Helvetica", 16),
                           bg=self.bg_color, fg=self.secondary_color, 
                           relief=tk.FLAT, command=self.play_prev_song)
        prev_btn.pack(side=tk.LEFT, padx=10)
        
        self.play_pause_text = tk.StringVar()
        self.play_pause_text.set("▶")
        
        self.play_pause_btn = tk.Button(controls_frame, textvariable=self.play_pause_text, 
                                     font=("Helvetica", 16), bg=self.primary_color,
                                     fg="white", relief=tk.FLAT, width=2, command=self.toggle_play_pause)
        self.play_pause_btn.pack(side=tk.LEFT, padx=10)
        
        next_btn = tk.Button(controls_frame, text="⏭", font=("Helvetica", 16),
                           bg=self.bg_color, fg=self.secondary_color, 
                           relief=tk.FLAT, command=self.play_next_song)
        next_btn.pack(side=tk.LEFT, padx=10)
        
        footer = tk.Label(self.root, text="© 2025 MusicStream", 
                        font=self.small_font, fg=self.secondary_color, bg=self.bg_color)
        footer.pack(side=tk.BOTTOM, pady=10)
        
        pygame.mixer.init()
        self.load_music_library()

    def show_logout_main_page(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.pause()
            self.play_pause_text.set("▶")
            self.music_paused = True
        self.show_main_page()

    
    def load_music_library(self):
        send_message("song")
        self.music_files = recieve_message()[2:-2].split(r"', '")
        self.music_titles = recieve_message()[2:-2].split(r"', '")

        self.song_listbox.delete(0, tk.END)
        for title in self.music_titles:
            self.song_listbox.insert(tk.END, title)

    def get_song_length(self, song_path):
        send_message("get_length")
        send_message(song_path)
        length = recieve_message()
        return float(length)

    def play_next_song(self):
        next_index = (self.current_song_index + 1) % len(self.music_titles)
        
        self.song_listbox.selection_clear(0, 'end')
        self.song_listbox.selection_set(next_index)
        self.song_listbox.see(next_index)

        self.set_selected_song()

    def play_prev_song(self):
        prev_index = (self.current_song_index - 1) % len(self.music_titles)
        
        self.song_listbox.selection_clear(0, 'end')
        self.song_listbox.selection_set(prev_index)
        self.song_listbox.see(prev_index)

        self.set_selected_song()
    
    def set_selected_song(self):
        selected_indices = self.song_listbox.curselection()
        self.current_song_index = selected_indices[0]

        selected_song = self.music_titles[self.current_song_index]
        self.current_song_var.set(selected_song)
        self.play_selected_song()

    
    def play_selected_song(self):
        if hasattr(self, 'timer_id') and self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        selected_song_path = self.music_files[self.current_song_index]
        send_message("stream_song")
        send_message(selected_song_path)
        
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_filename = temp_file.name
        temp_file.close()
        
        def receive_stream():
            with open(temp_filename, 'wb') as file:
                while True:
                    try:
                        client_socket.settimeout(10) 
                        data, _ = client_socket.recvfrom(8192)
                        
                        try:
                            message = data.decode()
                            if message == "end_streaming":
                                break
                            elif message.startswith("error:"):
                                messagebox.showerror("Error", message[6:])
                                return
                            elif message == "start_streaming":
                                continue
                        except UnicodeDecodeError:
                            file.write(data)
                            
                    except socket.timeout:
                        messagebox.showerror("Error", "Streaming timed out")
                        break
            
            try:
                self.play_pause_text.set("⏸")
                self.music_paused = False
                pygame.mixer.music.load(temp_filename)
                pygame.mixer.music.play()

                song_length = pygame.mixer.Sound(temp_filename).get_length()
                self.progress_slider.config(to=song_length)
                
                mins, secs = divmod(song_length, 60)
                self.song_length_var.set(f"{int(mins)}:{int(secs):02d}")

                self.current_playback_time = 0
                self.update_progress()
                
            except Exception as e: 
                messagebox.showerror("Error", f"Could not play the song: {str(e)}")
        
        threading.Thread(target=receive_stream, daemon=True).start()

    def toggle_play_pause(self):
        if not self.music_paused and pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.play_pause_text.set("▶")
            self.music_paused = True
        else:
            pygame.mixer.music.unpause()
            self.play_pause_text.set("⏸")
            self.music_paused = False
    
    def update_progress(self):
        if hasattr(self, 'timer_id') and self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
            
        if pygame.mixer.music.get_busy() and not getattr(self, 'music_paused', False):
            self.current_playback_time += 1
            
            self.progress_slider.set(self.current_playback_time)
            
            mins, secs = divmod(self.current_playback_time, 60)
            self.time_elapsed_var.set(f"{int(mins)}:{int(secs):02d}")
            
            self.timer_id = self.root.after(1000, self.update_progress)
        else:
            if getattr(self, 'music_paused', False):
                self.timer_id = self.root.after(1000, self.update_progress)


    def clear_labels(self):
        self.name_var.set("")
        self.email_var.set("")
        self.password_var.set("")
        self.otp_var.set("")

    
    def clear_window(self):
        for widget in self.root.winfo_children():
            if widget != self.logo_frame:
                widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

client_socket.close()
