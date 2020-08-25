import tensorflow as tf

from nalp.corpus import TextCorpus
from nalp.datasets import LanguageModelingDataset
from nalp.encoders import IntegerEncoder
from nalp.models.generators import LSTMGenerator

# Creating a character TextCorpus from file
corpus = TextCorpus(from_file='iliad.txt', corpus_type='word')

# Creating an IntegerEncoder
encoder = IntegerEncoder()

# Learns the encoding based on the TextCorpus dictionary and reverse dictionary
encoder.learn(corpus.vocab_index, corpus.index_vocab)

# Applies the encoding on new data
encoded_tokens = encoder.encode(corpus.tokens)

# Creating Language Modeling Dataset
dataset = LanguageModelingDataset(encoded_tokens, max_length=25, batch_size=128)

# Creating the LSTM
lstm = LSTMGenerator(encoder=encoder, vocab_size=corpus.vocab_size, embedding_size=256, hidden_size=1024)

# As NALP's LSTMs are stateful, we need to build it with a fixed batch size
lstm.build((128, None))

# Compiling the LSTM
lstm.compile(optimizer=tf.optimizers.Adam(learning_rate=0.001),
            loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=[tf.metrics.SparseCategoricalAccuracy(name='accuracy')])

# Fitting the LSTM
lstm.fit(dataset.batches, epochs=100)

# Saving LSTM weights
lstm.save_weights('lstm', save_format='tf')