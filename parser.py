# Parse a segmented or unsegmented line and return its words and labels
def parse(line):
    length = len(line)  # length of sentence line
    no_use_char = {' ', '\n', '\r'} # chars of no use

    word = ''
    label = []

    for i in range(length):
        if line[i] in no_use_char:
            continue
        else:
            word += line[i]
            if i == 0:
                if line[i + 1] in no_use_char:
                    label.append('S');
                else:
                    label.append('B');
            elif i == length - 1:
                if line[i - 1] in no_use_char:
                    label.append('S');
                else:
                    label.append('E');
            else:
                if line[i - 1] in no_use_char:
                    if line[i + 1] in no_use_char:
                        label.append('S');
                    else:
                        label.append('B');
                else:
                    if line[i + 1] in no_use_char:
                        label.append('E');
                    else:
                        label.append('M');

    return (word, label)
