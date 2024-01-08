import customtkinter as ctk
import tkinter as tk
import pygame
import threading


def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load('sound.mp3')
    pygame.mixer.music.play()


def update_timer():
    global seconds, timer_task, time_until_next_sound, sound_time
    seconds -= 1
    time_until_next_sound -= 1
    timer_label.config(text=f"{seconds // 3600:02}:{(seconds // 60) % 60:02}:{seconds % 60:02}")
    if time_until_next_sound == 0:
        sound_thread = threading.Thread(target=play_sound)
        sound_thread.start()
    if seconds < 0:
        reset_timer()
    if running:
        timer_task = app.after(1000, update_timer)
    return timer_task


def update_start_button_state():
    if timer_label.cget("text") == "00:00:00":
        start_button.configure(state="disabled")
    else:
        start_button.configure(state="normal")


def start_timer():
    global running, timer_task
    running = True
    timer_task = update_timer()


def stop_timer():
    global running, timer_task
    running = False
    app.after_cancel(timer_task)


def reset_timer():
    global seconds, time_until_next_sound, sound_time
    seconds = initial_seconds
    time_until_next_sound = sound_time
    timer_label.config(text=f"{seconds // 3600:02}:{(seconds // 60) % 60:02}:{seconds % 60:02}")


def reset_button_function():
    stop_timer()
    global seconds
    seconds = 0
    timer_label.config(text=f"{seconds // 3600:02}:{(seconds // 60) % 60:02}:{seconds % 60:02}")
    update_start_button_state()


def open_settings():
    settings_window = ctk.CTk()
    settings_window.geometry("300x400")
    settings_window.title("Settings")

    minutes_label = ctk.CTkLabel(settings_window, text="Minutes:")
    minutes_label.pack(pady=5)
    minutes_entry = ctk.CTkEntry(settings_window)
    minutes_entry.pack(pady=5)

    seconds_label = ctk.CTkLabel(settings_window, text="Seconds:")
    seconds_label.pack(pady=5)
    seconds_entry = ctk.CTkEntry(settings_window)
    seconds_entry.pack(pady=5)

    sound_minutes_label = ctk.CTkLabel(settings_window, text="Sound Minutes:")
    sound_minutes_label.pack(pady=5)
    sound_minutes_entry = ctk.CTkEntry(settings_window)
    sound_minutes_entry.pack(pady=5)

    sound_seconds_label = ctk.CTkLabel(settings_window, text="Sound Seconds:")
    sound_seconds_label.pack(pady=5)
    sound_seconds_entry = ctk.CTkEntry(settings_window)
    sound_seconds_entry.pack(pady=5)

    def apply_settings():
        global seconds, initial_seconds, sound_time, time_until_next_sound
        minutes = int(minutes_entry.get() or 0)
        secs = int(seconds_entry.get() or 0)
        seconds = minutes * 60 + secs
        initial_seconds = seconds
        sound_minutes = int(sound_minutes_entry.get() or 0)
        sound_seconds = int(sound_seconds_entry.get() or 0)
        sound_time = sound_minutes * 60 + sound_seconds
        time_until_next_sound = sound_time
        timer_label.config(text=f"{seconds // 3600:02}:{(seconds // 60) % 60:02}:{seconds % 60:02}")
        settings_window.destroy()
        update_start_button_state()

    ok_button = ctk.CTkButton(settings_window, text="OK", command=apply_settings)
    ok_button.pack(pady=10)

    settings_window.mainloop()


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("600x300")
app.title("Timer App")

timer_label = tk.Label(app, text="00:00:00", font=("Arial", 30), bg="#242424", fg="white")
timer_label.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

button_width = 0.15
button_spacing = 0.005
button_vertical_spacing = 0.1

start_button = ctk.CTkButton(app, text="START", command=start_timer)
start_button.place(relx=0.5 - button_width - 0.5 * button_spacing, rely=0.6 - button_vertical_spacing,
                   anchor=ctk.CENTER)

stop_button = ctk.CTkButton(app, text="STOP", command=stop_timer)
stop_button.place(relx=0.5 + button_width + 0.5 * button_spacing, rely=0.6 - button_vertical_spacing, anchor=ctk.CENTER)

settings_button = ctk.CTkButton(app, text="SETTINGS", command=open_settings)
settings_button.place(relx=0.5 - button_width - 0.5 * button_spacing, rely=0.6 + button_vertical_spacing,
                      anchor=ctk.CENTER)

reset_button = ctk.CTkButton(app, text="RESET", command=reset_button_function)
reset_button.place(relx=0.5 + button_width + 0.5 * button_spacing, rely=0.6 + button_vertical_spacing,
                   anchor=ctk.CENTER)

initial_seconds = 0
seconds = 0
sound_time = 0
time_until_next_sound = 0
running = False

update_start_button_state()

app.mainloop()
