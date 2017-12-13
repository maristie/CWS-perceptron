# Project Report

**Note**: this is a backup [website](https://maristie.github.io/CWS-perceptron) for README.md in original [repo](https://github.com/Maristie/CWS-perceptron).

This project includes an unstructured perceptron and a structured perceptron written in Python.

## Result

The following results are under the condition of 10 iterations, averaged perceptrons and a tag set `{'B', 'M', 'E', 'S'}`.

|   Type        | Unstructured  |  Structured |
|---------------|---------------|-------------|
|   F-score     |     0.952     |    0.964    |

Unigrams and bigrams are used in structured perceptron, and one additional trigram is used in unstructured perceptron.

Most of the implementation is based on the NLP lecture slides such as Viterbi algorithm. Unique features are listed as below.

## Features

### Improvements for F-score

#### Add position information

Lecture slides has not required the position information, however without position information the accuracy of segmentation will be extremely low. After position information being added, the F-score of the unstructured perceptron increased from 0.56 to 0.90.

For example, bigram `北大_B` should be `北大_mn_B`, `m` stands for `middle` and `n` stands for `next`, in order to distinguish it from `北大_pm_B` (`p` for `previous`).


**Note**: No position information is attached to the trigram as only $$\langle x_{n-1}x_nx_{n+1}, y_n \rangle$$ is involved in unstructured perceptron.

#### Sparse vector addition and inner product

It will cost unacceptably much time if we use list in Python as vector to do the calculations. Here I have used a dictionary to map a feature to its weight, and only calculate when a feature has been recorded in the dictionary.

#### Averaged perceptron

Averaged perceptron improved F-score of unstructured version from 0.90 to 0.93. But as what I said above, if we just add the vectors, calculate the sum and divide it by the total number, it's just too slow. The pseudocode is as below.[^1]

![Naive](https://stp.lingfil.uu.se/~nivre/master/AvgPerceptron.jpg){:width="300px" height="200px"}

It's of course inefficient. I first tried to count the total iteration times and decrement it as a weight factor (just opposite to the one below). Fortunately, I found a more efficient algorithm on the Web:[^2][^3]

![Improved](https://i.loli.net/2017/12/07/5a281449b6423.jpg){:width="360px" height="315px"}

After being averaged, the unstructured version improved F-score to 0.93.

#### Multiple iterations

Simply repeat iterations and the result will be better until convergence. In the unstructured version, the F-score converges to 0.948 after 10 iterations .

Be careful that averaging operation should be done after all iterations end.

#### Improvement of segmentation strategy

My original code is:
```python
f.write(line[i])        # Write the Chinese character
if tag[i] == 'E' or tag[i] == 'S':
        f.write('  ')   # Segmentation
```

But `'B'` was not considered, and then I use the following:
```python
if tag[i] == 'B':
        f.write(' ' + line[i])
elif tag[i] == 'E':
        f.write(line[i] + ' ')
elif tag[i] == 'S':
        f.write(' ' + line[i] + ' ')
else:
        f.write(line[i])
```

The F-score rose to 0.953.

### Optimizations

#### Add begin and end mark

Like regex, we use `^` as begin mark and `$` as end mark. For example,
```
`我爱北大` -> `^我爱北大$`
```

Now we can avoid considering the first and last characters and unify the operations, which is a small trick.

#### Code refactoring

At first I didn't think of writing any class. Later I found code too messy and wrote a `Percept` class to include functions of perceptron. And some other code prettifications.

#### Consider grams that appear more than once

Some unigrams and bigrams just appear only once in the training data. Therefore to improve training efficiency, we can ignore those grams. To do this, I import `Counter` from `collections`:
```python
from collections import Counter
...
ctr = Counter(gram_list)        # Count grams stored in the list
...
if ctr[elem] > 1:       # Only grams whose frequency > 1 can be added
...
```

#### `readlines()` to `readline()`

At first the sizes of files that store the dictionary and weight vectors are as large as 100-300 MB, which is quite costly in memory. Hence I use `readline()` instead of `readlines()` to slash down its memory occupation.

#### Combine dictionary and weight vector

I set up a dictionary to map features to its index in the weight vector, and stored weight in a list. It's just a waste of space, as weights could be directly stored in the dictionary, which I call 'weight vector'.

#### Compress weight vector

The original weight vector file is quite large, however most of the stored features have a small impact on the result of segmentation. Actually, it's a 'sparse vector' and almost 90 percent of it can be cut off.

I use `1e-1` as the threshold and only features whose absolute value of its weight is larger than the threshold will be left. After compression, F-score of unstructured perceptron decreased only by 0.001 to 0.952, and the structured one remained the same as 0.964. As a contrast, file size decreased from 330 MB to 48 MB.

### Special Improvement from Unstructured to Structured

In the lecture slide, only $$y_{n-1}y_n$$ is listed as edge feature. After I implemented structured perceptron with the feature added, F-score rose to 0.962.

Then I think of combining edge feature with original node features. Here take $$x_n$$ and $$x_{n-1}x_n$$ as an example. They're node features now.

Consider a first-order Markov process. Instead of adding a single $$y_{n-1}y_n$$ to the set of features, we add the ordered pairs $$\langle x_n, y_{n-1}y_n \rangle$$ and $$\langle x_{n-1}x_n, y_{n-1}y_n \rangle$$ each of which is a combination of a node feature and an edge feature. Notice that for 4-tag set `'B', 'M', 'E', 'S'`, there would be totally 16 times features as before. Therefore it will surely cost much more memory and time to work out the result.[^4] In fact I have to remove trigrams in node features, otherwise memory limit will be exceeded and OS will subsequently crash down.

As a result, after combining node features and edge features, the final F-score rose to 0.964.

## Documentation

### Directory Tree

**Note**: Since the files that store weight vectors exceed the file size limit of GitHub, I have to compress them in `.zip` format. Hence the directory tree below may not be consistent with the present one on GitHub.

Descriptions of the files:

- `answer.txt`: the result of segmentation (that is, the segmented sentences)
- `result.txt`: the result of evaluation of `answer.txt` generated by the perl evaluation script
- Files that store the trained data
  - `wgt_vec_struct.txt`: a generated file that stores the weight vector for structured perceptron
  - `wgt_vec_unstruct.txt`: a generated file that stores the weight vector for unstructured perceptron
- `segmenter`: code, I'll introduce it in later parts.
  - `vecinit.py`
  - `ioer.py`
  - `__main__.py`
  - `parser.py`
  - `percept.py` (main)
  - `__pycache__` (automatically generated while running)
- Files that are provided initially:
  - `test.answer.txt`
  - `test.txt`
  - `train.txt`
  - `score`: provided perl script
  - `perl_arg.txt`: provided file used for F-score evaluation

**Note**:

1. `answer.txt` is the default output file of *BOTH* structured and unstructured perceptron. Thus `answer.txt` will be **OVERWRITTEN** every time you run either perceptron segmenter. If you'd like to change location and name of output file, edit the `segmenter/__main__.py` file.

2. `wgt_vec_{struct, unstruct}.txt` are just for your convenience, since it takes tens of minutes for structured perceptron to train 10 iterations. If you'd like to train weight vector from zero, edit the `segmenter/__main__.py` file.

### Recommended Operating Environment

Software: Linux kernel version 4.14 with Python 3.6.3 and Git 2.15.1

Hardware: i5-7200U + 8G Memory

Encoding: UTF-8

**Note**: Though it's alright to run any Python program on any platform, it's recommended to run on Linux distros, since the following commands are all based on Linux CLI.

### Commands

#### Run the perceptron segmenter

```sh
$ cd NLP_Project        # Get into the project directory
$ pwd                   # Check if you're in NLP_Project

# Now you should be in /[your path]/NLP_Project

$ python segmenter      # Run the perceptron segmenter
                        # Ensure python files are EXECUTABLE
                        # the result of segmentation is output as NLP_Project/answer.txt

# result.txt is the result of evaluation of answer.txt by perl script
# Ensure that the perl script is EXECUTABLE

$ perl score perl_arg.txt test.answer.txt answer.txt > result.txt
```

#### Switch between structured and unstructured version

`git` is used to help to manage versions during development, which should have been built into most Linux distros.

The default branch `master` is the unstructured version. The branch of structured version is named `struct`.

```sh
$ pwd                   # Be sure you're in NLP_Project directory now

$ cd segmenter          # Get into the segmenter directory
$ git checkout struct   # Switch to structured version

$ cd ..                 # Get back to the parent directory

# Now you can run the segmenter again with the perceptron of structured version

$ python segmenter
$ perl score perl_arg.txt test.answer.txt answer.txt > result.txt

# Switch back to unstructured version
$ cd segmenter
$ git checkout master
```

### Simple Descriptions of `.py` files

#### `parser.py`

Parse sentences in `train.txt`. The `parse` function in the file returns a tuple composed of a string without space or newline character and a list that indicates the tags for each character in the string.

Example:

Input: `'我 爱 北京大学'`

Output:
```
(str, list)
str = '我爱北京大学'
list = ['S', 'S', 'B', 'M', 'M', 'E']
```

`get_gram` function get unigrams, bigrams and an optional trigram for `i`th character in the sentence.

Example:

```
line = `我爱北京大学`
i = 1

res = get_gram(line, i)
# res will be {'爱_m', '我爱_pm', ...}
```

#### `vecinit.py`

Initialize an untrained weight vector from `train.txt` with `get_init_vec` function. It extracts features from the file and return a dictionary that maps features to weights which are set to 0.

Example:

```
get_init_vec(train_file, tag_set))
```

#### `ioer.py`

`ioer.py` stands for `inputter and outputter` which mainly processes I/O operations.

#### `percept.py`

Implement the perceptrons.

#### `__main__.py`

Import functions from the files above and run. You can use the trained weight vector directly or uncomment certain lines in `__main__.py` to train from zero.

## TODO Ideas

- Add syntax rules as constraints
- More efficient algorithm for feature compression
- Clearer commit history tree during development
- Automated feature extraction by unsupervised learning
- Random initialization

## References

[^1]: https://stp.lingfil.uu.se/~santinim/ml/Assignment2/Assignment_2_Master.htm

[^2]: https://www.slideshare.net/jchoi7s/cs571-gradient-descent

[^3]: http://www.ciml.info/dl/v0_8/ciml-v0_8-ch03.pdf

[^4]: http://www.aclweb.org/anthology/P12-1027

<script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML' async></script>
