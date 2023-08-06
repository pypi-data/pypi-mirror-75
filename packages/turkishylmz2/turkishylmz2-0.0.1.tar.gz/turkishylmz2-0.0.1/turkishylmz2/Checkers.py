
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import pickle

def check_de(string):
    with open('turkishylmz1/tokenizer_deda.pickle', 'rb') as handle:
        turkish_tokenizer = pickle.load(handle)
    model = load_model('turkishylmz1/Model_deda.h5')
    tokens = turkish_tokenizer.texts_to_sequences(string)
    tokens_pad = pad_sequences(tokens, maxlen=7)
    print(tokens)

