from feature import get_feat
from process import train, predict

train_file = 'train.txt'
test_file = 'test.txt'
output_file = 'answer.txt'

dict = get_feat(train_file)
weight_vec = train(dict, train_file)
predict(dict, weight_vec, test_file, output_file)
