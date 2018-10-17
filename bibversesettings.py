import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.scrolledtext

import requests
import platform
import winbibversedisplay

import math

import win10toast

import datetime

from time import sleep
from auth import auth_token
import config
import threading

import sys

from functools import partial

import json

class BibVerseSettings:
    def __init__(self):

        self.thread_done = False
        self.started = False
        self.closing = False
        print(platform.system())

        if platform.system() == 'Windows':
            self.bible_verse_display = winbibversedisplay.WinBibleVerseDisplay()
        else:
            raise NotImplementedError("OS not supported")


        # self.worker_thread = None
        self.worker_thread = threading.Thread(target=self.run)


        self.main_window = tk.Tk()

        self.settings_open = False
        self.verses_window_open = False

        self.verse_entry = None

        self.verses = ""

        self.settings = { "verses": "" }
        
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

        manage_verses_button = ttk.Button(self.settings_frame, text="Verses...", command=self.show_verses_window)
        manage_verses_button.grid(row=2, column=0, columnspan=2)
        # settings_frame.pack()
        
        # settings_frame.
        # self.main_window.pack()

        self.load_from_file()
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
        self.thread_done = False

        self.stop_btn.config(state=tk.NORMAL)
        self.start_btn.config(state=tk.DISABLED)

        if not self.started:
            # self.start()
            self.worker_thread.start()

            self.started = True
    
    def stop(self):
        self.thread_done = True
        self.stop_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.NORMAL)

    def close(self):
        print("CLOSE")
        self.closing = True
        self.stop()
        if self.started:
            self.worker_thread.join()
        
        self.save_to_file()
        self.main_window.destroy()

    def save_to_file(self):
        file_structure = { "verses": self.verses, "cycle_time": self.cycle_time_slider.get(), "per_word_time": self.settings_delay_slider.get() }
        with open("settings.json", "w") as f:
            json.dump(file_structure, f)
    
    def load_from_file(self):
        try:
            with open("settings.json", "r") as f:
                file_structure = json.load(f)
                print(file_structure)
                self.verses = file_structure["verses"]
                self.cycle_time_slider.set(int(file_structure["cycle_time"]))
                self.settings_delay_slider.set(float(file_structure["per_word_time"]))
        except IOError:
            print('config file not found')



    def run(self):
        while True:
            passages = self.verses.strip().split("\n")

            # for p in passages:
            #     if p == "":
            #         passages.remove(p)

            print(len(passages))
            print(passages)

            cycle_time = self.cycle_time_slider.get()
            per_word_time = self.settings_delay_slider.get()
            

            while not self.thread_done:

                for passage in passages:
                    print("passage " + passage)
                    # code here
                    r = get_passage_text(passage)
                    passage_text = r.json()['passages'][0]

                    #toaster.show_toast('bibverserem', r.json()['passages'][0], duration=10)
                    print(passage_text)
                    reference, verses = passage_text.split('\n\n')
                    print(verses)
                        

                    passage_text_words = verses.split(" ")

                    splits = math.ceil(len(passage_text_words)/int(config.settings["split_words"]))

                    for split in range(splits):
                        print("split: " + str(split))
                        split_passage = passage_text_words[split*config.settings["split_words"]:(split+1)*config.settings["split_words"]]
                        print(split_passage)
                        # toaster.show_toast(reference, " ".join(split_passage), duration=math.ceil(2 + 0.1*len(passage_text_words)))
                        # self.bible_verse_display.display_verse(reference, " ".join(split_passage), math.ceil(2 + 0.1*len(passage_text_words)))
                        print(per_word_time)
                        print(per_word_time*len(split_passage))
                        self.bible_verse_display.display_verse(reference, " ".join(split_passage), math.ceil(2 + float(per_word_time)*len(split_passage)))
                        


                    # sleep(int(config.settings["cycle_time"]) * 60)
                    # sleep(int(cycle_time) * 60)

                    start_d = datetime.datetime.now()
                    while not self.thread_done:
                        now_d = datetime.datetime.now()
                        if (now_d - start_d).seconds > (cycle_time*60):
                            # self.thread_done = True
                            break
                        else:
                            sleep(0.1)
                    print("end")

                    if self.thread_done:
                        break
                print("out end")
                # self.join()


            sleep(0.01)
            if self.closing:
                print('closing')

                
                break

        # self.join()
        # sys.exit(0)


    
    
# class Worker(threading.Thread):
#     def __init__(self, settings):
#         self.settings = settings
#     def launch


#r = requests.get(
#    'https://api.esv.org/v3/passage/text/?q=John+11:35-John+11:37',
#    params={'include-verse-numbers': 'false'},
#    headers={'Authorization': 'Token 4f5ab1c47d563c0dff34f2bd152619ddc7dab676'}
#    )


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
