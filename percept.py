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


    # Score with feature set
    def score(self, feat_set):
        total_score = 0

        for feat in feat_set:
            if feat in self.dict:
                total_score += self.wgt_vec[self.dict[feat]]

        total_score += self.wgt_vec[self.dict[pretag + '_' + tag]]

        return total_score


    def get_best_pretag(self, gram_set, tag, pre_best_score):
<<<<<<< HEAD
        # Pick any pretag as the initial best pretag
        best_score = \
            pre_best_score[0][self.rand_tag] \
            + self.score(gram_set, self.rand_tag, tag)

        best_pretag = self.rand_tag

        print(pre_best_score)

=======
        # Set initial best_score as negative infinity
        best_score = float('-inf')
>>>>>>> Temporary fix for get_gram
        # Get best_score and best_pretag by comparing
        for pretag in self.remain_tag_set:
            pretag_score = \
                pre_best_score[0][pretag] + self.score(gram_set, pretag, tag)
            if pretag_score > best_score:
                best_score = pretag_score
                best_pretag = pretag

        # Set best score for current tag
        pre_best_score[1][tag] = best_score

        return best_pretag


    # Return best tag path
    def find_best_path(self, pre_best_tag, final_best_tag):
        length = len(pre_best_tag)
        path = [final_best_tag] * length    # Initialize tag path

        for i in range(length - 1, 0, -1):  # Find best tag path
            path[i - 1] = pre_best_tag[i][path[i]]

        return path


    # Return a predicted tag sequence using Viterbi algorithm
    # gram_set is a trick to improve space and time performance
    def pred_by_line(self, line, gram_set = []):
        length = len(line)

        # If it's an empty line, then return an empty tag sequence
        if length == 0:
            return []

        # 0 for previous best scores of different tags, and 1 for current ones
        pre_best_score = [{} for i in range(2)]
        # pre_best_tag records best tag previous to the current one
        pre_best_tag = [{} for i in range(length)]

        # Record get_gram results
        gram_set.append(get_gram(line, 0))

        # Initialization for first character
        for tag in self.tag_set:
            # Score and store
            pre_best_score[0][tag] = self.score(gram_set[0], '*', tag)

        # 0 (first) was initialized above
        for i in range(1, length):
            gram_set.append(get_gram(line, i))
            for tag in self.tag_set:
                pre_best_tag[i][tag] = \
                    self.get_best_pretag(gram_set[i], tag, pre_best_score)

            for tag in self.tag_set:
                # Current best scores will be previous ones in next loop
                pre_best_score[0][tag] = pre_best_score[1][tag]

        # Get final best tag
        total_best_score = pre_best_score[0][self.rand_tag]
        final_best_tag = self.rand_tag

        for tag in self.remain_tag_set:
            tag_best_score = pre_best_score[0][tag]
            if tag_best_score > total_best_score:
                total_best_score = tag_best_score
                final_best_tag = tag

        return self.find_best_path(pre_best_tag, final_best_tag)


    # Train by a line that has been tagged as real_tag_seq
    def train_by_line(self, line, real_tag_seq, sum_vec):
        length = len(line)
        gram_set = []

        # Get predicted tag sequence
        pred_best_seq = self.pred_by_line(line, gram_set)

        for i in range(length):
            real_tag = real_tag_seq[i]
            pred_tag = pred_best_seq[i]
            # If prediction result isn't correct
            if pred_tag != real_tag:
                # Adjustment for common node features
                for gram in gram_set[i]:
                    real_index = self.dict[gram + '_' + real_tag]
                    pred_index = self.dict[gram + '_' + pred_tag]

                    self.wgt_vec[real_index] += 1   # Plus correct component
                    self.wgt_vec[pred_index] -= 1   # Minus wrong component

                    sum_vec[real_index] += self.train_times
                    sum_vec[pred_index] -= self.train_times

                # Adjustment for edge features
                if i == 0:
                    real_edge = '*_' + real_tag
                    pred_edge = '*_' + pred_tag
                else:
                    real_edge = real_tag_seq[i - 1] + '_' + real_tag
                    pred_edge = pred_best_seq[i - 1] + '_' + pred_tag

                real_index = self.dict[real_edge]
                pred_index = self.dict[pred_edge]

                self.wgt_vec[real_index] += 1
                self.wgt_vec[pred_index] -= 1

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
