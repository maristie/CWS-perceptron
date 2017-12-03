# Input / Output functions

def segment(line, label, output_file):
    with open(output_file, 'a', encoding = 'UTF-8') as f:
        for i in range(len(line)):
            f.write(line[i])
            if i == len(line) - 1:
                f.write('\r\n')
            elif label[i] == 'E' or label[i] == 'S':
                f.write('  ')


def output_pred(percept, test_file, output_file):
    # Clear the output file
    with open(output_file, 'w', encoding = 'UTF-8') as f: pass

    with open(test_file, 'r', encoding = 'UTF-8') as f:
        lines = f.readlines()

    for raw_line in lines:
        line = raw_line.rstrip('\r\n')  # Remove newline character by rstrip

        label = percept.pred_by_line(line)
        segment(line, label, output_file)


def output_dict(feat_dict, output_file):
    with open(output_file, 'w', encoding = 'UTF-8') as f:
        for key in feat_dict:
            pair = key + ' ' + str(feat_dict[key]) + '\r\n'
            f.write(pair)


def input_dict(input_file):
    dict = {}

    with open(input_file, 'r', encoding = 'UTF-8') as f:
        lines = f.readlines()

    for pair in lines:
        div_index = pair.rfind(' ')
        dict[pair[0:div_index]] = int(pair[div_index + 1:])

    return dict


def output_wgt_vec(vec, output_file):
    with open(output_file, 'w', encoding = 'UTF-8') as f:
        for elem in vec:
            f.write(str(elem) + '\r\n')


def input_wgt_vec(input_file):
    with open(input_file, 'r', encoding = 'UTF-8') as f:
        lines = f.readlines()

    length = len(lines) - 1
    wgt_vec = [0] * length

    for num in lines:
        wgt_vec[i] = float(num)

    return wgt_vec
