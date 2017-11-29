from feature import get_char_feat

def score(feature, label, weight_vec, dict):
    score = 0

    for elem in feature:
        key = elem + '_' + label
        if key in dict:
            score += weight_vec[dict[key]]

    return score

def get_best_label(feature, weight_vec, dict):
    label_set = {'M', 'E', 'S'}
    best_score = score(feature, 'B', weight_vec, dict)
    best_label = 'B'

    for label in label_set:
        label_score = score(feature, label, weight_vec, dict)
        if label_score > best_score:
            best_score = label_score
            best_label = label

    return best_label

def get_label(sent, dict, weight_vec, sum_vec,
              remain, mode = 'p', real_label = []):
    label = []
    length = len(sent)

    for i in range(length):
        gram_set = get_char_feat(sent, i)

        pred_label = get_best_label(gram_set, weight_vec, dict)

        if mode == 't':
            if pred_label != real_label[i]:
                for gram in gram_set:
                    # remain could divided by a coefficient
                    real_index = dict[gram + '_' + real_label[i]]
                    pred_index = dict[gram + '_' + pred_label]
                    weight_vec[real_index] += 1
                    weight_vec[pred_index] -= 1
                    #sum_vec[real_index] += remain
                    #sum_vec[pred_index] -= remain
            remain -= 1

        else:
            label.append(pred_label)

    return label
