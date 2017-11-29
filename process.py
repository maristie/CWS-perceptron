from label import get_label
from parse import parse
from random import randint

def segment(sent, label, output_file):
    with open(output_file, 'a') as f:
        length = len(sent)
        for i in range(length):
            f.write(sent[i])
            if i == length - 1:
                f.write('\r\n')
            elif label[i] == 'E' or label[i] == 'S':
                f.write('  ')

def char_count(train_file):
    length = 0
    with open(train_file) as f:
        newline = f.readline()
        while newline != '':
            length += len(parse(newline)[0])
            newline = f.readline()
    return length

def process_txt(dict, weight_vec, file_name, mode = 'p', output_file = ''):
    total_char = remain_char = char_count(file_name)
    dict_len = len(dict)

    init_vec = weight_vec.copy()
    sum_vec = [0] * dict_len

    if mode != 't':
        with open(output_file, 'w') as f: pass

    with open(file_name) as f:
        newline = f.readline()
        while newline != '':
            temp = parse(newline)
            sent = temp[0]
            sent_len = len(sent)

            label = get_label(sent, dict, weight_vec, sum_vec,
                              remain_char, mode, temp[1])
            remain_char -= sent_len

            if mode != 't':
                segment(sent, label, output_file)

            newline = f.readline()
'''
    if mode == 't':
        for elem in label_set:
            for i in range(dict_len):
                offset = sum_vec[i] / (total_char + 1)
                weight_vec[i] = offset + init_vec[i]
'''

def train(dict, train_file):
    length = len(dict)
    weight_vec = [0] * length
    process_txt(dict, weight_vec, train_file, 't')
    return weight_vec

def predict(dict, weight_vec, test_file, output_file):
    process_txt(dict, weight_vec, test_file, 'p', output_file)
