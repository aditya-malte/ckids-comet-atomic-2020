from transformers import pipeline, AutoModelWithLMHead, AutoTokenizer

path = "/nas/home/malte/ckids-comet-atomic-2020/models/comet_atomic2020_gpt2/model_files/checkpoint_0"

model = AutoModelWithLMHead.from_pretrained(path)
tokenizer = AutoTokenizer.from_pretrained(path)
text2text_generator = pipeline("text2text-generation",model=model, tokenizer=tokenizer)
print(text2text_generator)

while(True):
    print("Please enter an input...")
    input_text = input()
    if(input_text!="exit"):
        print(text2text_generator(input_text))
    else:
        break
