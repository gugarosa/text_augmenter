import torch
from torch.nn import functional as F
from textfier.tasks import CausalLanguageModelingTask
from transformers import top_k_top_p_filtering

# Creates a causal language modeling task
task = CausalLanguageModelingTask(model='gpt2')

# Defines the input seed
seed = 'I would like to go to the zoo and '

# Encodes the input
inputs = task.tokenizer.encode(seed, return_tensors='pt')

# Passes the inputs through the model and gathers the logits
logits = task.model(inputs)[0][:, -1, :]

# Filters the logits
filtered_logits = top_k_top_p_filtering(logits, top_k=50, top_p=1.0)

# Gathers the softmax distribution and samples the logits
probs = F.softmax(filtered_logits, dim=-1)
token = torch.multinomial(probs, num_samples=1)

# Concatenates the generated token with the input seed and decodes into text
generated = task.tokenizer.decode(torch.cat([inputs, token], dim=-1).tolist()[0])
print(generated)
