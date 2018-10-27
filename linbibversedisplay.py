import gi
from gi.repository import GObject
from gi.repository import Notify

from bibversedisplay import BibleVerseDisplay

class LinBibleVerseDisplay(BibleVerseDisplay):
    def __init__(self):
        Notify.init("bibleverserem")
    
    def display_verse(self, reference, passage_text, duration):
        n = Notify.Notification.new(reference, passage_text, "")
        n.show()

    def active(self):
        return False