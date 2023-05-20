from constants import ALL_WORDS


class Word:
    def __init__(self, letters, wpm, is_error):
        self.letters = letters
        self.wpm = (None if wpm is None else int(wpm))
        self.is_error = is_error

    
    def __repr__(self):
        return f'{self.letters}: wpm={self.wpm}, typo={self.is_error}'
    


class WordList:
    def __init__(self):
        self.words = []
    

    def add(self, word):
        self.words.append(word)
    

    def get_average_wpm(self):
        num_words, wpm_sum = 0, 0
        for word in self.words:
            if word.wpm is None:
                continue
            num_words += 1
            wpm_sum += word.wpm
        
        return wpm_sum / num_words
    

    