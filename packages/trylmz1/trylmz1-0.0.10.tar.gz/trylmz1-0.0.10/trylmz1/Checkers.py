
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import pickle
import os
import tensorflow as tf
this_dir, this_filename = os.path.split(__file__)
tokenizerpath = os.path.join(this_dir, "tokenizers", "tokenizer_deda.pickle")

weigthpath = os.path.join(this_dir, "weights", "Model_deda.h5")


def check_de(string):
    with open(tokenizerpath, 'rb') as handle:
        turkish_tokenizer = pickle.load(handle)
    model = load_model(weigthpath, custom_objects=tf.keras.metrics.AUC(name='auc'))
    tokens = turkish_tokenizer.texts_to_sequences(string)
    tokens_pad = pad_sequences(tokens, maxlen=7)
    print(tokens)

