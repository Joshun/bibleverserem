import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.scrolledtext

import requests
import platform

import math

import datetime

from time import sleep
from auth import auth_token
import config
import threading

import sys

from functools import partial
from queue import Queue, Empty

import json
import bibverseworker

from bibindices import Indices

class BibVerseSettings:
    def __init__(self):
        self.indices = Indices()


        self.thread_done = False
        self.started = False
        self.closing = False
        # print(platform.system())

        # if platform.system() == 'Windows':
        #     import winbibversedisplay
        #     self.bible_verse_display = winbibversedisplay.WinBibleVerseDisplay()
        # elif platform.system() == 'Linux':
        #     print("yay Linux")
        #     import linbibversedisplay
        #     self.bible_verse_display = linbibversedisplay.LinBibleVerseDisplay()
        # else:
        #     raise NotImplementedError("OS not supported")


        # self.worker_thread = None
        # self.worker_thread = threading.Thread(target=self.run)

        self.errors_queue = Queue()
        self.errors_thread = threading.Thread(target=self.errors_process, daemon=True)
        self.errors_thread.start()

        self.worker_thread = bibverseworker.BibVerseWorker()
        self.worker_thread.setDaemon(True)
        self.worker_thread.set_errors_queue(self.errors_queue)

        self.main_window = tk.Tk()

        self.settings_open = False
        self.verses_window_open = False

        self.verse_entry = None

        self.custom_verses = ""
        self.verses = ""

        # self.settings = { "verses": "" }

        
        # label = ttk.Label(self.main_window, text=)

        self.main_window.protocol("WM_DELETE_WINDOW", self.close)

        # launch_args = partial(main.launch, self.verses)
        # configure_btn = ttk.Button(self.main_window, text="Launch", command=launch_args)
        self.start_btn = ttk.Button(self.main_window, text="Launch", command=self.launch)
        self.stop_btn = ttk.Button(self.main_window, text="Stop", command=self.stop)
        settings_btn = ttk.Button(self.main_window, text="Settings", command=self.toggle_settings)

        self.stop_btn.config(state=tk.DISABLED)


        self.start_btn.pack()
        self.stop_btn.pack()
        settings_btn.pack()

        self.settings_frame = ttk.Frame(self.main_window)

        cycle_time_label = ttk.Label(self.settings_frame, text="Cycle time (mins)")
        cycle_time_label.grid(row=0, column=0)
        self.cycle_time_slider = tk.Scale(self.settings_frame, from_=1, to=60, orient=tk.HORIZONTAL, resolution=1)
        self.cycle_time_slider.grid(row=0, column=1)

        settings_delay_label = ttk.Label(self.settings_frame, text="Delay per word (secs)")
        settings_delay_label.grid(row=1, column=0)

        self.settings_delay_slider = tk.Scale(self.settings_frame, from_=0.1, to=1, orient=tk.HORIZONTAL, resolution=0.1)
        self.settings_delay_slider.grid(row=1, column=1)

        self.mode_select_frame = tk.Frame(self.settings_frame)
        self.mode_select_frame.grid(row=2, column=0, columnspan=2)

        self.mode_select_var = tk.IntVar(None, 1)

        mode_select_radio_by_book = ttk.Radiobutton(self.mode_select_frame, text="By book", variable=self.mode_select_var, value=1, command=self.set_bybook)
        mode_select_radio_by_book.pack(side=tk.LEFT)        
        mode_select_radio_by_chapter = ttk.Radiobutton(self.mode_select_frame, text="By chapter", variable=self.mode_select_var, value=2, command=self.set_bychapter)
        mode_select_radio_by_chapter.pack(side=tk.LEFT)
        mode_select_custom = ttk.Radiobutton(self.mode_select_frame, text="Custom", variable=self.mode_select_var, value=3, command=self.set_custom)
        mode_select_custom.pack(side=tk.LEFT)

        self.manage_verses_button = ttk.Button(self.settings_frame, text="Verses...", command=self.show_verses_window)
        # self.manage_verses_button.grid(row=3, column=0, columnspan=2)
        # self.manage_verses_button.configure(state='disabled')


        self.chapter_verse_frame = tk.Frame(self.settings_frame)
        # self.chapter_verse_frame.grid(row=4, column=0, columnspan=2)

        self.book_var = tk.StringVar()
        # options = ["Genesis", "Exodus"]
        options = self.indices.get_books()
        # self.book_chapters = {"Genesis": 50, "Exodus": 40}
        self.book_var.set(self.indices.get_books()[0])
        book_menu = ttk.OptionMenu(self.chapter_verse_frame, self.book_var, options[0], *options)
        book_menu.pack(side=tk.LEFT)

        self.book_var.trace("w", self.reload_chapters)

        self.chapter_var = tk.IntVar()
        chapters = self.indices.get_chapters(self.book_var.get())
        self.chapter_menu = ttk.OptionMenu(self.chapter_verse_frame, self.chapter_var, chapters[0], *chapters)
        self.chapter_menu.pack()
        # settings_frame.pack()
        
        self.book_frame = tk.Frame(self.settings_frame)
        self.book_menu = ttk.OptionMenu(self.book_frame, self.book_var, options[0], *options)
        self.book_menu.pack()

        # settings_frame.
        # self.main_window.pack()
        # self.chapter_verse_frame.pack_forget()
        # self.manage_verses_button.pack_forget()

        self.load_from_file()
        self.main_window.mainloop()


    def set_mode(self, mode):
        if mode == 1:
            self.set_bybook()
        elif mode == 2:
            self.set_bychapter()
        elif mode == 3:
            self.set_custom()
        else:
            raise Exception("This should not happen")
    
    def set_bybook(self):
        self.chapter_verse_frame.grid_forget()
        self.manage_verses_button.grid_forget()
        self.book_frame.grid(row=3, column=0, columnspan=2)

    def set_bychapter(self):
        # self.chapter_verse_frame.config.set
        self.manage_verses_button.grid_forget()
        self.book_frame.grid_forget()
        self.chapter_verse_frame.grid(row=3, column=0, columnspan=2)

        # self.manage_verses_button.configure(state='disabled')
        # for child in self.chapter_verse_frame.winfo_children():
        #     child.configure(state='enable')
    
    def set_custom(self):
        self.book_frame.grid_forget()
        self.chapter_verse_frame.grid_forget()        
        self.manage_verses_button.grid(row=3, column=0, columnspan=2)
        # self.manage_verses_button.configure(state='enable')
        # # self.chapter_verse_frame.pack_forget()
        # # self.manage_verses_button.pack()
        # for child in self.chapter_verse_frame.winfo_children():
        #     child.configure(state='disabled')
    
    def book_change(self):
        book = self.book_var.get()
        # self.

    def errors_process(self):
        while True:
            err = self.errors_queue.get()
            print("Error:")
            print(err)
            tkinter.messagebox.showerror("Error", err)
            self.stop()
            
            while not self.errors_queue.empty():
                try:
                    self.errors_queue.get(False)
                except Empty:
                    continue
                self.errors_queue.task_done()
        
    def toggle_settings(self):
        # self.settings_window = tk.Toplevel(master=self.main_window)
        if self.settings_open:
            self.settings_frame.pack_forget()
        else:
            self.settings_frame.pack()
        
        self.settings_open = not self.settings_open

    def show_verses_window(self):
        def save_verses():
            self.custom_verses = text.get("1.0", tk.END)
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

        if len(self.custom_verses) > 0:
            text.insert("1.0", self.custom_verses, tk.END)

        confirm_button = ttk.Button(self.verses_window, text="Confirm", command=save_verses)
        confirm_button.grid(row=2, column=0)

        cancel_button = ttk.Button(self.verses_window, text="Cancel", command=cancel)
        cancel_button.grid(row=2, column=1)

        # set focus
        self.verses_window.focus_set()
        text.focus_set()

        # add_btn = ttk.Button(self.verses_window, text="+", command=add_verse)
        # add_btn.pack()

        self.verses_window.grab_set()

        # self.verses_window.lift()
        # self.verses_window.attributes('-topmost', True)
        # self.verses_window.attributes('-topmost', False)
        # self.verses_window.deiconify()
        self.verses_window.mainloop()

    def get_verses(self):
        return self.verses

    def launch(self):
        mode = self.mode_select_var.get()
        if mode == 1:
            book = self.book_var.get()
            verses_list = [ "{} {}".format(book, chapter) for chapter in self.indices.get_chapters(book) ]
            self.verses = "\n".join(verses_list)
        elif mode == 2:
            book = self.book_var.get()
            chapter = self.chapter_var.get()
            verses_list = [ "{} {}:{}".format(book, chapter, verse) for verse in self.indices.get_verses(book, chapter) ]
            self.verses = "\n".join(verses_list)
        elif mode == 3:
            self.verses = self.custom_verses
        else:
            raise Exception("Should not happen")

        if len(self.verses.replace("\n", "")) == 0:
            tkinter.messagebox.showinfo("Setup verses", "You must add verses in the settings first")
            return

        self.thread_done = False

        self.stop_btn.config(state=tk.NORMAL)
        self.start_btn.config(state=tk.DISABLED)

        self.worker_thread.reset()
        self.worker_thread.set_options(cycle_time=self.cycle_time_slider.get(), per_word_time=self.settings_delay_slider.get(), verses=self.verses)

        if not self.started:
            self.worker_thread.start()
            self.started = True
    
    def stop(self):
        self.thread_done = True
        self.worker_thread.set_done()
        self.stop_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.NORMAL)


    def close(self):
        print("CLOSE")
        self.closing = True
        self.stop()
        self.worker_thread.set_done()
        self.worker_thread.set_closing()

        self.save_to_file()

        self.main_window.destroy()

        if self.started:
            print('WAIT')
            self.worker_thread.join()
            print("done")
        

    def save_to_file(self):
        file_structure = { "custom_verses": self.custom_verses, "cycle_time": self.cycle_time_slider.get(), "per_word_time": self.settings_delay_slider.get(), "mode": self.mode_select_var.get() }
        with open("settings.json", "w") as f:
            json.dump(file_structure, f)
    
    def load_from_file(self):
        try:
            with open("settings.json", "r") as f:
                file_structure = json.load(f)
                print(file_structure)
                self.custom_verses = file_structure["custom_verses"]
                self.cycle_time_slider.set(int(file_structure["cycle_time"]))
                self.settings_delay_slider.set(float(file_structure["per_word_time"]))
                self.mode_select_var.set(int(file_structure["mode"]))
                self.set_mode(self.mode_select_var.get())

        except IOError:
            print('config file not found')
    
    def reload_chapters(self, *args):
        # nchapters = self.book_chapters[self.book_var.get()]
        chapters = self.indices.get_chapters(self.book_var.get())
        self.chapter_menu['menu'].delete(0, 'end')
        for chapter in chapters:
            self.chapter_menu['menu'].add_command(label=str(chapter), command=tk._setit(self.chapter_var,str(chapter)))
        # set back to first chapter to avoid it being set to non-existent chapters
        self.chapter_var.set(1)
        

def get_passage_text(passage):
    encoded_passage = passage.replace(" ", "+")
    r = requests.get(
        'https://api.esv.org/v3/passage/text/?q={0}'.format(encoded_passage),
        params={'include-verse-numbers': 'false', 'include-headings': 'false', 'include-footnotes': 'false'},
        headers={'Authorization': 'Token {}'.format(auth_token)}
        )
    return r

#   print(r.json()['passages'])

# toaster = ToastNotifier()





if __name__ == '__main__':
    b = BibVerseSettings()
