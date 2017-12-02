from dict import get_dict
from percept import Percept
from outputter import output

train_file = 'train.txt'
test_file = 'test.txt'
output_file = 'answer.txt'

label_set = {'B', 'M', 'E', 'S'}

perc = Percept(get_dict(train_file, label_set), label_set)
perc.train(train_file, 1)   # The latter argument stands for loop times

output(perc, test_file, output_file)
