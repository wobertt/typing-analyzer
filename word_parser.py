from bs4 import BeautifulSoup
from word_analyzer import Word
import csv


def get_word_from_div(word_div):
    letter_tags = word_div.find_all('letter')
    
    letters = ''.join(
        letter_tag.string for letter_tag in letter_tags
        if 'extra' not in letter_tag.get('class', [])
    )

    return letters


def get_wordlist_from_html(filename):
    with open(filename, 'r') as f:
        html_doc = ''.join(f.readlines())

    # Find words class in HTML
    soup = BeautifulSoup(html_doc, 'html.parser')
    word_divs_wrapper = soup.find('div', {'class': 'words'})
    all_word_divs = word_divs_wrapper.find_all('div', {'class': 'word'})

    # Add all words to wordlist
    wordlist = []
    for word_div in all_word_divs:
        wordlist.append(Word(
            letters=get_word_from_div(word_div),
            wpm=word_div.get('burst', None),
            is_error=('error' in word_div.get('class', None))
        ))
    
    return wordlist


# Read from old CSV format
def get_wordlist_from_csv(filename):
    wordlist = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            letters, speed, accuracy, amt = (
                row['Word'],
                float(row['Raw']),
                float(row['Accuracy']),
                int(row['Amt. Typed'])
            )
            for i in range(amt):
                wordlist.append(Word(
                    letters=letters,
                    wpm=speed,
                    is_error=(i > accuracy*amt)
                ))
    return wordlist
