from constants import ALL_WORDS, NUM_WORDS
import pandas as pd


class Word:
    def __init__(self, letters, wpm, is_error):
        self.letters = letters
        self.wpm = (None if wpm is None else int(wpm))
        self.is_error = is_error

    
    def __repr__(self):
        return f'{self.letters}: wpm={self.wpm}, typo={self.is_error}'
    

class UserData:
    word_to_idx = {word: pos for pos, word in enumerate(ALL_WORDS)}

    def __init__(self):
        self.df = pd.DataFrame(
            {'words': ALL_WORDS,
             'speeds': [[] for _ in range(NUM_WORDS)],
             'errors': [[] for _ in range(NUM_WORDS)]
            }
        )
    

    def add(self, word: str, speed: float, is_error: bool):
        idx = UserData.word_to_idx[word]
        self.df.speeds[idx].append(speed)
        self.df.errors[idx].append(is_error)



def main(): # Testing
    data = UserData()
    data.add('the', 123, False)
    

    data2 = UserData()
    data2.add('be', 12, True)
    print(data.df.head())
    print(data2.df.head())



if __name__ == '__main__':
    main()
    