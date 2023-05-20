from constants import ALL_WORDS, NUM_WORDS
import pandas as pd
import matplotlib.pyplot as plt


class Word:
    def __init__(self, letters, wpm, is_error):
        self.letters = letters
        self.wpm = (None if wpm is None else int(wpm))
        self.is_error = is_error

    
    def __repr__(self):
        return f'{self.letters}: wpm={self.wpm}, typo={self.is_error}'
    

class UserData:
    word_to_idx = {word: pos for pos, word in enumerate(ALL_WORDS)}

    def __init__(self, wordlist=None):
        self.df = pd.DataFrame(
            {'words': ALL_WORDS,
             'speeds': [[] for _ in range(NUM_WORDS)],
             'errors': [[] for _ in range(NUM_WORDS)]
            }
        )
        
        if wordlist is not None:
            self.add_words(wordlist)
    

    def add_word(self, word: Word):
        idx = UserData.word_to_idx[word.letters]
        self.df.speeds[idx].append(word.wpm)
        self.df.errors[idx].append(word.is_error)


    def add_words(self, wordlist: list[Word]):
        for word in wordlist:
            self.add_word(word)
    

