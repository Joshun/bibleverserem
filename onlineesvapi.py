import requests
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
        return r