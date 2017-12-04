# Input / Output functions

def segment(line, tag, output_file):
    with open(output_file, 'a', encoding = 'UTF-8') as f:
        for i in range(len(line)):
            if tag[i] == 'B':
                f.write(' ' + line[i])
            elif tag[i] == 'E':
                f.write(line[i] + ' ')
            elif tag[i] == 'S':
                f.write(' ' + line[i] + ' ')
            else:
                f.write(line[i])

        f.write('\r\n') # Newline


def output_pred(percept, test_file, output_file):
    # Clear the output file
    with open(output_file, 'w', encoding = 'UTF-8') as f: pass

    with open(test_file, 'r', encoding = 'UTF-8') as f:
        lines = f.readlines()

    for raw_line in lines:
        line = raw_line.rstrip('\r\n')  # Remove newline character by rstrip

        tag = percept.pred_by_line(line)
        segment(line, tag, output_file)


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

    length = len(lines)
    wgt_vec = [0] * length

    for i in range(length):
        wgt_vec[i] = float(lines[i])

    return wgt_vec
