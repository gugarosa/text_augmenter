import torch

from textfier.tasks import MaskedLanguageModelingTask

# Creates a masked language modeling task
task = MaskedLanguageModelingTask(model='distilbert-base-cased')

# Defines the input text
text = f'Do you want to {task.tokenizer.mask_token} tomorrow?'

# Encodes the input
enc_text = task.tokenizer.encode(text, return_tensors='pt')

# Gathers the mask token's index
mask_token = torch.where(enc_text == task.tokenizer.mask_token_id)[1]

# Performs the generation and gathers the masked token predictions
preds = task.model(enc_text)[0]
mask_preds = preds[0, mask_token, :]

# Gathers the top-5 mask predictions
top_masks = torch.topk(mask_preds, 5, dim=1).indices[0].tolist()

# Iterates over all top-5 mask predictions
for mask in top_masks:
    print(text.replace(task.tokenizer.mask_token, task.tokenizer.decode([mask])))