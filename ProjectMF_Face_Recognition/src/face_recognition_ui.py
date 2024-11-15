import tkinter as tk
from tkinter import ttk

# Create main window
window = tk.Tk()
window.title("Face Recognition Security System")
window.geometry("800x600")
window.configure(bg="#1a1a1a")  # Set background color to dark mode

# Define colors
bg_color = "#2d2d2d"  # Dark gray background
button_color = "#4CAF50"  # Green button color
text_color = "#ffffff"  # White text color

# Main title label
title_label = tk.Label(window, text="Face Recognition Security System", font=("Helvetica", 24, "bold"), bg=bg_color, fg=text_color)
title_label.pack(pady=20)

# Frame for video display with rounded corners
video_frame = ttk.Frame(window, width=600, height=400, style="Custom.TFrame")
video_frame.pack(pady=20)

# Recognize face button with icon
recognize_img = tk.PhotoImage(file="android-contact.png")  # Replace with your icon image path
recognize_button = tk.Button(window, text="Recognize Face", image=recognize_img, compound=tk.LEFT, font=("Helvetica", 16, "bold"),
                             bg=button_color, fg=text_color, bd=0, relief=tk.FLAT)
recognize_button.pack(pady=20)

# Result label
result_label = tk.Label(window, text="Result: Unknown", font=("Helvetica", 18), bg=bg_color, fg=text_color)
result_label.pack(pady=10)

# Footer label
footer_label = tk.Label(window, text="© 2024 Face Recognition Security Inc.", font=("Helvetica", 10), bg=bg_color, fg=text_color)
footer_label.pack(pady=10)

# Configure style for rounded frame
style = ttk.Style()
style.configure("Custom.TFrame", background=bg_color, borderwidth=0, relief=tk.FLAT)

# Run the main event loop
window.mainloop()
