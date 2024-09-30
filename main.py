import tkinter as tk
from tkinter import font, messagebox, filedialog
import json
from logic import *


with open("content/config.json", "r") as file:
    config = json.load(file)


def start_gui():
    root = tk.Tk()
    root.title("Art Scaner")
    root.configure(bg="black")
    bind_key_var = tk.StringVar(value=config["bind"])

    listener = Listener(bind_key_var.get())
    custom_font = font.Font(family="Helvetica", size=16, weight="bold")

    TRACKING_ENABLED = False

    def toggle_switch():
        global TRACKING_ENABLED
        TRACKING_ENABLED = True if switch_var.get() else False
        if TRACKING_ENABLED:
            listener.create_bind(bind_key_var.get())
        else:
            print("remove_bind")
            listener.remove_bind()
        print(f"SWITCH: {TRACKING_ENABLED}")

    def update_bind_gui():
        global TRACKING_ENABLED
        update_bind(bind_key_var.get())
        root.focus_set()

    def clear_cache_gui():
        clear_cache()
        messagebox.showinfo("Cache", "Cache cleared!")

    def save_file_gui():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("Json files", "*.json"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )

        if file_path:
            if save_file(file_path):
                messagebox.showinfo("File saved", f"File path: {file_path}")
            else:
                messagebox.showerror("Error", "Failed to save the file")

    def exit_app():
        root.destroy()
        exit()

    root.protocol("WM_DELETE_WINDOW", exit_app)

    # GUI

    switch_var = tk.BooleanVar(value=False)
    toggle_button = tk.Checkbutton(
        root,
        text="ON/OFF",
        variable=switch_var,
        command=toggle_switch,
        font=custom_font,
        bg="black",
        fg="white",
        selectcolor="gray",
    )
    toggle_button.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    bind_entry = tk.Entry(
        root, textvariable=bind_key_var, font=custom_font, width=10, justify="center"
    )
    bind_entry.grid(row=1, column=0, padx=10, pady=10)

    bind_button = tk.Button(
        root,
        text="Change",
        command=update_bind_gui,
        font=custom_font,
        bg="gray",
        fg="white",
    )
    bind_button.grid(row=1, column=1, padx=10, pady=10)

    clear_button = tk.Button(
        root,
        text="Clear cache",
        command=clear_cache_gui,
        font=custom_font,
        bg="gray",
        fg="white",
        width=15,
    )
    clear_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

    export_button = tk.Button(
        root,
        text="Save file",
        command=save_file_gui,
        font=custom_font,
        bg="gray",
        fg="white",
        width=15,
    )
    export_button.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

    root.mainloop()


if __name__ == "__main__":
    start_gui()
