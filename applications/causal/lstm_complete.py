import tensorflow as tf

from nalp.corpus import TextCorpus
from nalp.encoders import IntegerEncoder
from nalp.models.generators import LSTMGenerator

# When generating artificial text, make sure
# to use the same data, classes and parameters
# as the pre-trained network

# Creating a character TextCorpus from file
corpus = TextCorpus(from_file='iliad.txt', corpus_type='word')

# Creating an IntegerEncoder
encoder = IntegerEncoder()

# Learns the encoding based on the TextCorpus dictionary and reverse dictionary
encoder.learn(corpus.vocab_index, corpus.index_vocab)

# Creating the LSTM
lstm = LSTMGenerator(encoder=encoder, vocab_size=corpus.vocab_size, embedding_size=256, hidden_size=1024)

# Loading pre-trained RNN weights
lstm.load_weights('lstm').expect_partial()

# Now, for the inference step, we build with a batch size equals to 1
lstm.build((1, None))

# Defining an start string to generate the text
start_string = 'his temples spreads his golden wing'

# Generating artificial text
text = lstm.generate_text(start=start_string.split(' '), length=100, temperature=0.5)

# Outputting the text
print(start_string + ' '.join(text))