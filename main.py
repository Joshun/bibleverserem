import requests
import config
from win10toast import ToastNotifier
from time import sleep
import math
from auth import auth_token




#r = requests.get(
#    'https://api.esv.org/v3/passage/text/?q=John+11:35-John+11:37',
#    params={'include-verse-numbers': 'false'},
#    headers={'Authorization': 'Token 4f5ab1c47d563c0dff34f2bd152619ddc7dab676'}
#    )


def get_passage_text(passage):
    encoded_passage = passage.replace(" ", "+")
    r = requests.get(
        'https://api.esv.org/v3/passage/text/?q={0}'.format(encoded_passage),
        params={'include-verse-numbers': 'false', 'include-headings': 'false', 'include-footnotes': 'false'},
        headers={'Authorization': 'Token {}'.format(auth_token)}
        )
    return r

#   print(r.json()['passages'])

toaster = ToastNotifier()

while True:
    for passage in config.passages:
        # code here
        r = get_passage_text(passage)
        passage_text = r.json()['passages'][0]

        #toaster.show_toast('bibverserem', r.json()['passages'][0], duration=10)
        print(passage_text)
        reference, verses = passage_text.split('\n\n')
        print(verses)
            

        passage_text_words = verses.split(" ")

        splits = math.ceil(len(passage_text_words)/int(config.settings["split_words"]))

        for split in range(splits):
            print("split: " + str(split))
            split_passage = passage_text_words[split*config.settings["split_words"]:(split+1)*config.settings["split_words"]]
            print(split_passage)
            toaster.show_toast(reference, " ".join(split_passage), duration=math.ceil(2 + 0.1*len(passage_text_words)))
            


        sleep(int(config.settings["cycle_time"]) * 60)


#passage = r.json()['passages'][0]

#reference, verses = passage.split('\n\n')
#toaster.show_toast(reference, verses, duration=10)

