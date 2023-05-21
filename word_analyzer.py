from constants import ALL_WORDS, NUM_WORDS, MAX_SPEED
import pandas as pd
import numpy as np
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
        if word.wpm is None:
            return
        idx = UserData.word_to_idx[word.letters]
        self.df.speeds[idx].append(word.wpm)
        self.df.errors[idx].append(word.is_error)


    def add_words(self, wordlist: list[Word]):
        for word in wordlist:
            self.add_word(word)
    

    def plot_speed_histogram(self, n_bins, name="Unnamed"):
        # Get all speed data
        speeds = []
        for speed_data in self.df.speeds:
            speeds.extend(speed_data)
        series = pd.Series(speeds)
        # Remove outliers
        series_adjusted = series[series.between(0, MAX_SPEED)]

        # Plot
        _, ax = plt.subplots()
        _, bins, _ = ax.hist(series_adjusted, bins=n_bins, density=True)
        
        # Add Gaussian approximation
        mu = series_adjusted.mean()
        sigma = series_adjusted.std()
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) 
             * np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
        ax.plot(bins, y, '--')
        
        ax.set_xlabel('WPM')
        ax.set_ylabel('Probability Density')
        ax.set_title(f'{name}\'s Speed Histogram: $\mu={mu:.1f}$, $\sigma={sigma:.1f}$')
        plt.show()


    def get_full_table(self, sort_ascending=True):
        avg_speed = np.array(list(map(
            lambda x: sum(x)/len(x) if x else None,
            self.df.speeds)))
        accuracy = np.array(list(map(
            lambda x: x.count(False)/len(x) if x else None,
            self.df.errors
        )))
        amt_typed = np.array(list(map(
            lambda x: len(x),
            self.df.errors
        )))
        
        table = pd.DataFrame({
            'word': ALL_WORDS,
            'speed': avg_speed,
            'accuracy': accuracy,
            'amt_typed': amt_typed
        })
        # Can't divide None by a scalar, so we add after dropping
        table.dropna(inplace=True)
        table.insert(2, 'relative', table['speed']/table['speed'].mean())

        return table.sort_values(by='speed', 
                          ascending=sort_ascending,
                          ignore_index=True)
