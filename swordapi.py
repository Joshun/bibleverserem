import re
import pysword
import os
import glob

from pysword.modules import SwordModules

from bibverseapi import BibVerseApi

from exceptions import *

class SwordApi(BibVerseApi):
    def __init__(self):
        # loads first available bible in current directory
        # TODO: give user choice

        self.bible = None
        zips = glob.glob("*.zip")

        for zipfile in zips:
            modules = SwordModules(zipfile)
            found_modules = modules.parse_modules()

            found_module_keys = list(found_modules.keys())

            if len(found_module_keys) == 0:
                continue
            else:
                module_key_choice = found_module_keys[0]
                self.bible = modules.get_bible_from_module(module_key_choice)
                self.zipfile = zipfile
                print("Loaded bible from " + str(zipfile))
        
        if self.bible is None:
            raise NoOfflineBibleException("No bibles found")

        self.bible = modules.get_bible_from_module(module_key_choice)
        

    def _convert_passage_reference(self, passage):

        full_ref_regex = "([0-9 ]*[a-zA-Z]+) ([0-9]+):([0-9]+)"
        book_regex = "([0-9 ]*[a-zA-Z]+)"
        chapter_regex = "([0-9 ]*[a-zA-Z]+) ([0-9]+)"

        matches = re.findall(full_ref_regex, passage)
        if len(matches) == 0:
            matches = re.findall(chapter_regex, passage)

            if len(matches) == 0:
                matches = re.findall(book_regex, passage)

                if len(matches) == 0:

                    raise Exception("Invalid ref " + str(passage))

        return matches[0]
    

    def get_passage(self, passage):
        parsed_reference = self._convert_passage_reference(passage)
        passage_text = ""
        if len(parsed_reference) == 3:
            book, chapter, verse = parsed_reference
            passage_text = self.bible.get(books=[book], chapters=[int(chapter)], verse=[int(verse)])
        elif len(parsed_reference) == 2:
            book, chapter = parsed_reference
            passage_text = self.bible.get(books=[book], chapters=[int(chapter)])            
        else:
            book = parsed_reference
            passage_text = self.bible.get(books=[book])                      
        
        return passage, passage_text
    
    def get_zipfile(self):
        return self.zipfile

