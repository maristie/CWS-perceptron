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
        raw_line = f.readline()

        while raw_line != '':
            line = raw_line.rstrip('\r\n')  # Remove newline character by rstrip

            # Predict tags and segment sentence
            tag = percept.pred_by_line(line)
            segment(line, tag, output_file)

            raw_line = f.readline()


def output_dict(feat_dict, output_file):
    with open(output_file, 'w', encoding = 'UTF-8') as f:
        for key in feat_dict:
            pair = key + ' ' + str(feat_dict[key]) + '\r\n'
            f.write(pair)


def input_dict(input_file):
    dict = {}

    with open(input_file, 'r', encoding = 'UTF-8') as f:
        line = f.readline()

        while line != '':
            div_index = line.rfind(' ')
            dict[line[0:div_index]] = int(line[div_index + 1:])

            line = f.readline()

    return dict


def output_wgt_vec(vec, output_file):
    with open(output_file, 'w', encoding = 'UTF-8') as f:
        for elem in vec:
            f.write(str(elem) + '\r\n')


def input_wgt_vec(input_file):
    wgt_vec = []    # Initial weight vector

    with open(input_file, 'r', encoding = 'UTF-8') as f:
        line = f.readline()

        while line != '':
            wgt_vec.append(float(line))

            line = f.readline()

    return wgt_vec
