import threading
import platform
import math
import datetime
import requests
import sys
from time import sleep

import config
from auth import auth_token
from onlineesvapi import OnlineEsvApi
from swordapi import SwordApi

import tkinter.messagebox

from exceptions import *

class BibVerseWorker(threading.Thread):
    def __init__(self):
        # super().__init__()
        threading.Thread.__init__(self)

        if platform.system() == 'Windows':
            import winbibversedisplay
            self.bible_verse_display = winbibversedisplay.WinBibleVerseDisplay()
        elif platform.system() == 'Linux':
            import linbibversedisplay
            self.bible_verse_display = linbibversedisplay.LinBibleVerseDisplay()
        else:
            raise NotImplementedError("OS not supported")
        
        self.verses = ""
        self.per_word_time = 0
        self.cycle_time = 0

        self.thread_done = False
        self.closing = False

        self.errors_queue = None

        # self.api = OnlineEsvApi()
        self.api = None
        self._autoselect_api()
    
    def _autoselect_api(self):
        use_notifications = config.settings["bible_verse_notifications"]
        try:
            self.api = SwordApi()
            zipfile = self.api.get_zipfile()
            if use_notifications:
                self.bible_verse_display.display_verse("Offline bible found", zipfile, 5)
            
        except NoOfflineBibleException:
            self.api = OnlineEsvApi()
            if use_notifications:
                self.bible_verse_display.display_verse("No offline bibles found", "Using online ESV bible", 5)
    
    def set_errors_queue(self, queue):
        self.errors_queue = queue
    
    def write_error(self, err):
        if self.errors_queue is not None:
            self.errors_queue.put(("error", err))
    
    def write_info(self, info):
        if self.errors_queue is not None:
            self.errors_queue.put(("info", info))

    def set_options(self, *, cycle_time, per_word_time, verses):
        self.cycle_time = cycle_time
        self.per_word_time = per_word_time
        self.verses = verses
    
    def set_done(self):
        self.thread_done = True

    def set_closing(self):
        self.closing = True
    
    def reset(self):
        self.thread_done = False
    
    def run(self):
        while True:
            try:
                self.run_worker()
                if self.closing:
                    break
            except Exception as e:
                self.write_error(e)
            sleep(0.01)
                
    def run_worker(self):
        passages = self.verses.strip().split("\n")

        # for p in passages:
        #     if p == "":
        #         passages.remove(p)

        print(len(passages))
        print(passages)

        cycle_time = self.cycle_time
        per_word_time = self.per_word_time
        

        while not self.thread_done:
            print(passages)
            for passage in passages:
                if passage == "":
                    continue


                # code here
                # r = self.api.get_passage(passage)
                # passage_text = r.json()['passages'][0]
                # passage_text = self.api.get_passage(passage)

                #toaster.show_toast('bibverserem', r.json()['passages'][0], duration=10)
                # print(passage_text)
                # reference_loc = passage_text.find("\n")
                # reference = passage_text[:reference_loc]
                # verses = passage_text[reference_loc:]
                # verses = verses.replace("\n", " ")

                reference, verses = self.api.get_passage(passage)

                # reference, verses = passage_text.split('\n\n')
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

                    progress_text = " ({}/{})".format(split+1,splits)

                    self.bible_verse_display.display_verse(reference + progress_text, " ".join(split_passage), math.ceil(2 + float(per_word_time)*len(split_passage)))
                    
                    while self.bible_verse_display.active() and not self.thread_done:
                        sleep(0.01)
                    if self.thread_done:
                        break


                start_d = datetime.datetime.now()
                while not self.thread_done:
                    now_d = datetime.datetime.now()
                    if (now_d - start_d).seconds > (cycle_time*60):
                        # self.thread_done = True
                        break
                    else:
                        sleep(0.01)
                print("end")

                if self.thread_done:
                    break
            print("out end")
            # self.join()


    #     sleep(0.01)
    #     if self.closing:
    #         print('closing')
    #         break
    #         # sys.exit(0)
    # print("END")



