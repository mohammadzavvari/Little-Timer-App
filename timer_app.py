import tkinter as tk
from tkinter import messagebox
import time
import os
import pygame


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer App")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        self.time_left = 0
        self.running = False
        self.music_playing = False

        self.timer_label = tk.Label(
            self.root, text="00:00:00", font=("Arial", 24, "bold")
        )
        self.timer_label.pack(pady=20)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        self.start_pause_button = tk.Button(
            self.button_frame,
            text="Start",
            font=("Arial", 12),
            command=self.toggle_start_pause,
        )
        self.start_pause_button.grid(row=0, column=0, padx=5)

        self.resume_button = tk.Button(
            self.button_frame,
            text="Resume",
            font=("Arial", 12),
            command=self.resume_timer,
        )
        self.resume_button.grid(row=0, column=1, padx=5)
        self.resume_button.grid_remove()

        self.cancel_button = tk.Button(
            self.button_frame,
            text="Cancel",
            font=("Arial", 12),
            command=self.cancel_timer,
        )
        self.cancel_button.grid(row=0, column=2, padx=5)
        self.cancel_button.grid_remove()

        self.add_time_frame = tk.Frame(self.root)
        self.add_time_frame.pack(pady=10)

        self.add_30_button = tk.Button(
            self.add_time_frame,
            text="Add 30 seconds",
            font=("Arial", 12),
            command=lambda: self.add_time(30),
        )
        self.add_30_button.grid(row=0, column=0, padx=5)

        self.add_1m_button = tk.Button(
            self.add_time_frame,
            text="Add 1 minute",
            font=("Arial", 12),
            command=lambda: self.add_time(60),
        )
        self.add_1m_button.grid(row=0, column=1, padx=5)

        self.add_5m_button = tk.Button(
            self.add_time_frame,
            text="Add 5 minutes",
            font=("Arial", 12),
            command=lambda: self.add_time(300),
        )
        self.add_5m_button.grid(row=0, column=2, padx=5)

        pygame.mixer.init()

    def parse_time(self, time_str):
        try:
            h, m, s = map(int, time_str.split(":"))
            return h * 3600 + m * 60 + s
        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Please enter time in hh:mm:ss format."
            )
            return None

    def toggle_start_pause(self):
        if not self.running:
            self.start_timer()
        else:
            self.pause_timer()

    def start_timer(self):
        if self.time_left == 0:
            self.time_left = 3600  # Default to 1 hour if no time set
        self.running = True
        self.start_pause_button.config(text="Pause")
        self.resume_button.grid_remove()
        self.cancel_button.grid_remove()
        self.update_timer()

    def pause_timer(self):
        self.running = False
        self.start_pause_button.config(text="Resume")
        self.resume_button.grid()
        self.cancel_button.grid()

    def resume_timer(self):
        if not self.running and self.time_left > 0:
            self.running = True
            self.start_pause_button.config(text="Pause")
            self.resume_button.grid_remove()
            self.cancel_button.grid_remove()
            self.update_timer()

    def cancel_timer(self):
        self.running = False
        self.time_left = 0
        self.start_pause_button.config(text="Start")
        self.resume_button.grid_remove()
        self.cancel_button.grid_remove()
        self.update_display()
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False

    def add_time(self, seconds):
        self.time_left += seconds
        self.update_display()
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False
            self.start_pause_button.config(text="Pause")

    def update_display(self):
        mins, secs = divmod(self.time_left, 60)
        hrs, mins = divmod(mins, 60)
        time_format = f"{hrs:02d}:{mins:02d}:{secs:02d}"
        self.timer_label.config(text=f"{time_format}")

    def update_timer(self):
        if self.running and self.time_left > 0:
            self.update_display()
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        elif self.time_left <= 0:
            self.timer_label.config(text="00:00:00")
            self.running = False
            self.play_sound()
            self.start_pause_button.config(text="Pause Music")

    def play_sound(self):
        try:
            pygame.mixer.music.load("alarm.mp3")
            pygame.mixer.music.play(-1)  # Loop the music
            pygame.mixer.music.set_pos(44)  # Start playback at a specific time
            self.music_playing = True
        except Exception as e:
            messagebox.showerror("Error", f"Could not play sound: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
