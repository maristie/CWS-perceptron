from parser import parse, get_gram


class Percept:

    def __init__(self, wgt_vec, tag_set):
        self.wgt_vec = wgt_vec
        self.tag_set = tag_set


    def get_wgt_vec(self):
        return self.wgt_vec


    # Score with feature set
    def score(self, feat_set):
        total_score = 0

        for feat in feat_set:
            if feat in self.wgt_vec:
                total_score += self.wgt_vec[feat]

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
                    real_feat = gram + '_' + real_tag
                    pred_feat = gram + '_' + pred_tag

                    # If the feature exists in weight vector
                    if real_feat in self.wgt_vec:   # Check pred_feat is also OK
                        real_feat = gram + '_' + real_tag
                        pred_feat = gram + '_' + pred_tag

                        self.wgt_vec[real_feat] += 1    # Plus correct component
                        self.wgt_vec[pred_feat] -= 1    # Minus wrong component

                        sum_vec[real_feat] += self.train_times
                        sum_vec[pred_feat] -= self.train_times

            # No matter prediction correct or wrong, train_times increments by 1
            self.train_times += 1


    def train(self, train_file, iter_times):
        self.train_times = 1

        sum_vec = self.wgt_vec.copy()   # Store the sum of differentials

        for i in range(iter_times):
            # Train times = iter_times
            with open(train_file, 'r', encoding = 'UTF-8') as f:
                raw_line = f.readline()

                while raw_line != '':
                    temp_tuple = parse(raw_line)
                    line = temp_tuple[0]    # Line of valid characters
                    tag = temp_tuple[1]     # Tags for each character

                    self.train_by_line(line, tag, sum_vec)  # Train by this line

                    raw_line = f.readline()

        # Averaged perceptron
        for feat in self.wgt_vec:
            self.wgt_vec[feat] -= sum_vec[feat] / self.train_times


    # Return a tag sequence
    def pred_by_line(self, line):
        tag = []  # Initial tag sequence

        for i in range(len(line)):
            gram_set = get_gram(line, i)
            tag.append(self.get_best_tag(gram_set))

        return tag

    # Cut unimportant features whose abs(weight) <= threshold
    def feat_cut(self, threshold):
        new_wgt_vec = {}

        for feat in self.wgt_vec:
            feat_wgt = self.wgt_vec[feat]
            if abs(feat_wgt) > threshold:
                new_wgt_vec[feat] = feat_wgt

        self.wgt_vec = new_wgt_vec
