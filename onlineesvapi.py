import requests
import re
from bibverseapi import BibVerseApi
from auth import auth_token

class OnlineEsvApi(BibVerseApi):
    def get_passage(self, passage):
        encoded_passage = passage.replace(" ", "+")
        r = requests.get(
            'https://api.esv.org/v3/passage/text/?q={0}'.format(encoded_passage),
            params={'include-verse-numbers': 'false', 'include-headings': 'false', 'include-footnotes': 'false', 'indent-poetry': 'false'},
            headers={'Authorization': 'Token {}'.format(auth_token)}
            )
        # return r
        passage_text =  r.json()['passages'][0]

        reference_loc = passage_text.find("\n")
        reference = passage_text[:reference_loc]
        verses = passage_text[reference_loc:]
        verses = verses.replace("\n", " ")
        verses = verses.replace("\r", " ")

        # get rid of excess spaces
        verses = re.sub(" [ ]+", " ", verses)


        return reference, verses