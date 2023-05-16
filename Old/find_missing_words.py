import main


def find_missing_words():
    print("Running find_missing_words.py")

    word_list = []
    while True:
        word = input()

        if word != '-1':
            word_list.append(word)
        else:
            break

    main.print_missing_words(word_list)


if __name__ == "__main__":
    find_missing_words()