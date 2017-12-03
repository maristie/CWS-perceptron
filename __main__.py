from dict import get_dict
from percept import Percept
from ioer import output_pred, output_dict, output_wgt_vec, \
                 input_dict, input_wgt_vec

train_file = 'train.txt'
test_file = 'test.txt'
output_file = 'answer.txt'

dict_file = 'dict.txt'
wgt_vec_file = 'wgt_vec.txt'

label_set = {'B', 'M', 'E', 'S'}

# Get the dictionary of features
'''
feat_dict = get_dict(train_file, label_set)
output_dict(feat_dict, dict_file)
'''

# Read dictionary from existing file
feat_dict = input_dict(dict_file)

'''
# Set up a perceptron with dictionary of features and the label set
perc = Percept(feat_dict, label_set)

for i in range(5)
    perc.train(train_file, 1)   # The latter argument stands for loop times

perc.get_wgt_vec()

output_pred(perc, test_file, output_file)
'''
