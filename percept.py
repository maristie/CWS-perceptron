from dict import get_gram
from parser import parse

class Percept:

    def __init__(self, feat_dict, tag_set):
        self.dict = feat_dict
        self.wgt_vec = [0] * len(self.dict)
        self.tag_set = tag_set


    def get_wgt_vec(self):  # Get the copy of weight vector
        return self.wgt_vec.copy()


    def set_wgt_vec(self, wgt_vec): # Set weight vector as the copy of wgt_vec
        self.wgt_vec = wgt_vec.copy()


    # Score with gram set and tag
    def score(self, feat_set):
        total_score = 0

        for feat in feat_set:
            if feat in self.dict:
                total_score += self.wgt_vec[self.dict[feat]]

        return total_score


    def get_best_tag(self, gram_set):
        # Set initial best_score as negative infinity
        best_score = float('-inf')

        for tag in self.tag_set:
            feat_set = set()    # Feature set
            for elem in gram_set:
                feat_set.add(elem + '_' + tag)

            tag_score = self.score(feat_set)    # Score by features

            if tag_score > best_score:
                best_score = tag_score
                best_tag = tag

        return best_tag


    # Train by a line that has been tagged as seq_tag
    def train_by_line(self, line, seq_tag, sum_vec):
        line_len = len(line)

        for i in range(line_len):
            # Predict tag for the i th char in the line
            gram_set = get_gram(line, i)
            pred_tag = self.get_best_tag(gram_set)

            real_tag = seq_tag[i]

            # If prediction result isn't correct
            if pred_tag != real_tag:
                for gram in gram_set:
                    real_index = self.dict[gram + '_' + real_tag]
                    pred_index = self.dict[gram + '_' + pred_tag]

                    self.wgt_vec[real_index] += 1   # Plus correct component
                    self.wgt_vec[pred_index] -= 1   # Minus wrong component

                    sum_vec[real_index] += self.train_times
                    sum_vec[pred_index] -= self.train_times

            # No matter prediction correct or wrong, train_times increments by 1
            self.train_times += 1


    def train(self, train_file, iter_times):
        self.train_times = 1

        sum_vec = [0] * len(self.dict)  # Store the sum of differentials

        with open(train_file, 'r', encoding = 'UTF-8') as f:
            lines = f.readlines()

        for i in range(iter_times):
            for raw_line in lines:
                temp_tuple = parse(raw_line)
                line = temp_tuple[0]    # Line of valid characters
                tag = temp_tuple[1]     # Tags for each character

                self.train_by_line(line, tag, sum_vec)

        # Averaged perceptron
        for i in range(len(self.wgt_vec)):
            self.wgt_vec[i] -= sum_vec[i] / self.train_times


    # Return a tag sequence
    def pred_by_line(self, line):
        tag = []  # Initial tag sequence

        for i in range(len(line)):
            gram_set = get_gram(line, i)
            tag.append(self.get_best_tag(gram_set))

        return tag
