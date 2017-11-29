def parse(sent): # sent for sentence
    length = len(sent)  # length of sentence line
    no_use_char = {' ', '\n', '\r'} # chars of no use

    word = ''
    label = []

    for i in range(length):
        if sent[i] in no_use_char:
            continue
        else:
            word += sent[i]
            if i == 0:
                if sent[i + 1] in no_use_char:
                    label.append('S');
                else:
                    label.append('B');
            elif i == length - 1:
                if sent[i - 1] in no_use_char:
                    label.append('S');
                else:
                    label.append('E');
            else:
                if sent[i - 1] in no_use_char:
                    if sent[i + 1] in no_use_char:
                        label.append('S');
                    else:
                        label.append('B');
                else:
                    if sent[i + 1] in no_use_char:
                        label.append('E');
                    else:
                        label.append('M');

    return (word, label)
