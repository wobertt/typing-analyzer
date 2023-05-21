from word_parser import get_wordlist_from_html, get_wordlist_from_csv
from word_analyzer import UserData
from itertools import chain


# Get all data from current volunteers
def get_all_user_data():
    csv_names = ('Alternator', 'Denver', 'Fristy', 'Rynchia', 'Wobert')
    wordlists = {name: get_wordlist_from_csv(f'CSVData/{name}_data.csv') for name in csv_names}
    
    # Add Octa's HTML data separately
    wordlists['Octa'] = chain.from_iterable(
        get_wordlist_from_html(f'HTMLData/Octa {i}.txt') for i in range(1, 6)
    )

    user_data = {name: UserData(data) for name, data in wordlists.items()}

    return user_data


def main():
    user_data = get_all_user_data()

    for name, data in user_data.items():
        print(name)
        print(data.get_full_table())

    

if __name__ == '__main__':
    main()