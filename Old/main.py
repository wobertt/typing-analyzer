from important_constants import ALL_WORDS

"""
1. turn the raw html into something easier to process

GOAL:
- each line should be (word, burst speed, was it correctly typed)
- e.g., ("consider", 200, True)

PART 1:
- strip to only important parts

PART 2:
- group by individual words.
- let the html for each word be an element of a list

PART 3:
- handle each kind of word.
    from github:   dead, correct, corrected, extraCorrected, incorrect, incorrect.extra
    from txt file: correct, corrected, incorrect, incorrect extra, incorrect extraCorrected

- get the three values (word, burst speed, was it correctly typed)

takeaways:
- ignore incorrect extra, not incorrect extraCorrected
- must do something about missing letters

2. group the words into something a spreadsheet can use

GOAL:
- columns: Word, WPM, Raw, Accuracy, Amount Typed
- e.g., consider, 150, 200, 0.75, 4

- WARNING: what to do about missing letters?
- try: people, 0, 0, 0, 0

3. find a clean way to export to google sheets
- or just output with nice formatting to a text file, maybe learn pandas!


"""


"""
process_file()
    1. strip_text()
    2. convert_to_list()
        find_parameter_value()
        find_word_stats()
"""


def find_parameter_value(text, parameter, start_pos):
    """
    Example:
    parameter = "letter class"
    text = 'letter class="incorrect "'

    After running code:
    start_index is at 'i' in incorrect
    end_index is at the last character
    function returns "incorrect "
    """

    temp_index = text.find(parameter, start_pos)
    if temp_index == -1:
        return -1

    start_index = temp_index + len(parameter) + 2   # +2 to adjust for the =", see example
    end_index = text.index("\"", start_index)

    return text[start_index:end_index]


def merge_and_strip_files(files):
    converted_text = ""
    for file in files:
        with open(file) as f:
            raw_text = f.read()
        converted_text += strip_text(raw_text)     # find text only in <div class="words">

    return converted_text


def process_files(files):
    converted_text = merge_and_strip_files(files)

    converted_list = convert_to_list(converted_text)

    desired_data = compile_data(converted_list)

    with open(NEW_FILENAME, "a") as f:
        f.write(str(desired_data))

    return desired_data


def strip_text(text):  # returns the text inside <div class="words">
    temp_index = text.index("<div class=\"words\">")  # finds <div class="words">
    start_index = text.index("<div class", temp_index + 1)  # deletes above, we don't need it
    end_index = text.index("</div></div>", start_index) + 6  # delete the second </div> (from <div class="words">)

    new_text = text[start_index:end_index]

    return new_text


def find_word_stats(text_line):
    class_value = find_parameter_value(text_line, "class", 0)

    if class_value == -1 or "heatmap" not in class_value:  # skips words that weren't typed (they don't have heatmaps)
        return -1

    is_correct = "error heatmap" not in class_value     # all incorrectly typed words have an "error heatmap" class

    burst_value = int(find_parameter_value(text_line, "burst", 0))

    word = ""
    current_pos = 0
    while True:
        letter_class = find_parameter_value(text_line, "letter class", current_pos)  # if -1, the letter wasn't typed

        current_pos = text_line.find("</letter>", current_pos+1)

        if current_pos == -1:
            break

        if letter_class != "incorrect extra":
            word += text_line[current_pos-1]    # the actual letter is found just before </letter>

    return word, burst_value, is_correct


def convert_to_list(text):
    raw_list = text.split("<div ")  # each word starts with <div class=
    processed_list = []

    for text_line in raw_list:
        packaged_values = find_word_stats(text_line)

        if packaged_values != -1:
            processed_list.append(find_word_stats(text_line))

    processed_list.sort()
    return processed_list


def compile_data(converted_list):
    word_list = []
    reciprocal_raw_list = []     # find sum of 1/raw for all words (use harmonic mean)
    amount_correct_list = []
    amount_typed_list = []

    for packaged_info in converted_list:
        word, burst, is_correct = packaged_info
        if word not in word_list:
            word_list.append(word)
            reciprocal_raw_list.append(1/burst)

            amount_correct_list.append(int(is_correct))
            amount_typed_list.append(1)
        else:
            word_index = word_list.index(word)
            reciprocal_raw_list[word_index] += 1/burst
            amount_correct_list[word_index] += int(is_correct)
            amount_typed_list[word_index] += 1

    # Desired data: Word, WPM, Raw, Accuracy, Amount Typed, Time
    desired_data = []
    for i in range(len(word_list)):
        word, reciprocal_raw, amount_correct, amount_typed = (
            word_list[i],
            reciprocal_raw_list[i],
            amount_correct_list[i],
            amount_typed_list[i]
        )

        raw_wpm = amount_typed / reciprocal_raw    # harmonic mean

        accuracy = amount_correct / amount_typed
        wpm = raw_wpm * accuracy

        data_row = (word, wpm, raw_wpm, accuracy, amount_typed)

        rounded_data_row = []
        for datapoint in data_row:
            try:
                rounded_data_row.append(round(datapoint, 2))
            except TypeError:
                rounded_data_row.append(datapoint)

        desired_data.append(rounded_data_row)

    return desired_data


def print_missing_words(word_list):
    for word in ALL_WORDS:
        if word not in word_list:
            print(word)


def print_output(desired_data):
    print("Prints: word (includes words not typed), wpm, raw, accuracy, amount typed.\n"
          "Press enter to get the next column of data.")

    for i in range(len(desired_data[0])):
        input()

        for datapoint in [data_column[i] for data_column in desired_data]:
            print(datapoint)

        if i == 0 and IS_ENGLISH:
            print_missing_words([data_column[0] for data_column in desired_data])


def main():
    print_output(process_files(FILENAMES))


FILENAMES = ("Octa 1.txt", "Octa 2.txt", "Octa 3.txt", "Octa 4.txt", "Octa 5.txt")
NEW_FILENAME = "octa compressed.txt"
IS_ENGLISH = True

if __name__ == "__main__":
    main()
