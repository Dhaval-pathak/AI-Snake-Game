import tkinter as tk
from tkinter import PhotoImage, messagebox
import subprocess

def play_game():
    root.destroy()  # Close the main window
    subprocess.run(["python", "play_game.py"])

def play_table_driven():
    root.destroy()  # Close the main window
    subprocess.run(["python", "snake_game.py"])

def play_intelligent_agent():
    root.destroy()  # Close the main window
    subprocess.run(["python", "agent.py"])

# Create the main window
root = tk.Tk()
root.title("Snake Game")

# Set window size
w, h = 640, 480
root.geometry(f"{w}x{h}")

# Load background image
background_image = PhotoImage(file="background.png")  # Replace "background.png" with your image file
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Create buttons with some styling
btn_play = tk.Button(root, text="Play Game", command=play_game, font=("Helvetica", 14), bd=5, bg="lightgreen", padx=20, pady=10)
btn_table_driven = tk.Button(root, text="Play with Table-Driven Agent", command=play_table_driven, font=("Helvetica", 14), bd=5, bg="lightblue", padx=20, pady=10)
btn_intelligent_agent = tk.Button(root, text="Play with Intelligent Agent", command=play_intelligent_agent, font=("Helvetica", 14), bd=5, bg="lightcoral", padx=20, pady=10)

# Place buttons in the window
btn_play.place(relx=0.5, rely=0.3, anchor="center")
btn_table_driven.place(relx=0.5, rely=0.5, anchor="center")
btn_intelligent_agent.place(relx=0.5, rely=0.7, anchor="center")

# Center the main window on the screen
root.eval('tk::PlaceWindow . center')

# Run the main loop
root.mainloop()
