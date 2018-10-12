import tkinter as tk
import tkinter.ttk as ttk
class BibVerseSettings:
    def __init__(self):
        self.main_window = tk.Tk()

        self.settings_open = False
        self.verses_window_open = False
        
        # label = ttk.Label(self.main_window, text=)
        configure_btn = ttk.Button(self.main_window, text="Launch")
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
        verses_window = tk.Toplevel(self.main_window)

        label = ttk.Label(verses_window, text="Verses window")
        label.pack()
        verses_window.grab_set()
        verses_window.mainloop()



if __name__ == '__main__':
    b = BibVerseSettings()