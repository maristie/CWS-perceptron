def segment(line, label, output_file):
    with open(output_file, 'a') as f:
        for i in range(len(line)):
            f.write(line[i])
            if i == len(line) - 1:
                f.write('\r\n')
            elif label[i] == 'E' or label[i] == 'S':
                f.write('  ')

def output(percept, test_file, output_file):
    # Clear the output file
    with open(output_file, 'w') as f: pass

    with open(test_file) as f:
        lines = f.readlines()

    for raw_line in lines:
        line = raw_line.rstrip('\r\n')  # Remove newline character by rstrip
        
        label = percept.pred_by_line(line)
        segment(line, label, output_file)
