from transformers import *
import torch

tokenizer = T5Tokenizer.from_pretrained('t5-small')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('The generating is running on %s'%device)

model = T5ForConditionalGeneration.from_pretrained('t5-small')
model = model.to(device)

checkpoint_path = 'results/CSNpyEx2/model/checkpoint-34000/pytorch_model.bin'
model.load_state_dict(torch.load(checkpoint_path))

while True:
    input_code = input('Please enter the code snippet:\n')
    input_ids = tokenizer.encode(input_code, return_tensors='pt').to(device)

    greedy_output = model.generate(input_ids)
    print('Greedy Output:\n', tokenizer.decode(greedy_output[0]))

    beam_outputs = model.generate(
        input_ids, 
        num_beams=5, 
        no_repeat_ngram_size=2, 
        num_return_sequences=5, 
        early_stopping=True
    )

    print('Beam Search Output:\n')
    for i, beam_output in enumerate(beam_outputs):
        print("{}: {}".format(i, tokenizer.decode(beam_output, skip_special_tokens=True)))