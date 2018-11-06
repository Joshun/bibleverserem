import sys
import re

class Indices:

    def __init__(self, datafile="bibletaxonomy.csv"):
        self.indices = {}
        self.total_books = 0
        self.total_chapters = 0


        with open(datafile, "r") as f:
            for line in f:
                book, chapter, verse = line.strip().split(",")
                chapter = int(chapter)
                verse = int(verse)
                self._add_entry(book, chapter, verse)

        print('Loaded indices ({} books, {} chapters)'.format(self.total_books, self.total_chapters))

    
    def _add_entry(self, book, chapter, verse):
        # print(book, chapter, verse)
        # sys.exit(0)
        if book not in self.indices:
            self.indices[book] = {}
            self.total_books += 1

        if chapter not in self.indices[book]:
            self.indices[book][chapter] = [verse]
            self.total_chapters += 1
        else:
            self.indices[book][chapter].append(verse)

    def get_books(self):
        return list(self.indices.keys())
    def get_chapters(self, book):
        return list(self.indices[book].keys())
    def get_verses(self, book, chapter):
        return self.indices[book][chapter]
    

if __name__ == '__main__':
    indices = Indices()
    # print(indices.indices)
    # print(indices.get_chapters('Genesis'))
    print(indices.get_verses('Genesis', 1))

        



