from dict import get_dict
from percept import Percept
from ioer import output_pred, output_dict, output_wgt_vec, \
                 input_dict, input_wgt_vec

train_file = 'train.txt'    # Train data
test_file = 'test.txt'      # Test data
output_file = 'answer.txt'  # Segmented result of test data

dict_file = 'dict.txt'      # Dictionary file
wgt_vec_file = 'wgt_vec_1_loops.txt'   # Trained weight vector data

iter_times = 1              # Iteration times

tag_set = {'B', 'M', 'E', 'S'}    # tags used for segmentation

# Get the dictionary of features and output to a file
'''
feat_dict = get_dict(train_file, tag_set)
output_dict(feat_dict, dict_file)
'''

# Read dictionary directly from existing file
feat_dict = input_dict(dict_file)

# Set up a perceptron with dictionary of features and the tag set
perc = Percept(feat_dict, tag_set)

# The latter argument stands for iteration times
perc.train(train_file, iter_times)

output_wgt_vec(perc.get_wgt_vec(), wgt_vec_file)

output_pred(perc, test_file, output_file)
