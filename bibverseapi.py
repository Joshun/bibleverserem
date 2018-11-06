from abc import ABC, abstractmethod

class BibVerseApi:
    @abstractmethod
    def get_passage(self, passage):
        pass