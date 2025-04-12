import socket
import tkinter as tk
from tkinter import messagebox, ttk, font
import os
from PIL import Image, ImageTk
import threading
import time
import pygame
from mutagen.mp3 import MP3

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
        pygame.mixer.init()
        self.root = root
        self.root.title("Music Streaming App")
        self.root.geometry("900x750")
        self.root.resizable(False, False)
        
        # Set app theme colors
        self.bg_color = "#f5f5f5"  # Light gray background
        self.primary_color = "#3498db"  # Blue
        self.secondary_color = "black"  # Dark blue/gray
        self.accent_color = "#e74c3c"  # Red accent
        self.text_color = "#333333"  # Dark text
        
        # Configure the root window
        self.root.configure(bg=self.bg_color)
        
        # Create custom fonts
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=12)
        self.small_font = font.Font(family="Helvetica", size=10)
        
        # Variables
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.otp_var = tk.StringVar()
        self.is_playing = False
        self.current_song = None
        self.play_button = None  # Store reference to play button
        self.song_title_label = None  # Store reference to song title label
        self.artist_label = None  # Store reference to artist label
        self.song_length = 0  # Store the length of the current song
        self.current_time_label = None  # Reference to current time label
        self.total_time_label = None  # Reference to total time label
        
        # Create placeholder for logo
        self.logo_frame = tk.Frame(self.root, bg=self.bg_color)
        self.logo_frame.pack(pady=20)
        
        self.logo_label = tk.Label(self.logo_frame, text="🎵 MusicStream", 
                                   font=("Helvetica", 24, "bold"), 
                                   fg=self.primary_color, bg=self.bg_color)
        self.logo_label.pack()
        
        # Show main page
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
                          bg=self.secondary_color, fg="black", 
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
        
        # Keep the logo
        self.logo_frame.pack(pady=20)
        
        # Main content frame
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
        
        # Footer
        footer = tk.Label(self.root, text="© 2025 MusicStream", 
                        font=self.small_font, fg=self.secondary_color, bg=self.bg_color)
        footer.pack(side=tk.BOTTOM, pady=10)
    
    def show_register_page(self):
        self.clear_window()
        
        # Keep the logo
        self.logo_frame.pack(pady=10)
        
        # Add back button
        back_btn = tk.Button(self.root, text="← Back", command=self.show_main_page,
                          bg=self.bg_color, fg=self.secondary_color, 
                          font=self.small_font, relief=tk.FLAT,
                          activebackground=self.bg_color, bd=0,
                          cursor="hand2")
        back_btn.place(x=20, y=20)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(pady=10)
        
        title = tk.Label(content_frame, text="Create Account", 
                       font=self.title_font, fg=self.secondary_color, bg=self.bg_color)
        title.pack(pady=10)
        
        # Form frame
        form_frame = tk.Frame(content_frame, bg=self.bg_color)
        form_frame.pack(pady=10)
        
        # Name field
        name_label = tk.Label(form_frame, text="Full Name:", 
                            font=self.normal_font, fg=self.text_color, bg=self.bg_color,
                            anchor="w")
        name_label.grid(row=0, column=0, sticky="w", pady=5)
        name_entry = self.create_styled_entry(form_frame, self.name_var)
        name_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Email field
        email_label = tk.Label(form_frame, text="Email:", 
                             font=self.normal_font, fg=self.text_color, bg=self.bg_color,
                             anchor="w")
        email_label.grid(row=1, column=0, sticky="w", pady=5)
        email_entry = self.create_styled_entry(form_frame, self.email_var)
        email_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Password field
        pwd_label = tk.Label(form_frame, text="Password:", 
                           font=self.normal_font, fg=self.text_color, bg=self.bg_color,
                           anchor="w")
        pwd_label.grid(row=2, column=0, sticky="w", pady=5)
        pwd_entry = self.create_styled_entry(form_frame, self.password_var, show="*")
        pwd_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Register button
        register_btn = self.create_styled_button(content_frame, "Continue", self.send_register_info)
        register_btn.pack(pady=20)
    
    def send_register_info(self):
        # Show loading spinner
        loading_label = tk.Label(self.root, text="Sending registration...", 
                               font=self.small_font, fg=self.primary_color, bg=self.bg_color)
        loading_label.pack(pady=10)
        self.root.update()
        
        send_message("register")
        send_message(self.name_var.get())
        send_message(self.email_var.get())
        send_message(self.password_var.get())
        
        loading_label.config(text="OTP sent to your email")
        self.root.update()
        time.sleep(1)
        loading_label.destroy()
        
        self.show_otp_page()
    
    def show_otp_page(self):
        self.clear_window()
        
        # Keep the logo
        self.logo_frame.pack(pady=20)
        
        # OTP content frame
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(pady=20)
        
        title = tk.Label(content_frame, text="Verify Your Email", 
                       font=self.title_font, fg=self.secondary_color, bg=self.bg_color)
        title.pack(pady=10)
        
        instruction = tk.Label(content_frame, 
                             text=f"We've sent an OTP to {self.email_var.get()}\nPlease enter it below to verify your account.", 
                             font=self.small_font, fg=self.text_color, bg=self.bg_color)
        instruction.pack(pady=10)
        
        # OTP entry
        otp_frame = tk.Frame(content_frame, bg=self.bg_color)
        otp_frame.pack(pady=10)
        
        otp_label = tk.Label(otp_frame, text="Enter OTP:", 
                           font=self.normal_font, fg=self.text_color, bg=self.bg_color)
        otp_label.pack(side=tk.LEFT, padx=5)
        
        otp_entry = self.create_styled_entry(otp_frame, self.otp_var, width=10)
        otp_entry.pack(side=tk.LEFT, padx=5)
        
        # Verify button
        verify_btn = self.create_styled_button(content_frame, "Verify", self.verify_otp)
        verify_btn.pack(pady=20)
        
        # Resend OTP option
        resend_btn = tk.Button(content_frame, text="Resend OTP", 
                              font=self.small_font, fg=self.primary_color, bg=self.bg_color,
                              relief=tk.FLAT, activebackground=self.bg_color, bd=0,
                              cursor="hand2")
        resend_btn.pack()
    
    def verify_otp(self):
        # Show loading spinner
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
    
    # Get song length in seconds
    def get_song_length(self, song_path):
        try:
            audio = MP3(song_path)
            return audio.info.length
        except Exception as e:
            print(f"Error getting song length: {e}")
            return 0  # Default if can't determine

    # Format time as minutes:seconds
    def format_time(self, seconds):
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"

    # Function to handle slider value change
    def slider_position(self, value):
        # Convert slider position (0-100) to seconds
        if not self.current_song or not hasattr(self, 'song_length') or self.song_length == 0:
            return
            
        position = float(value) * self.song_length / 100
        
        # Store the start position for the progress timer
        self.start_position_offset = position
        
        # Set the music position
        if pygame.mixer.music.get_busy() or self.is_playing:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play(start=position)
            self.is_playing = True
            if self.play_button:
                self.play_button.config(text="⏸")  # Pause symbol
        
        # Update current time display
        if self.current_time_label:
            self.current_time_label.config(text=self.format_time(position))

    def show_login_page(self):
        self.clear_window()
        
        # Keep the logo
        self.logo_frame.pack(pady=10)
        
        # Add back button
        back_btn = tk.Button(self.root, text="← Back", command=self.show_main_page,
                          bg=self.bg_color, fg=self.secondary_color, 
                          font=self.small_font, relief=tk.FLAT,
                          activebackground=self.bg_color, bd=0,
                          cursor="hand2")
        back_btn.place(x=20, y=20)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(pady=30)
        
        title = tk.Label(content_frame, text="Sign In", 
                       font=self.title_font, fg=self.secondary_color, bg=self.bg_color)
        title.pack(pady=10)
        
        # Form frame
        form_frame = tk.Frame(content_frame, bg=self.bg_color)
        form_frame.pack(pady=10)
        
        # Username field
        user_label = tk.Label(form_frame, text="Username:", 
                            font=self.normal_font, fg=self.text_color, bg=self.bg_color,
                            anchor="w")
        user_label.grid(row=0, column=0, sticky="w", pady=5)
        user_entry = self.create_styled_entry(form_frame, self.name_var)
        user_entry.grid(row=0, column=1, pady=5, padx=10)
        user_entry.focus()
        
        # Password field
        pwd_label = tk.Label(form_frame, text="Password:", 
                           font=self.normal_font, fg=self.text_color, bg=self.bg_color,
                           anchor="w")
        pwd_label.grid(row=1, column=0, sticky="w", pady=5)
        pwd_entry = self.create_styled_entry(form_frame, self.password_var, show="*")
        pwd_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Login button
        login_btn = self.create_styled_button(content_frame, "Sign In", self.send_login_info)
        login_btn.pack(pady=20)
        
        # Forgot password option
        forgot_btn = tk.Button(content_frame, text="Forgot Password?", 
                             font=self.small_font, fg=self.primary_color, bg=self.bg_color,
                             relief=tk.FLAT, activebackground=self.bg_color, bd=0,
                             cursor="hand2")
        forgot_btn.pack()
    
    def send_login_info(self):
        # Show loading spinner
        loading_label = tk.Label(self.root, text="Signing in...", 
                               font=self.small_font, fg=self.primary_color, bg=self.bg_color)
        loading_label.pack(pady=10)
        self.root.update()
        
        send_message("login")
        send_message(self.name_var.get())
        send_message(self.password_var.get())
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

    def toggle_play_pause(self):
        """Toggle between play and pause states"""
        if not self.current_song:
            messagebox.showinfo("Info", "Please select a song first")
            return

        if self.is_playing:
            # Currently playing, so pause
            pygame.mixer.music.pause()
            self.is_playing = False
            if self.play_button:
                self.play_button.config(text="▶")  # Play symbol
        else:
            # Resume playing from pause
            pygame.mixer.music.unpause()
            self.is_playing = True
            if self.play_button:
                self.play_button.config(text="⏸")  # Pause symbol
            self.update_progress()
 

    def play_next_song(self):
        """Play the next song in the playlist"""
        if not hasattr(self, 'music_files') or not self.music_files:
            messagebox.showinfo("Info", "No songs available")
            return
        
        if not self.songs_listbox.curselection():
            # If no song is selected, select the first one
            self.songs_listbox.selection_set(0)
            current_idx = 0
        else:
            current_idx = self.songs_listbox.curselection()[0]
        
        # Calculate next index with wraparound
        next_idx = (current_idx + 1) % len(self.music_files)
        
        # Update selection
        self.songs_listbox.selection_clear(0, tk.END)
        self.songs_listbox.selection_set(next_idx)
        self.songs_listbox.see(next_idx)  # Scroll to make selection visible
        
        # Play the selected song
        self.play_selected_song()
        
    def play_previous_song(self):
        """Play the previous song in the playlist"""
        if not hasattr(self, 'music_files') or not self.music_files:
            messagebox.showinfo("Info", "No songs available")
            return
        
        if not self.songs_listbox.curselection():
            # If no song is selected, select the last one
            self.songs_listbox.selection_set(len(self.music_files) - 1)
            current_idx = len(self.music_files) - 1
        else:
            current_idx = self.songs_listbox.curselection()[0]
        
        # Calculate previous index with wraparound
        prev_idx = (current_idx - 1) % len(self.music_files)
        
        # Update selection
        self.songs_listbox.selection_clear(0, tk.END)
        self.songs_listbox.selection_set(prev_idx)
        self.songs_listbox.see(prev_idx)  # Scroll to make selection visible
        
        # Play the selected song
        self.play_selected_song()
        
    def update_progress(self):
        if self.is_playing and pygame.mixer.music.get_busy():
            # Get the current song position in seconds
            current_pos = pygame.mixer.music.get_pos() / 1000
            
            # Add the position we started from (if we dragged the slider)
            if hasattr(self, 'start_position_offset'):
                current_pos += self.start_position_offset
            
            # Update progress bar based on actual song length
            if self.song_length > 0:
                progress = (current_pos / self.song_length) * 100
                self.progress_bar['value'] = progress
                
                # Keep slider in sync
                self.progress_slider.set(progress)
            
            # Update current time label
            if self.current_time_label:
                self.current_time_label.config(text=self.format_time(current_pos))
                
        # Schedule the next update
        self.root.after(1000, self.update_progress)

    def play_selected_song(self):
        selected_idx = self.songs_listbox.curselection()
        if not selected_idx:
            messagebox.showinfo("Info", "Please select a song first")
            return
        
        selected_idx = selected_idx[0]
        self.current_song = self.music_files[selected_idx]
        song_title = self.music_titles[selected_idx]
        
        # Get song length
        self.song_length = self.get_song_length(self.current_song)
        
        # Update song title in UI if it exists
        if self.song_title_label:
            self.song_title_label.config(text=song_title)
        
        # Update total time label
        if self.total_time_label:
            self.total_time_label.config(text=self.format_time(self.song_length))
        # Reset start position offset for the timer
        self.start_position_offset = 0
        # Reset progress bar and slider
        if hasattr(self, 'progress_bar'):
            self.progress_bar['value'] = 0
        if hasattr(self, 'progress_slider'):
            self.progress_slider.set(0)
    
        # Reset current time display
        if self.current_time_label:
            self.current_time_label.config(text="0:00")
        
        # Play the song
        try:
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play()
            self.is_playing = True
            
            # Update play button to pause
            if self.play_button:
                self.play_button.config(text="⏸")
            
            # Start progress updates
            self.update_progress()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play music: {e}")

    def show_home_page(self):
        self.clear_window()
        
        # Main container frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header frame
        header_frame = tk.Frame(main_frame, bg=self.secondary_color, height=50)
        header_frame.pack(fill=tk.X)
        
        # Logo in header
        header_logo = tk.Label(header_frame, text="🎵 MusicStream", 
                            font=("Helvetica", 14, "bold"), fg="white", bg=self.secondary_color)
        header_logo.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Logout button
        logout_btn = tk.Button(header_frame, text="Logout", command=self.show_main_page,
                            bg=self.primary_color, fg="black", relief=tk.FLAT,
                            activebackground=self.accent_color, cursor="hand2")
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Welcome message
        welcome_frame = tk.Frame(main_frame, bg=self.bg_color)
        welcome_frame.pack(fill=tk.X, pady=20, padx=20)
        
        welcome_msg = tk.Label(welcome_frame, text=f"Welcome, {self.name_var.get()}!", 
                            font=self.title_font, fg=self.secondary_color, bg=self.bg_color)
        welcome_msg.pack(anchor="w")
        
        # Music player frame
        player_frame = tk.Frame(main_frame, bg="white", bd=1, relief=tk.SOLID)
        player_frame.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)
        
        # Songs list frame
        songs_list_frame = tk.Frame(player_frame, bg="white")
        songs_list_frame.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)
        
        songs_label = tk.Label(songs_list_frame, text="Your Music", font=self.title_font, 
                            fg=self.secondary_color, bg="white")
        songs_label.pack(anchor="w", pady=10)
        
        self.songs_listbox = tk.Listbox(songs_list_frame, bg="white", fg=self.text_color,
                                    font=self.normal_font, height=8, width=40)
        self.songs_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Load music from your folder - update with your actual path
        music_folder = os.path.join(os.path.expanduser("~"), "Desktop", "Sem 4", "CN proj", "songs")
        self.load_music_library(music_folder)
        
        # Add songs to listbox
        for title in self.music_titles:
            self.songs_listbox.insert(tk.END, title)
        
        # Bind double-click to play
        self.songs_listbox.bind('<Double-1>', lambda event: self.play_selected_song())
        
        # Music info frame
        music_info_frame = tk.Frame(player_frame, bg="white", height=200)
        music_info_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Music icon placeholder
        music_icon_label = tk.Label(music_info_frame, text="🎵", font=("Arial", 48), fg=self.primary_color, bg="white")
        music_icon_label.pack()
        
        # Store references to these UI elements
        self.song_title_label = tk.Label(music_info_frame, text="Song Title", font=("Helvetica", 16, "bold"), fg=self.text_color, bg="white")
        self.song_title_label.pack(pady=5)
        
        self.artist_label = tk.Label(music_info_frame, text="Artist Name", font=("Helvetica", 12), fg=self.text_color, bg="white")
        self.artist_label.pack(pady=5)
        
        # Progress bar and slider
        progress_frame = tk.Frame(player_frame, bg="white")
        progress_frame.pack(fill=tk.X, padx=20, pady=10)

        # Create the slider/progress bar
        self.progress_slider = ttk.Scale(progress_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                    command=self.slider_position)
        self.progress_slider.pack(fill=tk.X)

        self.progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=500, mode='determinate')
        self.progress_bar.pack(fill=tk.X)

        time_frame = tk.Frame(progress_frame, bg="white", name="time_frame")
        time_frame.pack(fill=tk.X, pady=5)

        self.current_time_label = tk.Label(time_frame, text="0:00", font=self.small_font, fg=self.text_color, bg="white")
        self.current_time_label.pack(side=tk.LEFT)

        self.total_time_label = tk.Label(time_frame, text="0:00", font=self.small_font, fg=self.text_color, bg="white")
        self.total_time_label.pack(side=tk.RIGHT)
        
        # Control buttons
        control_frame = tk.Frame(player_frame, bg="white")
        control_frame.pack(pady=20)
        
        prev_btn = tk.Button(control_frame, text="⏮", font=("Arial", 16), bg="white", 
                        fg="black", relief=tk.FLAT, 
                        command=self.play_previous_song)
        prev_btn.pack(side=tk.LEFT, padx=10)
        
        self.play_button = tk.Button(control_frame, text="▶", font=("Arial", 24), 
                        bg="red", fg="black", relief=tk.FLAT, 
                        command=self.toggle_play_pause, width=3, height=1)
        self.play_button.pack(side=tk.LEFT, padx=20)
        
        next_btn = tk.Button(control_frame, text="⏭", font=("Arial", 16),
                        bg="red", fg=self.secondary_color, relief=tk.FLAT,
                        command=self.play_next_song)
        next_btn.pack(side=tk.LEFT, padx=10)
        
        # Volume control
        volume_frame = tk.Frame(player_frame, bg="red")
        volume_frame.pack(pady=10)
        
        volume_label = tk.Label(volume_frame, text="🔊", font=("Arial", 12), bg="red")
        volume_label.pack(side=tk.LEFT, padx=5)
        
        self.volume_scale = ttk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                    length=150, command=self.set_volume)
        self.volume_scale.set(70)
        self.volume_scale.pack(side=tk.LEFT)
        
        # Set initial volume
        pygame.mixer.music.set_volume(0.7)
        
        # Footer
        footer = tk.Label(main_frame, text="© 2025 MusicStream", 
                        font=self.small_font, fg=self.secondary_color, bg=self.bg_color)
        footer.pack(side=tk.BOTTOM, pady=10)
    
    def load_music_library(self, music_folder_path):
        self.music_files = []
        self.music_titles = []
    
        # Check if the folder exists
        if not os.path.exists(music_folder_path):
            messagebox.showerror("Error", f"Folder not found: {music_folder_path}")
            # Add fallback directory for testing
            self.music_files = []
            self.music_titles = ["No music files found"]
            return
    
        # Get all mp3 files
        for file in os.listdir(music_folder_path):
            if file.endswith('.mp3'):
                self.music_files.append(os.path.join(music_folder_path, file))
                # Use filename without extension as title
                self.music_titles.append(os.path.splitext(file)[0])
        
        # Add fallback if no files found
        if not self.music_files:
            self.music_titles = ["No music files found"]

    def set_volume(self, val):
        volume_value = float(val) / 100.0
        pygame.mixer.music.set_volume(volume_value)
        
    def clear_window(self):
        for widget in self.root.winfo_children():
            if widget != self.logo_frame:
                widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

client_socket.close()