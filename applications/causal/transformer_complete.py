from textfier.tasks import CausalLanguageModelingTask

# Creates a causal language modeling task
task = CausalLanguageModelingTask(model='xlnet-base-cased')

# Usage of padding text helps XLNet with short seeds
# Proposed by Aman Rusia in https://github.com/rusiaaman/XLNet-gen#methodology
PADDING = '''In 1991, the remains of Russian Tsar Nicholas II and his family
(except for Alexei and Maria) are discovered.
The voice of Nicholas's young son, Tsarevich Alexei Nikolaevich, narrates the
remainder of the story. 1883 Western Siberia,
a young Grigori Rasputin is asked by his father and a group of men to perform magic.
Rasputin has a vision and denounces one of the men as a horse thief. Although his
father initially slaps him for making such an accusation, Rasputin watches as the
man is chased outside and beaten. Twenty years later, Rasputin sees a vision of
the Virgin Mary, prompting him to become a priest. Rasputin quickly becomes famous,
with people, even a bishop, begging for his blessing. <eod> </s> <eos>'''

# Defines the input seed
seed = 'I would like to go to the zoo and '

# Encodes the input
inputs = task.tokenizer.encode(PADDING + seed, add_special_tokens=False, return_tensors='pt')

# Gathers the length of padded input
length = len(task.tokenizer.decode(inputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True))

# Performs the generation
outputs = task.model.generate(inputs, max_length=250, do_sample=True, top_p=0.95, top_k=60)

# Decodes the generation outputs
generated = seed + task.tokenizer.decode(outputs[0])[length:]
print(generated)