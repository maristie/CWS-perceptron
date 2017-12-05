from dict import get_dict
from percept import Percept
from ioer import output_pred, output_dict, output_wgt_vec, \
                 input_dict, input_wgt_vec

train_file = 'train.txt'    # Train data
test_file = 'test.txt'      # Test data
output_file = 'answer.txt'  # Segmented result of test data

dict_file = 'dict_dev.txt'  # Dictionary file
wgt_vec_file = 'wgt_vec_dev.txt'    # Trained weight vector data

iter_times = 10             # Iteration times

tag_set = {'B', 'M', 'E', 'S'}    # tags used for segmentation

# Get the dictionary of features
# feat_dict = get_dict(train_file, tag_set)

# Read the dictionary directly from existing file
feat_dict = input_dict(dict_file)

# Initialize a perceptron with dictionary of features and the tag set
perc = Percept(feat_dict, tag_set)

# Get weight vector by training
# perc.train(train_file, iter_times)

# Read weight vector from the existing file that has been trained
wgt_vec = input_wgt_vec(wgt_vec_file)
# Set weight vector as the above one
perc.set_wgt_vec(wgt_vec)

# Feature cutting
# perc.feat_cut(1e-1)

# Output dictionary and weight vector
# output_dict(perc.get_dict(), dict_file)
# output_wgt_vec(perc.get_wgt_vec(), wgt_vec_file)

# Predict segmentation using the perceptron and output result
output_pred(perc, test_file, output_file)
