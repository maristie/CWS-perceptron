from collections import Counter # For counting features

from parser import parse

def get_gram(line, index):
    length = len(line)
    i = index + 1   # As we've added a header ^

    # ^ for begin, $ for end
    temp_line = '^' + line + '$'

    # Get unigrams and bigrams with position information
    # p for previous, m for middle, n for next
    gram_set = {temp_line[i] + '_m', temp_line[i + 1] + '_n',
                temp_line[i - 1] + '_p', temp_line[i:i + 2] + '_mn', temp_line[i - 1:i + 1] + '_pm',
                temp_line[i - 1] + temp_line[i + 1] + '_pn',
                temp_line[i - 1:i + 2]}

    return gram_set

def get_dict(train_file, tag_set):
    dict = {}
    gram_list = []

    with open(train_file, 'r', encoding = 'UTF-8') as f:
        line = f.readline() # Initial line

        while line != '':
            # Get features in a list
            temp = parse(line)[0]
            for i in range(len(temp)):
                gram_list.extend(get_gram(temp, i))

            line = f.readline()

    ctr = Counter(gram_list)
    length = 0

    # Add features to dictionary
    for elem in ctr:
        if ctr[elem] > 1:
            for tag in tag_set:
                dict[elem + '_' + tag] = length
                length += 1

    return dict
