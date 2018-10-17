from win10toast import ToastNotifier

from bibversedisplay import BibleVerseDisplay

class WinBibleVerseDisplay(BibleVerseDisplay):
    def __init__(self):
        self.toaster = ToastNotifier()
    def display_verse(self, reference, passage_text, duration):
        self.toaster.show_toast(reference, passage_text, duration=duration, icon_path="python.ico", threaded=True)
    def active(self):
        return self.toaster.notification_active()

