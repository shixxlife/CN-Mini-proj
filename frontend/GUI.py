import tkinter as tk
from tkinter import ttk, filedialog
import os
from PIL import Image, ImageTk
import pygame
import time
import threading

class SpotifyClone:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Streaming Platform")
        self.root.geometry("1000x600")
        self.root.configure(bg="#121212")
        
        # Set a custom style for buttons and elements
        self.style = ttk.Style()
        self.style.configure("TScale", background="#181818")
        self.style.configure("TButton", background="#333333", foreground="black")
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Track variables
        self.current_track = None
        self.is_playing = False
        self.tracks = []
        self.track_index = 0
        self.playlists = ["Liked Songs", "Recently Played", "Your Top Songs"]
        
        # Create a sample music library
        self.music_library = [
            {"title": "Song 1", "artist": "Artist 1", "album": "Album 1", "duration": "3:45"},
            {"title": "Song 2", "artist": "Artist 2", "album": "Album 2", "duration": "4:20"},
            {"title": "Song 3", "artist": "Artist 1", "album": "Album 3", "duration": "2:55"},
            {"title": "Song 4", "artist": "Artist 3", "album": "Album 1", "duration": "3:30"},
            {"title": "Song 5", "artist": "Artist 2", "album": "Album 4", "duration": "5:10"},
        ]
        
        # Create main frames
        self.create_sidebar()
        self.create_content_area()
        self.create_playback_controls()
        
        # Update track progress (simulated)
        self.update_progress()
    
    def create_sidebar(self):
        # Sidebar frame
        sidebar = tk.Frame(self.root, bg="#000000", width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Logo
        logo_label = tk.Label(sidebar, text="YourMusic", font=("Helvetica", 16, "bold"), 
                              bg="#000000", fg="white")
        logo_label.pack(pady=20)
        
        # Navigation buttons
        nav_items = ["Home", "Search", "Your Library"]
        for item in nav_items:
            nav_frame = tk.Frame(sidebar, bg="#000000", padx=10, pady=5)
            nav_frame.pack(fill=tk.X)
            
            btn = tk.Button(nav_frame, text=item, font=("Helvetica", 12), 
                           bg="#333333", fg="black", bd=1, 
                           activebackground="#444444", activeforeground="#FFFFFF",
                           highlightthickness=1, width=15, anchor="w", padx=10, relief="raised")
            btn.pack(fill=tk.X)
        
        # Separator
        separator = ttk.Separator(sidebar, orient='horizontal')
        separator.pack(fill=tk.X, padx=10, pady=10)
        
        # Playlists
        playlist_label = tk.Label(sidebar, text="PLAYLISTS", font=("Helvetica", 10, "bold"), 
                                 bg="#000000", fg="black")
        playlist_label.pack(anchor="w", padx=10, pady=5)
        
        # Create playlist button
        create_btn_frame = tk.Frame(sidebar, bg="#000000", padx=10, pady=2)
        create_btn_frame.pack(fill=tk.X)
        
        create_playlist_btn = tk.Button(create_btn_frame, text="Create Playlist", font=("Helvetica", 10),
                                       bg="#333333", fg="black", bd=1, relief="raised",
                                       activebackground="#444444", activeforeground="#FFFFFF")
        create_playlist_btn.pack(fill=tk.X)
        
        # Playlist items
        for playlist in self.playlists:
            playlist_frame = tk.Frame(sidebar, bg="#000000", padx=10, pady=2)
            playlist_frame.pack(fill=tk.X)
            
            playlist_btn = tk.Button(playlist_frame, text=playlist, font=("Helvetica", 10),
                                   bg="#333333", fg="black", bd=1, anchor="w", relief="raised",
                                   activebackground="#444444", activeforeground="#FFFFFF")
            playlist_btn.pack(fill=tk.X)
    
    def create_content_area(self):
        # Main content area
        content_frame = tk.Frame(self.root, bg="#121212")
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Top navigation bar with back/forward buttons
        nav_bar = tk.Frame(content_frame, bg="#121212", height=40)
        nav_bar.pack(fill=tk.X, pady=10, padx=20)
        
        back_btn = tk.Button(nav_bar, text="<", font=("Helvetica", 16, "bold"), 
                           bg="#333333", fg="black", width=2, height=1, bd=1, relief="raised",
                           activebackground="#444444", activeforeground="#FFFFFF")
        back_btn.pack(side=tk.LEFT, padx=5)
        
        forward_btn = tk.Button(nav_bar, text=">", font=("Helvetica", 16, "bold"), 
                              bg="#333333", fg="black", width=2, height=1, bd=1, relief="raised",
                              activebackground="#444444", activeforeground="#FFFFFF")
        forward_btn.pack(side=tk.LEFT, padx=5)
        
        # User profile
        profile_frame = tk.Frame(nav_bar, bg="#121212", bd=0)
        profile_frame.pack(side=tk.RIGHT)
        
        profile_btn = tk.Button(profile_frame, text="User", font=("Helvetica", 10), 
                              bg="#333333", fg="black", bd=1, relief="raised",
                              activebackground="#444444", activeforeground="#FFFFFF")
        profile_btn.pack(padx=5, pady=2)
        
        # Content sections
        # Recently played section
        section_frame = tk.Frame(content_frame, bg="#121212")
        section_frame.pack(fill=tk.X, padx=20, pady=10, anchor="w")
        
        section_label = tk.Label(section_frame, text="Recently Played", font=("Helvetica", 16, "bold"),
                                bg="#121212", fg="white")
        section_label.pack(anchor="w")
        
        # Cards section (album/playlist cards)
        cards_frame = tk.Frame(content_frame, bg="#121212")
        cards_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Create some example cards
        for i in range(5):
            card = tk.Frame(cards_frame, bg="#181818", width=150, height=200, bd=1, relief="raised")
            card.pack(side=tk.LEFT, padx=10)
            card.pack_propagate(False)
            
            # Card content
            card_img_frame = tk.Frame(card, bg="#282828", width=130, height=130)
            card_img_frame.pack(padx=10, pady=10)
            card_img_frame.pack_propagate(False)
            
            card_img_label = tk.Label(card_img_frame, text="Album Art", bg="#282828", fg="white")
            card_img_label.pack(expand=True)
            
            card_title = tk.Label(card, text=f"Album {i+1}", bg="#181818", fg="#FFFFFF",
                                font=("Helvetica", 10, "bold"))
            card_title.pack(anchor="w", padx=10)
            
            card_subtitle = tk.Label(card, text=f"Artist {i+1}", bg="#181818", fg="#AAAAAA",
                                   font=("Helvetica", 8))
            card_subtitle.pack(anchor="w", padx=10)
        
        # Songs table section
        table_frame = tk.Frame(content_frame, bg="#121212")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Table header
        header_frame = tk.Frame(table_frame, bg="#121212")
        header_frame.pack(fill=tk.X, padx=5)
        
        headers = ["#", "TITLE", "ARTIST", "ALBUM", "DURATION"]
        widths = [50, 300, 200, 200, 100]
        
        for i, header in enumerate(headers):
            header_label = tk.Label(header_frame, text=header, font=("Helvetica", 10), 
                                   bg="#121212", fg="#AAAAAA", width=widths[i]//10, anchor="w")
            header_label.pack(side=tk.LEFT, padx=5)
        
        # Separator
        separator = ttk.Separator(table_frame, orient='horizontal')
        separator.pack(fill=tk.X, padx=5, pady=5)
        
        # Song rows
        songs_frame = tk.Frame(table_frame, bg="#121212")
        songs_frame.pack(fill=tk.BOTH, expand=True)
        
        for i, song in enumerate(self.music_library):
            row_bg = "#121212" if i % 2 == 0 else "#181818"
            row_frame = tk.Frame(songs_frame, bg=row_bg)
            row_frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Song number
            num_label = tk.Label(row_frame, text=str(i+1), font=("Helvetica", 10), 
                               bg=row_bg, fg="#AAAAAA", 
                               width=widths[0]//10, anchor="w")
            num_label.pack(side=tk.LEFT, padx=5)
            
            # Song title
            title_label = tk.Label(row_frame, text=song["title"], font=("Helvetica", 10), 
                                 bg=row_bg, fg="#FFFFFF", 
                                 width=widths[1]//10, anchor="w")
            title_label.pack(side=tk.LEFT, padx=5)
            
            # Artist
            artist_label = tk.Label(row_frame, text=song["artist"], font=("Helvetica", 10), 
                                  bg=row_bg, fg="#AAAAAA", 
                                  width=widths[2]//10, anchor="w")
            artist_label.pack(side=tk.LEFT, padx=5)
            
            # Album
            album_label = tk.Label(row_frame, text=song["album"], font=("Helvetica", 10), 
                                 bg=row_bg, fg="#AAAAAA", 
                                 width=widths[3]//10, anchor="w")
            album_label.pack(side=tk.LEFT, padx=5)
            
            # Duration
            duration_label = tk.Label(row_frame, text=song["duration"], font=("Helvetica", 10), 
                                    bg=row_bg, fg="#AAAAAA", 
                                    width=widths[4]//10, anchor="w")
            duration_label.pack(side=tk.LEFT, padx=5)
            
            # Make row clickable
            row_frame.bind("<Button-1>", lambda e, track=song: self.play_track(track))
            for widget in row_frame.winfo_children():
                widget.bind("<Button-1>", lambda e, track=song: self.play_track(track))
            
    def create_playback_controls(self):
        # Footer with playback controls
        footer = tk.Frame(self.root, bg="#181818", height=90)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        footer.pack_propagate(False)
        
        # Now playing info (left)
        now_playing = tk.Frame(footer, bg="#181818")
        now_playing.pack(side=tk.LEFT, padx=20, fill=tk.Y)
        
        # Album art placeholder
        album_frame = tk.Frame(now_playing, bg="#282828", width=60, height=60, bd=1, relief="raised")
        album_frame.pack(side=tk.LEFT, padx=5)
        album_frame.pack_propagate(False)
        
        album_label = tk.Label(album_frame, text="Art", bg="#282828", fg="white")
        album_label.pack(expand=True)
        
        # Song info
        song_info = tk.Frame(now_playing, bg="#181818")
        song_info.pack(side=tk.LEFT, padx=10)
        
        self.song_title_label = tk.Label(song_info, text="No track selected", font=("Helvetica", 10, "bold"),
                                       bg="#181818", fg="#FFFFFF")
        self.song_title_label.pack(anchor="w")
        
        self.song_artist_label = tk.Label(song_info, text="", font=("Helvetica", 8),
                                        bg="#181818", fg="#AAAAAA")
        self.song_artist_label.pack(anchor="w")
        
        # Playback controls (center)
        controls = tk.Frame(footer, bg="#181818")
        controls.pack(side=tk.LEFT, expand=True)
        
        # Control buttons
        control_btns = tk.Frame(controls, bg="#181818")
        control_btns.pack(pady=5)
        
        # Create media control buttons with visible styling
        shuffle_btn = tk.Button(control_btns, text="⇄", font=("Helvetica", 10), 
                               bg="#333333", fg="black", bd=1,
                               activebackground="#444444", activeforeground="#FFFFFF",
                               relief="raised")
        shuffle_btn.pack(side=tk.LEFT, padx=10)
        
        prev_btn = tk.Button(control_btns, text="⏮", font=("Helvetica", 12), 
                            bg="#333333", fg="black", bd=1,
                            activebackground="#444444", activeforeground="#FFFFFF",
                            command=self.previous_track, relief="raised")
        prev_btn.pack(side=tk.LEFT, padx=10)
        
        self.play_btn = tk.Button(control_btns, text="▶", font=("Helvetica", 16), 
                                bg="#333333", fg="black", bd=1,
                                activebackground="#444444", activeforeground="#FFFFFF",
                                command=self.toggle_playback, relief="raised")
        self.play_btn.pack(side=tk.LEFT, padx=10)
        
        next_btn = tk.Button(control_btns, text="⏭", font=("Helvetica", 12), 
                            bg="#333333", fg="black", bd=1,
                            activebackground="#444444", activeforeground="#FFFFFF",
                            command=self.next_track, relief="raised")
        next_btn.pack(side=tk.LEFT, padx=10)
        
        repeat_btn = tk.Button(control_btns, text="🔁", font=("Helvetica", 10), 
                              bg="#333333", fg="black", bd=1,
                              activebackground="#444444", activeforeground="#FFFFFF",
                              relief="raised")
        repeat_btn.pack(side=tk.LEFT, padx=10)
        
        # Timeline slider
        timeline = tk.Frame(controls, bg="#181818")
        timeline.pack(fill=tk.X, padx=20)
        
        self.current_time = tk.Label(timeline, text="0:00", font=("Helvetica", 8),
                                   bg="#181818", fg="white")
        self.current_time.pack(side=tk.LEFT, padx=5)
        
        # Make progress bar more visible with custom styling
        progress_frame = tk.Frame(timeline, bg="#666666", bd=1, relief="sunken")
        progress_frame.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.progress_bar = ttk.Scale(progress_frame, from_=0, to=100, orient="horizontal", length=400)
        self.progress_bar.pack(fill=tk.X, expand=True)
        
        self.total_time = tk.Label(timeline, text="0:00", font=("Helvetica", 8),
                                 bg="#181818", fg="white")
        self.total_time.pack(side=tk.LEFT, padx=5)
        
        # Volume control (right)
        volume = tk.Frame(footer, bg="#181818")
        volume.pack(side=tk.RIGHT, padx=20, fill=tk.Y)
        
        volume_icon = tk.Label(volume, text="🔊", font=("Helvetica", 10),
                              bg="#181818", fg="white")
        volume_icon.pack(side=tk.LEFT, padx=5)
        
        # Make volume slider more visible
        volume_frame = tk.Frame(volume, bg="#666666", bd=1, relief="sunken")
        volume_frame.pack(side=tk.LEFT, padx=5)
        
        volume_slider = ttk.Scale(volume_frame, from_=0, to=100, orient="horizontal", length=100)
        volume_slider.set(70)  # Default volume
        volume_slider.pack()
    
    def play_track(self, track):
        self.current_track = track
        self.song_title_label.config(text=track["title"])
        self.song_artist_label.config(text=track["artist"])
        self.play_btn.config(text="⏸")
        self.is_playing = True
        
        # Update track duration
        minutes, seconds = track["duration"].split(":")
        total_seconds = int(minutes) * 60 + int(seconds)
        self.progress_bar.config(to=total_seconds)
        self.total_time.config(text=track["duration"])
        
        # In a real app, you would play the actual music file here
        # For this example, we'll just simulate playback
        print(f"Now playing: {track['title']} by {track['artist']}")
    
    def toggle_playback(self):
        if self.current_track is None:
            return
        
        if self.is_playing:
            self.is_playing = False
            self.play_btn.config(text="▶")
            # In a real app: pygame.mixer.music.pause()
        else:
            self.is_playing = True
            self.play_btn.config(text="⏸")
            # In a real app: pygame.mixer.music.unpause()
    
    def next_track(self):
        if not self.music_library:
            return
        
        self.track_index = (self.track_index + 1) % len(self.music_library)
        self.play_track(self.music_library[self.track_index])
    
    def previous_track(self):
        if not self.music_library:
            return
        
        self.track_index = (self.track_index - 1) % len(self.music_library)
        self.play_track(self.music_library[self.track_index])
    
    def update_progress(self):
        if self.is_playing and self.current_track:
            current_value = self.progress_bar.get()
            
            # Get total track duration in seconds
            minutes, seconds = self.current_track["duration"].split(":")
            total_seconds = int(minutes) * 60 + int(seconds)
            
            if current_value < total_seconds:
                self.progress_bar.set(current_value + 1)
                
                # Update current time label
                current_minutes = int(current_value // 60)
                current_seconds = int(current_value % 60)
                self.current_time.config(text=f"{current_minutes}:{current_seconds:02d}")
            else:
                # Track finished, play next
                self.next_track()
        
        # Update every second
        self.root.after(1000, self.update_progress)
    
    def load_music(self):
        # In a real app, you would implement this to load actual music files
        # from a directory or streaming service
        pass

def main():
    root = tk.Tk()
    app = SpotifyClone(root)
    root.mainloop()

if __name__ == "__main__":
    main()