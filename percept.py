from dict import get_gram
from parser import parse

class Percept:

    def __init__(self, feat_dict, label_set):
        self.dict = feat_dict
        self.wgt_vec = [0] * len(self.dict)

        # Training configurations
        self.remain_label_set = label_set
        self.rand_label = self.remain_label_set.pop()


    def get_wgt_vec(self):
        return self.wgt_vec


    def set_wgt_vec(self, wgt_vec):
        self.wgt_vec = wgt_vec


    # Score with gram set and label
    def score(self, gram_set, label):
        total_score = 0

        for elem in gram_set:
            feat = elem + '_' + label
            if feat in self.dict:
                total_score += self.wgt_vec[self.dict[feat]]

        return total_score


    def get_best_label(self, gram_set):
        # Pick any label as the initial best label
        best_score = self.score(gram_set, self.rand_label)
        best_label = self.rand_label

        for label in self.remain_label_set:
            label_score = self.score(gram_set, label)
            if label_score > best_score:
                best_score = label_score
                best_label = label

        return best_label


    # Train by a line that has been labelled as seq_label
    def train_by_line(self, line, seq_label, sum_vec):
        line_len = len(line)

        for i in range(line_len):
            # Predict label for the i th char in the line
            gram_set = get_gram(line, i)
            pred_label = self.get_best_label(gram_set)

            real_label = seq_label[i]

            # If result isn't correct
            if pred_label != real_label:
                for gram in gram_set:
                    real_index = self.dict[gram + '_' + real_label]
                    pred_index = self.dict[gram + '_' + pred_label]

                    self.wgt_vec[real_index] += 1   # Plus correct component
                    self.wgt_vec[pred_index] -= 1   # Minus wrong component

                    sum_vec[real_index] += self.train_times
                    sum_vec[pred_index] -= self.train_times

                    self.train_times += 1


    def train(self, train_file, loop_times):
        self.train_times = 1

        sum_vec = [0] * len(self.dict)  # Store the sum of differentials

        with open(train_file, 'r', encoding = 'UTF-8') as f:
            lines = f.readlines()

        for i in range(loop_times):
            for raw_line in lines:
                temp_tuple = parse(raw_line)
                line = temp_tuple[0]    # Line of valid characters
                label = temp_tuple[1]   # Labels for each character

                self.train_by_line(line, label, sum_vec)

        # Averaged perceptron
        for i in range(len(self.wgt_vec)):
            self.wgt_vec[i] -= sum_vec[i] / self.train_times


    # Return a label sequence
    def pred_by_line(self, line):
        label = []  # Initial label array

        for i in range(len(line)):
            gram_set = get_gram(line, i)
            label.append(self.get_best_label(gram_set))

        return label
