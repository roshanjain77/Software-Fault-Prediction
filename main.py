import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Replace 'microsoft/codebert-base' with the actual model name you have
model_name = 'microsoft/codebert-base'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Input text
prompt = "Generate a Python function that adds two numbers."

# Tokenize input text
inputs = tokenizer.encode("python code generation: " + prompt, return_tensors="pt")

# Generate code
with torch.no_grad():
    output = model.generate(inputs, max_length=100, num_return_sequences=1, no_repeat_ngram_size=2)

# Decode generated code
generated_code = tokenizer.decode(output[0], skip_special_tokens=True)

print("Generated Code:")
print(generated_code)
