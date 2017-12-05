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

# Add feature from a sentence to the dictionary
def add_feat(line, dict, tag_set):
    line_gram_set = set()

    for i in range(len(line)):
        line_gram_set |= get_gram(line, i)

    for elem in line_gram_set:
        for tag in tag_set:
            feat = elem + '_' + tag
            if feat not in dict:
                dict_len = len(dict)
                dict[feat] = dict_len

# Get dictionary
def get_dict(train_file, tag_set):
    dict = {}

    with open(train_file, 'r', encoding = 'UTF-8') as f:
        line = f.readline() # Initial line

        while line != '':
            add_feat(parse(line)[0], dict, tag_set)
            line = f.readline()

    return dict
