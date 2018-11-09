import re
import pysword
import os
import glob

from pysword.modules import SwordModules

from bibverseapi import BibVerseApi

from exceptions import *

class SwordApi(BibVerseApi):
    def __init__(self, indices):
        # loads first available bible in current directory
        # TODO: give user choice

        self.indices = indices
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
    

    def _map_book_name(self, book_name):
        # this maps a user selected book name to the name of the module:
        #   1. get all the book names from the module in an ordered list
        #   2. look up the user selected book name in Indices to get an index for the book
        #   3. look up the corresponding module name from the ordered list of module book names
        # this is a bit of a hack, there must be a better way to do this
        # it will only work for standard canonical bibles
        books_dict = self.bible.get_structure().get_books()
        ot_books = [b.name for b in books_dict["ot"]]
        nt_books = [b.name for b in books_dict["nt"]]
        
        module_book_names = ot_books + nt_books
        if len(module_book_names) != 66:
            raise HereticalBibleTranslationException("due to indexing limitations, only canonical bibles are supported")
        

        book_index = self.indices.get_book_name_index(book_name)
        resolved_moudle_book_name = module_book_names[book_index]

        return resolved_moudle_book_name


    def get_passage(self, passage):
        parsed_reference = self._convert_passage_reference(passage)
        passage_text = ""
        if len(parsed_reference) == 3:
            book, chapter, verse = parsed_reference
            passage_text = self.bible.get(books=[self._map_book_name(book)], chapters=[int(chapter)], verses=[int(verse)])
        elif len(parsed_reference) == 2:
            book, chapter = parsed_reference
            passage_text = self.bible.get(books=[self._map_book_name(book)], chapters=[int(chapter)])            
        else:
            book = parsed_reference
            passage_text = self.bible.get(books=[self._map_book_name(book)])                      
        
        passage_text = passage_text.replace("\n", " ")
        passage_text = passage_text.replace("\r", " ")
        # get rid of excess spaces
        passage_text = re.sub(" [ ]+", " ", passage_text)

        return passage, passage_text
    
    def get_zipfile(self):
        return self.zipfile

