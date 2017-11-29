from parse import parse

def get_char_feat(sent, index):
    i = index
    length = len(sent)
    feat_set = set()

    feat_set.add(sent[index] + '_m')
    if i == 0 and i + 1 < length:
        feat_set |= {sent[i + 1] + '_n', sent[i:i + 2] + '_mn'}
    elif i == length - 1:
        feat_set |= {sent[i - 1] + '_p', sent[i - 1:i + 1] + '_pm'}
    else:
        feat_set |= {sent[i + 1] + '_n', sent[i:i + 2] + '_mn',
                     sent[i - 1] + '_p', sent[i - 1:i + 1] + '_pm',
                     sent[i - 1] + sent[i + 1] + '_pn',
                     sent[i - 1:i + 2] + '_pmn'}
    return feat_set


def add_feat(sent, dict):
    length = len(sent)
    label_set = {'B', 'M', 'E', 'S'}
    char_feat_set = set()

    for i in range(length):
        char_feat_set |= get_char_feat(sent, i)

    for unit in char_feat_set:
        for label in label_set:
            feat = unit + '_' + label
            if feat not in dict:
                dict_len = len(dict)
                dict[feat] = dict_len

def get_feat(train_file):
    dict = {}

    with open(train_file) as f:
        newline = f.readline()
        while newline != '':
            add_feat(parse(newline)[0], dict)
            newline = f.readline()

    return dict
