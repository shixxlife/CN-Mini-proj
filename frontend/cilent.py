import socket  
import tkinter as tk  # For GUI components
from tkinter import messagebox, ttk, font  
import time 
import tempfile  # For creating temporary files
import threading  # For running tasks concurrently
import pygame  # For audio playback

SERVER_IP = "localhost" 
SERVER_PORT = 5000  
BUFFER_SIZE = 1024 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create UDP socket

def send_message(message):  # Helper function to send messages to server
    client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

def recieve_message():  # Helper function to receive messages from server (note typo in name)
    response, _ = client_socket.recvfrom(BUFFER_SIZE)
    return response.decode()

class App:  # Main application class
    def __init__(self, root):  # Initialize the application
        self.root = root  # Set the root window
        self.root.title("Music Streaming App")  # Set window title
        self.root.geometry("900x750")  # Set window size

        self.bg_color = "#f5f5f5"  # Background color
        self.primary_color = "#3498db"  
        self.secondary_color = "black"  
        self.accent_color = "#e74c3c"  
        self.text_color = "#333333" 
        
        self.root.configure(bg=self.bg_color)  # Set window background color
        
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")  # Font for titles
        self.normal_font = font.Font(family="Helvetica", size=12)  # Font for normal text
        self.small_font = font.Font(family="Helvetica", size=10)  # Font for small text
        
        self.name_var = tk.StringVar()  # Variable to store username
        self.email_var = tk.StringVar()  # Variable to store email
        self.password_var = tk.StringVar()  # Variable to store password
        self.otp_var = tk.StringVar()  # Variable to store OTP

        self.current_user = ""  # Track current logged-in user
        self.current_email = ""  # Track current user's email
        self.timer_id = None  # For managing timed events

        self.logo_frame = tk.Frame(self.root, bg=self.bg_color)  # Create frame for logo
        self.logo_frame.pack(pady=20)  # Add padding and display logo frame
        
        self.logo_label = tk.Label(self.logo_frame, text="🎵 MusicStream", 
                                   font=("Helvetica", 24, "bold"), 
                                   fg=self.primary_color, bg=self.bg_color)  # Create logo label
        self.logo_label.pack()  # Display logo
        
        self.show_main_page()  # Show the main page initially

    def create_styled_button(self, parent, text, command, primary=True, width=15):  # Helper to create styled buttons
        if primary:
            return tk.Button(parent, text=text, command=command, 
                          bg="red", fg="black",  # Red button for primary actions
                          font=self.normal_font, relief=tk.FLAT,
                          activebackground=self.secondary_color,
                          width=width, cursor="hand2")
        else:
            return tk.Button(parent, text=text, command=command, 
                          bg=self.secondary_color, fg="white",  # Black button for secondary actions
                          font=self.normal_font, relief=tk.FLAT,
                          activebackground=self.accent_color,
                          width=width, cursor="hand2")
    
    def create_styled_entry(self, parent, textvariable, show=None, width=25):  # Helper to create styled text inputs
        entry = tk.Entry(parent, textvariable=textvariable, font=self.normal_font,
                      bg="white", fg=self.text_color, show=show,
                      width=width, relief=tk.SOLID, bd=1)
        return entry
    
    def show_main_page(self):  # Display the main landing page
        self.clear_window()  # Remove previous content
        
        self.logo_frame.pack(pady=20)  # Show logo with padding
        
        content_frame = tk.Frame(self.root, bg=self.bg_color)  # Create frame for main content
        content_frame.pack(pady=30)  # Add padding and display content frame
        
        welcome_label = tk.Label(content_frame, text="Welcome to Music Streaming", 
                               font=self.title_font, fg=self.secondary_color, bg=self.bg_color)  # Welcome message
        welcome_label.pack(pady=10)  # Display welcome message
        
        description = tk.Label(content_frame, text="Stream your favorite music anytime, anywhere.", 
                             font=self.small_font, fg=self.text_color, bg=self.bg_color)  # App description
        description.pack(pady=5)  # Display description
        
        button_frame = tk.Frame(content_frame, bg=self.bg_color)  # Create frame for buttons
        button_frame.pack(pady=30)  # Add padding and display button frame
        
        register_btn = self.create_styled_button(button_frame, "Register", self.show_register_page)  # Create register button
        register_btn.pack(pady=10)  # Display register button
        
        login_btn = self.create_styled_button(button_frame, "Login", self.show_login_page, primary=False)  # Create login button
        login_btn.pack(pady=10)  # Display login button

        footer = tk.Label(self.root, text="© 2025 MusicStream", 
                        font=self.small_font, fg=self.secondary_color, bg=self.bg_color)  # Create copyright footer
        footer.pack(side=tk.BOTTOM, pady=10)  # Display footer at bottom
    
    def show_register_page(self):  # Display the registration page
        self.clear_window()  # Remove previous content
        
        self.logo_frame.pack(pady=10)  # Show logo with padding
        
        back_btn = tk.Button(self.root, text="← Back", command=self.show_main_page,
                        bg=self.bg_color, fg=self.secondary_color, 
                        font=self.small_font, relief=tk.FLAT,
                        activebackground=self.bg_color, bd=0,
                        cursor="hand2")  # Create back button
        back_btn.place(x=20, y=20)  # Position back button in top-left corner
        
        content_frame = tk.Frame(self.root, bg=self.bg_color)  # Create frame for main content
        content_frame.pack(pady=10)  # Add padding and display content frame
        
        title = tk.Label(content_frame, text="Create Account", 
                    font=self.title_font, fg=self.secondary_color, bg=self.bg_color)  # Page title
        title.pack(pady=10)  # Display title
        
        
        form_frame = tk.Frame(content_frame, bg=self.bg_color)  # Create frame for form elements
        form_frame.pack(pady=10)  # Add padding and display form frame
        
        name_label = tk.Label(form_frame, text="Full Name:", 
                            font=self.normal_font, fg=self.text_color, bg=self.bg_color,
                            anchor="w")  # Label for name field
        name_label.grid(row=0, column=0, sticky="w", pady=5)  # Position name label
        name_entry = self.create_styled_entry(form_frame, self.name_var)  # Create name input field
        name_entry.grid(row=0, column=1, pady=5, padx=10)  # Position name input field
        
        email_label = tk.Label(form_frame, text="Email:", 
                            font=self.normal_font, fg=self.text_color, bg=self.bg_color,
                            anchor="w")  # Label for email field
        email_label.grid(row=1, column=0, sticky="w", pady=5)  # Position email label
        email_entry = self.create_styled_entry(form_frame, self.email_var)  # Create email input field
        email_entry.grid(row=1, column=1, pady=5, padx=10)  # Position email input field
        
        pwd_label = tk.Label(form_frame, text="Password:", 
                        font=self.normal_font, fg=self.text_color, bg=self.bg_color,
                        anchor="w")  # Label for password field
        pwd_label.grid(row=2, column=0, sticky="w", pady=5)  # Position password label
        pwd_entry = self.create_styled_entry(form_frame, self.password_var, show="*")  # Create password input field with masked text
        pwd_entry.grid(row=2, column=1, pady=5, padx=10)  # Position password input field
        
        register_btn = self.create_styled_button(content_frame, "Continue", self.send_register_info)  # Create continue button
        register_btn.pack(pady=20)  # Display continue button

    def send_register_info(self):  # Process registration form submission
        loading_label = tk.Label(self.root, text="Sending registration...", 
                            font=self.small_font, fg=self.primary_color, bg=self.bg_color)  # Create loading message
        loading_label.pack(pady=10)  # Display loading message
        self.root.update()  # Force UI update to show loading message
        
        if not self.email_var.get().endswith("@gmail.com"):  # Validate email (must be Gmail)
            messagebox.showerror("Error", "Please enter valid google email")  # Show error for invalid email
            self.email_var.set("")  # Clear email field
            loading_label.destroy()  # Remove loading message
            return
        
        if len(self.password_var.get()) < 6:  # Validate password length
            messagebox.showerror("Error", "Password must be atleast 6 characters long")  # Show error for short password
            self.password_var.set("")  # Clear password field
            loading_label.destroy()  # Remove loading message
            return
        
        send_message("register")  # Send registration command to server
        send_message(self.name_var.get())  # Send name to server
        send_message(self.email_var.get())  # Send email to server
        send_message(self.password_var.get())  # Send password to server
        
        self.current_user = self.name_var.get()  # Store current user's name
        self.current_email = self.email_var.get()  # Store current user's email
        
        loading_label.config(text="OTP sent to your email")  # Update loading message
        self.root.update()  # Force UI update
        time.sleep(1)  # Wait briefly
        loading_label.destroy()  # Remove loading message
        
        self.clear_labels()  # Clear any other labels
        self.show_otp_page()  # Show OTP verification page

    def show_otp_page(self):  # Display OTP verification page
        self.clear_window()  # Remove previous content
        self.logo_frame.pack(pady=20)  # Show logo with padding
        content_frame = tk.Frame(self.root, bg=self.bg_color)  # Create frame for main content
        content_frame.pack(pady=20)  # Add padding and display content frame
        
        title = tk.Label(content_frame, text="Verify Your Email", 
                    font=self.title_font, fg=self.secondary_color, bg=self.bg_color)  # Page title
        title.pack(pady=10)  # Display title
        
        instruction = tk.Label(content_frame, 
                            text=f"We've sent an OTP to {self.current_email}\nPlease enter it below to verify your account.", 
                            font=self.small_font, fg=self.text_color, bg=self.bg_color)  # Instructions text
        instruction.pack(pady=10)  # Display instructions
        
        otp_frame = tk.Frame(content_frame, bg=self.bg_color)  # Create frame for OTP input
        otp_frame.pack(pady=10)  # Add padding and display OTP frame
        
        otp_label = tk.Label(otp_frame, text="Enter OTP:", 
                        font=self.normal_font, fg=self.text_color, bg=self.bg_color)  # Label for OTP field
        otp_label.pack(side=tk.LEFT, padx=5)  # Position OTP label
        
        otp_entry = self.create_styled_entry(otp_frame, self.otp_var, width=10)  # Create OTP input field
        otp_entry.pack(side=tk.LEFT, padx=5)  # Position OTP input field
        
        verify_btn = self.create_styled_button(content_frame, "Verify", self.verify_otp)  # Create verify button
        verify_btn.pack(pady=20)  # Display verify button
        
        resend_btn = tk.Button(content_frame, text="Resend OTP", 
                            font=self.small_font, fg=self.primary_color, bg=self.bg_color,
                            relief=tk.FLAT, activebackground=self.bg_color, bd=0,
                            cursor="hand2")  # Create resend OTP button (functionality not implemented)
        resend_btn.pack()  # Display resend button
    
    def verify_otp(self):  # Process OTP verification
        loading_label = tk.Label(self.root, text="Verifying...", 
                            font=self.small_font, fg=self.primary_color, bg=self.bg_color)  # Create loading message
        loading_label.pack(pady=10)  # Display loading message
        self.root.update()  # Force UI update to show loading message
        
        send_message(self.otp_var.get())  # Send OTP to server
        response = recieve_message()  # Get verification result from server
        
        loading_label.destroy()  # Remove loading message
        
        if response == "confirmed":  # Check if OTP was valid
            success_label = tk.Label(self.root, text="Registration successful!", 
                                font=self.normal_font, fg="green", bg=self.bg_color)  # Create success message
            success_label.pack(pady=10)  # Display success message
            self.root.update()  # Force UI update
            time.sleep(1.5)  # Brief delay to show success message
            self.show_home_page()  # Navigate to home page after successful registration
        else:
            messagebox.showerror("Error", "OTP verification failed")  # Show error for invalid OTP
            self.show_main_page()  # Return to main page on failure
        
        self.clear_labels()  # Clean up UI elements

    def show_login_page(self):  # Display the login page
        self.clear_window()  # Remove previous content
        
        self.logo_frame.pack(pady=10)  # Show logo with padding
        
        back_btn = tk.Button(self.root, text="← Back", command=self.show_main_page,
                        bg=self.bg_color, fg=self.secondary_color, 
                        font=self.small_font, relief=tk.FLAT,
                        activebackground=self.bg_color, bd=0,
                        cursor="hand2")  # Create back button
        back_btn.place(x=20, y=20)  # Position back button in top-left corner
        
        content_frame = tk.Frame(self.root, bg=self.bg_color)  # Create frame for main content
        content_frame.pack(pady=30)  # Add padding and display content frame
        
        title = tk.Label(content_frame, text="Sign In", 
                    font=self.title_font, fg=self.secondary_color, bg=self.bg_color)  # Page title
        title.pack(pady=10)  # Display title
        
        form_frame = tk.Frame(content_frame, bg=self.bg_color)  # Create frame for form elements
        form_frame.pack(pady=10)  # Add padding and display form frame
        
        user_label = tk.Label(form_frame, text="Username:", 
                            font=self.normal_font, fg=self.text_color, bg=self.bg_color,
                            anchor="w")  # Label for username field
        user_label.grid(row=0, column=0, sticky="w", pady=5)  # Position username label
        user_entry = self.create_styled_entry(form_frame, self.name_var)  # Create username input field
        user_entry.grid(row=0, column=1, pady=5, padx=10)  # Position username input field
        user_entry.focus()  # Set focus to username field
        
        pwd_label = tk.Label(form_frame, text="Password:", 
                        font=self.normal_font, fg=self.text_color, bg=self.bg_color,
                        anchor="w")  # Label for password field
        pwd_label.grid(row=1, column=0, sticky="w", pady=5)  # Position password label
        pwd_entry = self.create_styled_entry(form_frame, self.password_var, show="*")  # Create password input field with masked text
        pwd_entry.grid(row=1, column=1, pady=5, padx=10)  # Position password input field
        
        login_btn = self.create_styled_button(content_frame, "Sign In", self.send_login_info)  # Create sign in button
        login_btn.pack(pady=20)  # Display sign in button
        
        forgot_btn = tk.Button(content_frame, text="Forgot Password?", 
                            font=self.small_font, fg=self.primary_color, bg=self.bg_color,
                            relief=tk.FLAT, activebackground=self.bg_color, bd=0,
                            cursor="hand2")  # Create forgot password button (functionality not implemented)
        forgot_btn.pack()  # Display forgot password button

    def send_login_info(self):  # Process login form submission
        loading_label = tk.Label(self.root, text="Signing in...", 
                            font=self.small_font, fg=self.primary_color, bg=self.bg_color)  # Create loading message
        loading_label.pack(pady=10)  # Display loading message
        self.root.update()  # Force UI update to show loading message
        
        send_message("login")  # Send login command to server
        send_message(self.name_var.get())  # Send username to server
        send_message(self.password_var.get())  # Send password to server
        
        self.current_user = self.name_var.get()  # Store current username
        
        response = recieve_message()  # Get login result from server
        
        loading_label.destroy()  # Remove loading message
        
        if response == "confirmed":  # Check if login was successful
            success_label = tk.Label(self.root, text="Login successful!", 
                                font=self.normal_font, fg="green", bg=self.bg_color)  # Create success message
            success_label.pack(pady=10)  # Display success message
            self.root.update()  # Force UI update
            time.sleep(1)  # Brief delay to show success message
            self.show_home_page()  # Navigate to home page after successful login
        else:
            messagebox.showerror("Error", "Invalid username or password")  # Show error for invalid credentials
        
        self.clear_labels()  # Clean up UI elements

    def show_home_page(self):  # Display the main application home page
        self.clear_window()  # Remove previous content
        main_frame = tk.Frame(self.root, bg=self.bg_color)  # Create main container frame
        main_frame.pack(fill=tk.BOTH, expand=True)  # Fill available space
        
        header_frame = tk.Frame(main_frame, bg=self.secondary_color, height=50)  # Create header bar
        header_frame.pack(fill=tk.X)  # Make header span full width
        
        header_logo = tk.Label(header_frame, text="🎵 MusicStream", 
                            font=("Helvetica", 14, "bold"), fg="white", bg=self.secondary_color)  # Create header logo
        header_logo.pack(side=tk.LEFT, padx=20, pady=10)  # Position logo on left side
        
        logout_btn = tk.Button(header_frame, text="Logout", command=self.show_logout_main_page,
                            bg=self.primary_color, fg="black", relief=tk.FLAT,
                            activebackground=self.accent_color, cursor="hand2")  # Create logout button
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=10)  # Position button on right side
        
        welcome_frame = tk.Frame(main_frame, bg=self.bg_color)  # Create welcome section
        welcome_frame.pack(fill=tk.X, pady=20, padx=20)  # Make welcome span full width
        
        welcome_msg = tk.Label(welcome_frame, text=f"Welcome, {self.current_user}!", 
                            font=self.title_font, fg=self.secondary_color, bg=self.bg_color)  # Create welcome message
        welcome_msg.pack(anchor="w")  # Left-align welcome message
        
        content_frame = tk.Frame(main_frame, bg=self.bg_color)  # Create content container
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)  # Fill available space
        
        library_frame = tk.Frame(content_frame, bg=self.bg_color, width=600)  # Create library section
        library_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))  # Position on left side
        
        library_label = tk.Label(library_frame, text="Music Library", 
                                font=self.normal_font, fg=self.secondary_color, bg=self.bg_color)  # Create library header
        library_label.pack(pady=10, anchor="w")  # Left-align library header
        
        list_container = tk.Frame(library_frame, bg=self.bg_color)  # Create container for song list
        list_container.pack(fill=tk.BOTH, expand=True)  # Fill available space
        
        scrollbar = tk.Scrollbar(list_container)  # Create scrollbar for song list
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Position scrollbar on the right side
        
        self.song_listbox = tk.Listbox(list_container, bg="white", fg=self.text_color,
                                    font=self.normal_font, height=15,
                                    selectbackground=self.primary_color,
                                    selectforeground="white",
                                    activestyle="none", bd=1, relief=tk.SOLID)  # Create song list
        self.song_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Fill available space
        
        scrollbar.config(command=self.song_listbox.yview)  # Link scrollbar to song list
        self.song_listbox.config(yscrollcommand=scrollbar.set)  # Link song list to scrollbar
        
        self.song_listbox.bind("<Double-1>", lambda event: self.set_selected_song())  # Bind double-click to play selected song
        
        player_frame = tk.Frame(content_frame, bg=self.bg_color, width=400, relief=tk.RIDGE, bd=1)  # Create music player frame
        player_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))  # Position on right side
        
        now_playing_label = tk.Label(player_frame, text="Now Playing", 
                                    font=self.normal_font, fg=self.secondary_color, bg=self.bg_color)  # Create now playing header
        now_playing_label.pack(pady=10)  # Display header
        
        self.current_song_var = tk.StringVar()  # Variable to store current song name
        self.current_song_var.set("No song playing")  # Default value
        
        current_song_display = tk.Label(player_frame, textvariable=self.current_song_var,
                                    font=("Helvetica", 14, "bold"), fg=self.primary_color, 
                                    bg=self.bg_color, wraplength=350)  # Display for current song
        current_song_display.pack(pady=10)  # Show current song
        
        slider_frame = tk.Frame(player_frame, bg=self.bg_color)  # Create frame for progress display
        slider_frame.pack(fill=tk.X, padx=20, pady=10)  # Make it span full width
        
        self.time_elapsed_var = tk.StringVar()  # Variable to store elapsed time
        self.time_elapsed_var.set("0:00")  # Default value
        time_elapsed_label = tk.Label(slider_frame, textvariable=self.time_elapsed_var,
                                    font=self.small_font, fg=self.text_color, bg=self.bg_color)  # Display for elapsed time
        time_elapsed_label.pack(side=tk.LEFT)  # Position on left side
        
        self.song_length_var = tk.StringVar()  # Variable to store total song length
        self.song_length_var.set("0:00")  # Default value
        song_length_label = tk.Label(slider_frame, textvariable=self.song_length_var,
                                font=self.small_font, fg=self.text_color, bg=self.bg_color)  # Display for song length
        song_length_label.pack(side=tk.RIGHT)  # Position on right side
        
        self.progress_slider = ttk.Scale(player_frame, from_=0, to=100, 
                                    orient=tk.HORIZONTAL, length=350)  # Slider for song progress (seek function commented out)
        self.progress_slider.pack(fill=tk.X, padx=20)  # Make slider span width
        
        controls_frame = tk.Frame(player_frame, bg=self.bg_color)  # Create frame for playback controls
        controls_frame.pack(pady=20)  # Add padding
        
        prev_btn = tk.Button(controls_frame, text="⏮", font=("Helvetica", 16),
                        bg=self.bg_color, fg=self.secondary_color, 
                        relief=tk.FLAT, command=self.play_prev_song)  # Create previous song button
        prev_btn.pack(side=tk.LEFT, padx=10)  # Position on left
        
        self.play_pause_text = tk.StringVar()  # Variable for play/pause button text
        self.play_pause_text.set("▶")  # Default to play icon
        
        self.play_pause_btn = tk.Button(controls_frame, textvariable=self.play_pause_text, 
                                    font=("Helvetica", 16), bg=self.primary_color,
                                    fg="white", relief=tk.FLAT, width=2, command=self.toggle_play_pause)  # Create play/pause button
        self.play_pause_btn.pack(side=tk.LEFT, padx=10)  # Position in middle
        
        next_btn = tk.Button(controls_frame, text="⏭", font=("Helvetica", 16),
                        bg=self.bg_color, fg=self.secondary_color, 
                        relief=tk.FLAT, command=self.play_next_song)  # Create next song button
        next_btn.pack(side=tk.LEFT, padx=10)  # Position on right
        
        footer = tk.Label(self.root, text="© 2025 MusicStream", 
                        font=self.small_font, fg=self.secondary_color, bg=self.bg_color)  # Create copyright footer
        footer.pack(side=tk.BOTTOM, pady=10)  # Display at bottom
        
        pygame.mixer.init()  # Initialize audio player
        self.load_music_library()  # Load list of available songs

    def show_logout_main_page(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.pause()  # Pause any playing music
            self.play_pause_text.set("▶")  # Set button to play icon
            self.music_paused = True  # Set music state to paused
        self.show_main_page()  # Display the main page

    
    def load_music_library(self):
        send_message("song")  # Request song list from server
        self.music_files = recieve_message()[2:-2].split(r"', '")  # Parse file paths
        self.music_titles = recieve_message()[2:-2].split(r"', '")  # Parse song titles

        self.song_listbox.delete(0, tk.END)  # Clear the song list display
        for title in self.music_titles:
            self.song_listbox.insert(tk.END, title)  # Add each song to the listbox

    def get_song_length(self, song_path):
        send_message("get_length")  # Request song duration
        send_message(song_path)  # Send path of song to get length for
        length = recieve_message()  # Get the length response
        return float(length)  # Return length as a float

    def play_next_song(self):
        next_index = (self.current_song_index + 1) % len(self.music_titles)  # Calculate next song index with wrapping
        
        self.song_listbox.selection_clear(0, 'end')  # Clear current selection
        self.song_listbox.selection_set(next_index)  # Select next song
        self.song_listbox.see(next_index)  # Ensure next song is visible

        self.set_selected_song()  # Play the newly selected song

    def play_prev_song(self):
        prev_index = (self.current_song_index - 1) % len(self.music_titles)  # Calculate previous song index with wrapping
        
        self.song_listbox.selection_clear(0, 'end')  # Clear current selection
        self.song_listbox.selection_set(prev_index)  # Select previous song
        self.song_listbox.see(prev_index)  # Ensure previous song is visible

        self.set_selected_song()  # Play the newly selected song
    
    def set_selected_song(self):
        selected_indices = self.song_listbox.curselection()  # Get current selection
        self.current_song_index = selected_indices[0]  # Set current song index

        selected_song = self.music_titles[self.current_song_index]  # Get song title
        self.current_song_var.set(selected_song)  # Update display with current song
        self.play_selected_song()  # Play the selected song

    
    def play_selected_song(self):
        if hasattr(self, 'timer_id') and self.timer_id:
            self.root.after_cancel(self.timer_id)  # Cancel any existing timer
            self.timer_id = None  # Reset timer ID

        selected_song_path = self.music_files[self.current_song_index]  # Get path of selected song
        send_message("stream_song")  # Request to stream the song
        send_message(selected_song_path)  # Send the path of song to stream
        
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')  # Create temporary file for song
        temp_filename = temp_file.name  # Store the filename
        temp_file.close()  # Close the file handle
        
        def receive_stream():
            with open(temp_filename, 'wb') as file:
                while True:
                    try:
                        client_socket.settimeout(10)  # Set socket timeout
                        data, _ = client_socket.recvfrom(8192)  # Receive data from server
                        
                        try:
                            message = data.decode()  # Try to decode as message
                            if message == "end_streaming":
                                break  # End streaming if server signals completion
                            elif message.startswith("error:"):
                                messagebox.showerror("Error", message[6:])  # Show error message
                                return
                            elif message == "start_streaming":
                                continue  # Continue if streaming is starting
                        except UnicodeDecodeError:
                            file.write(data)  # Write binary data to file if not a control message
                            
                    except socket.timeout:
                        messagebox.showerror("Error", "Streaming timed out")  # Handle timeout
                        break
            
            try:
                self.play_pause_text.set("⏸")  # Set button to pause icon
                self.music_paused = False  # Set music state to playing
                pygame.mixer.music.load(temp_filename)  # Load the MP3 file
                pygame.mixer.music.play()  # Start playback

                song_length = pygame.mixer.Sound(temp_filename).get_length()  # Get song duration
                self.progress_slider.config(to=song_length)  # Configure slider to match song length
                
                mins, secs = divmod(song_length, 60)  # Convert seconds to minutes and seconds
                self.song_length_var.set(f"{int(mins)}:{int(secs):02d}")  # Display total song length

                self.current_playback_time = 0  # Reset playback time
                self.update_progress()  # Start progress updates
                
            except Exception as e: 
                messagebox.showerror("Error", f"Could not play the song: {str(e)}")  # Handle playback errors
        
        threading.Thread(target=receive_stream, daemon=True).start()  # Start streaming in a separate thread

    def toggle_play_pause(self):
        if not self.music_paused and pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()  # Pause music if currently playing
            self.play_pause_text.set("▶")  # Update button to play icon
            self.music_paused = True  # Update paused state
        else:
            pygame.mixer.music.unpause()  # Resume music if paused
            self.play_pause_text.set("⏸")  # Update button to pause icon
            self.music_paused = False  # Update paused state
    
    def update_progress(self):
        if hasattr(self, 'timer_id') and self.timer_id:
            self.root.after_cancel(self.timer_id)  # Cancel existing timer
            self.timer_id = None  # Reset timer ID
            
        if pygame.mixer.music.get_busy() and not getattr(self, 'music_paused', False):
            self.current_playback_time += 1  # Increment playback time by 1 second
            
            self.progress_slider.set(self.current_playback_time)  # Update slider position
            
            mins, secs = divmod(self.current_playback_time, 60)  # Convert to minutes and seconds
            self.time_elapsed_var.set(f"{int(mins)}:{int(secs):02d}")  # Update elapsed time display
            
            self.timer_id = self.root.after(1000, self.update_progress)  # Schedule next update in 1 second
        else:
            if getattr(self, 'music_paused', False):
                self.timer_id = self.root.after(1000, self.update_progress)  # Continue updates if paused


    def clear_labels(self):
        self.name_var.set("")  # Clear name field
        self.email_var.set("")  # Clear email field
        self.password_var.set("")  # Clear password field
        self.otp_var.set("")  # Clear OTP field

    
    def clear_window(self):
        for widget in self.root.winfo_children():
            if widget != self.logo_frame:
                widget.destroy()  # Remove all widgets except logo frame

if __name__ == "__main__":
    root = tk.Tk()  # Create main application window
    app = App(root)  # Initialize application
    root.mainloop()  # Start the event loop

client_socket.close()  # Close socket connection when application exits
