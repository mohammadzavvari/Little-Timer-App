import tkinter as tk
from tkinter import messagebox
import time
import os
import pygame

from timer_app import TimerApp

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
