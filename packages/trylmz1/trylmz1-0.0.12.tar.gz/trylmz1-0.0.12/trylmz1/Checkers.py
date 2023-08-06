
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import pickle
import os
import tensorflow as tf
from keras.layers import Dense, Embedding, LSTM, Bidirectional, GlobalMaxPool1D
from keras.models import Model, Sequential
this_dir, this_filename = os.path.split(__file__)
tokenizerpath = os.path.join(this_dir, "tokenizers", "tokenizer_deda.pickle")

weigthpath = os.path.join(this_dir, "weights", "Model_deda.h5")

def build_model(embedsize):
    model = Sequential()
    model.add(Embedding(15000, embedsize))
    model.add(Bidirectional(LSTM(64, return_sequences = True)))
    model.add(Bidirectional(LSTM(32, return_sequences = True)))
    model.add(GlobalMaxPool1D())
    model.add(Dense(1, activation="sigmoid"))
    return model

def check_de(string):
    model = build_model(128)
    with open(tokenizerpath, 'rb') as handle:
        turkish_tokenizer = pickle.load(handle)
    model.load_weights(weigthpath)
    tokens = turkish_tokenizer.texts_to_sequences(string)
    tokens_pad = pad_sequences(tokens, maxlen=7)
    pred = model.predict(string)
    print(tokens)
    print(pred)
