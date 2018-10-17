from abc import ABC, abstractmethod

class BibleVerseDisplay(ABC):
    @abstractmethod
    def display_verse(self, reference, passage_text, duration):
        pass
    @abstractmethod
    def active(self):
        pass