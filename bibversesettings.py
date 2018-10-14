import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.scrolledtext

import main

from functools import partial

class BibVerseSettings:
    def __init__(self):
        self.main_window = tk.Tk()

        self.settings_open = False
        self.verses_window_open = False

        self.verse_entry = None

        self.verses = ""
        
        # label = ttk.Label(self.main_window, text=)

        launch_args = partial(main.launch, self.verses)
        configure_btn = ttk.Button(self.main_window, text="Launch", command=launch_args)
        start_btn = ttk.Button(self.main_window, text="Settings", command=self.toggle_settings)

        configure_btn.pack()
        start_btn.pack()

        self.settings_frame = ttk.Frame(self.main_window)

        cycle_time_label = ttk.Label(self.settings_frame, text="Cycle time (mins)")
        cycle_time_label.grid(row=0, column=0)
        cycle_time_slider = tk.Scale(self.settings_frame, from_=1, to=60, orient=tk.HORIZONTAL, resolution=1)
        cycle_time_slider.grid(row=0, column=1)

        settings_delay_label = ttk.Label(self.settings_frame, text="Delay per word (secs)")
        settings_delay_label.grid(row=1, column=0)

        settings_delay_slider = tk.Scale(self.settings_frame, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.1)
        settings_delay_slider.grid(row=1, column=1)

        manage_verses_button = ttk.Button(self.settings_frame, text="Verses...", command=self.show_verses_window)
        manage_verses_button.grid(row=2, column=0, columnspan=2)
        # settings_frame.pack()
        
        # settings_frame.
        # self.main_window.pack()

        self.main_window.mainloop()
        
    def toggle_settings(self):
        # self.settings_window = tk.Toplevel(master=self.main_window)
        if self.settings_open:
            self.settings_frame.pack_forget()
        else:
            self.settings_frame.pack()
        
        self.settings_open = not self.settings_open

    def show_verses_window(self):
        def save_verses():
            self.verses = text.get("1.0", tk.END)
            print(self.verses)
            self.verses_window.destroy()
        def cancel():
            self.verses_window.destroy()

        # def add_verse():
        #     # tk.messagebox.askquestion(title="New verse", message="input verse")
        #     tk.simpledialog.askstring(title="New verse", prompt="input verse")

        self.verses_window = tk.Toplevel(self.main_window)

        label = ttk.Label(self.verses_window, text="Enter verses, one per line")
        label.grid(row=0, column=0, columnspan=2)

        text = tk.scrolledtext.Text(self.verses_window)
        text.grid(row=1, column=0, columnspan=2)

        if len(self.verses) > 0:
            text.insert("1.0", self.verses, tk.END)

        confirm_button = ttk.Button(self.verses_window, text="Confirm", command=save_verses)
        confirm_button.grid(row=2, column=0)

        cancel_button = ttk.Button(self.verses_window, text="Cancel", command=cancel)
        cancel_button.grid(row=2, column=1)

        # add_btn = ttk.Button(self.verses_window, text="+", command=add_verse)
        # add_btn.pack()

        self.verses_window.grab_set()
        self.verses_window.mainloop()

    def get_verses(self):
        return self.verses
    




if __name__ == '__main__':
    b = BibVerseSettings()
