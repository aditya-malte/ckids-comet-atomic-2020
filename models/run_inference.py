
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer

path = "/nas/home/linglan/ckids-comet-atomic-2020/models/comet_atomic2020_gpt2/checkpoint_1"

model = GPT2LMHeadModel.from_pretrained(path)
tokenizer = GPT2Tokenizer.from_pretrained(path)
text2text_generator = pipeline("text2text-generation",model=model, tokenizer=tokenizer)
print(text2text_generator)

while(True):
    print("Please enter an input...")
    input_text = input()
    if(input_text!="exit"):
        print(text2text_generator(input_text))
    else:
        break