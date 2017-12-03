# Parse a segmented or unsegmented line and return its words and tags
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
