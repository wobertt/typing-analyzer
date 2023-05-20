from word_parser import get_wordlist_from_file
from word_analyzer import UserData


def main():
    octa_datasets = [
        get_wordlist_from_file(f'HTMLData/Octa {i}.txt') for i in range(1, 6)
    ]
    data = UserData()
    for dataset in octa_datasets:
        data.add_words(dataset)


    data.plot_speed_histogram()
    

if __name__ == '__main__':
    main()