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


def output_wgt_vec(wgt_vec, output_file):
    with open(output_file, 'w', encoding = 'UTF-8') as f:
        for feat in wgt_vec:
            pair = feat + ' ' + str(wgt_vec[feat]) + '\r\n'
            f.write(pair)


def input_wgt_vec(input_file):
    wgt_vec = {}

    with open(input_file, 'r', encoding = 'UTF-8') as f:
        line = f.readline()

        while line != '':
            div_index = line.rfind(' ')
            wgt_vec[line[0:div_index]] = float(line[div_index + 1:])

            line = f.readline()

    return wgt_vec
