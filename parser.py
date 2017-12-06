# Parse a segmented line and return its words and tags
def parse(line):
    length = len(line)  # length of sentence line
    no_use_char = {' ', '\n', '\r'} # chars of no use

    word = ''
    tag = []

    for i in range(length):
        if line[i] in no_use_char:
            continue
        else:
            word += line[i]
            if i == 0:
                if line[i + 1] in no_use_char:
                    tag.append('S');
                else:
                    tag.append('B');
            elif i == length - 1:
                if line[i - 1] in no_use_char:
                    tag.append('S');
                else:
                    tag.append('E');
            else:
                if line[i - 1] in no_use_char:
                    if line[i + 1] in no_use_char:
                        tag.append('S');
                    else:
                        tag.append('B');
                else:
                    if line[i + 1] in no_use_char:
                        tag.append('E');
                    else:
                        tag.append('M');

    return (word, tag)

# Get grams for character line[index]
def get_gram(line, index):
    i = index + 1   # As we've added a header ^

    # ^ for begin, $ for end
    temp_line = '^' + line + '$'

    # Get unigrams and bigrams with position information
    # p for previous, m for middle, n for next
    gram_set = {temp_line[i] + '_m', temp_line[i + 1] + '_n',
                temp_line[i - 1] + '_p', temp_line[i:i + 2] + '_mn', temp_line[i - 1:i + 1] + '_pm',
                temp_line[i - 1] + temp_line[i + 1] + '_pn'}

    return gram_set
