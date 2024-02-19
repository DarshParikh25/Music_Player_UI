import os
import pygame
from tkinter import Tk, Button, Label, filedialog

class MusicPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Player")
        self.master.geometry("500x200")
        
        self.music_folder = ""
        self.current_index = 0
        self.is_playing = False
        
        self.label_status = Label(master, text="Select a folder to play music.")
        self.label_status.pack(pady = 10)
        
        self.button_select_folder = Button(master, text = "Select Folder", command = self.select_folder)
        self.button_select_folder.pack(pady = 10)
        
        self.button_play = Button(master, text = "Play", command = self.play_music, state="disabled")
        self.button_play.pack(side = "left", padx = 10)
        
        self.button_pause = Button(master, text = "Pause", command = self.pause_music, state="disabled")
        self.button_pause.pack(side = "left", padx = 10)
        
        self.button_stop = Button(master, text = "Stop", command = self.stop_music, state="disabled")
        self.button_stop.pack(side = "left", padx = 10)
        
        self.label_song_name = Label(master, text = "", wraplength = 175)
        self.label_song_name.pack(side = "right", padx = 10)
        
        self.button_previous = Button(master, text = "Previous", command = self.play_previous, state = "disabled")
        self.button_previous.pack(side="right", padx = 10)
        
        self.button_next = Button(master, text = "Next", command = self.play_next, state = "disabled")
        self.button_next.pack(side = "right", padx = 10)
    
    def select_folder(self):
        self.music_folder = filedialog.askdirectory()
        if self.music_folder:
            self.label_status.config(text = "Folder selected: " + self.music_folder)
            self.load_music_files()
    
    def load_music_files(self):
        self.music_files = [file for file in os.listdir(self.music_folder) if file.endswith(('.mp3', '.wav'))]
        if self.music_files:
            self.button_play.config(state = "normal")
            if len(self.music_files) > 1:
                self.button_next.config(state = "normal")
            self.current_index = 0
            self.play_music()
            self.update_buttons_state()

    
    def play_music(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(self.music_folder, self.music_files[self.current_index]))
        pygame.mixer.music.play()
        self.is_playing = True
        self.button_play.config(state = "disabled")
        self.button_pause.config(state = "normal")
        self.button_stop.config(state = "normal")
        self.update_song_name()
    
    def pause_music(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
    
    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.button_play.config(state = "normal")
        self.button_pause.config(state = "disabled")
        self.button_stop.config(state = "disabled")

    def play_next(self):
        if self.music_folder and self.music_files:
            self.current_index += 1
            self.play_music()
            self.update_buttons_state()

    def play_previous(self):
        if self.music_folder and self.music_files:
            self.current_index -= 1
            self.play_music()
            self.update_buttons_state()

    def update_buttons_state(self):
        if len(self.music_files) == 1:
            self.button_previous.config(state = "disabled")
            self.button_next.config(state = "disabled")
        elif self.current_index == 0:
            self.button_previous.config(state = "disabled")
            self.button_next.config(state = "normal")
        elif self.current_index == len(self.music_files) - 1:
            self.button_previous.config(state = "normal")
            self.button_next.config(state = "disabled")
        else:
            self.button_previous.config(state = "normal")
            self.button_next.config(state = "normal")

    def update_song_name(self):
        self.label_song_name.config(text = "Now Playing: " + self.music_files[self.current_index])

def main():
    root = Tk()
    music_player = MusicPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()