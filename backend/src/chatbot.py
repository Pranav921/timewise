from transformers import AutoModelForCausalLM, AutoTokenizer
model_name = "tiiuae/falcon-7b-instruct"
cache_dir = "model_cache"

# Load the tokenizer and model with a custom cache directory
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    cache_dir=cache_dir,
    device_map="auto",
    torch_dtype="auto"
)

prompt = ("Hi. My name is John. I am an upcoming freshman at University of Florida and I want to pursue computer graphics. "
          "I am unsure what math classes I am required to take for computer graphics. Additionally, I am super interested "
          "in statistics and want to take many statistics classes. Can you give me suggestions of what type of math and "
          "statistics class I should take? Also, just provide me general insight about what I should do.")

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(inputs["input_ids"], max_length=2500, temperature=0.7)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))