from vecinit import get_init_vec
from percept import Percept
from ioer import output_pred, output_wgt_vec, input_wgt_vec

train_file = 'train.txt'    # Train data
test_file = 'test.txt'      # Test data
output_file = 'answer.txt'  # Segmented result of test data

wgt_vec_file = 'wgt_vec_struct.txt'    # Trained weight vector data

iter_times = 10             # Iteration times

tag_set = {'B', 'M', 'E', 'S'}    # tags used for segmentation

# Initialize weight vector from train file
# wgt_vec = get_init_vec(train_file, tag_set)

# Read weight vector from the existing file that has been trained
wgt_vec = input_wgt_vec(wgt_vec_file)

# Initialize a perceptron with weight vector and the tag set
perc = Percept(wgt_vec, tag_set)

# Train weight vector
# perc.train(train_file, iter_times)

# Feature cutting, all features whose weight is less than 1e-1 is deleted
# perc.feat_cut(1e-1)

# Print weight vector
# output_wgt_vec(perc.get_wgt_vec(), wgt_vec_file)

# Predict segmentation using the perceptron and output result
output_pred(perc, test_file, output_file)
