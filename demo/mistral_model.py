from transformers import AutoModelForCausalLM, AutoTokenizer
import transformers
import torch
from langchain.llms import HuggingFacePipeline

MODEL_PATH = "mistralai/Mistral-7B-Instruct-v0.2"
device = 'cuda' if torch.cuda.is_available() else 'cpu'


model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, load_in_4bit=True, device_map='auto')
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

text_generation_pipeline = transformers.pipeline(
    model=model,
    tokenizer=tokenizer,
    task="text-generation",
    temperature=0.2,
    repetition_penalty=1.1,
    return_full_text=False,
    max_new_tokens=2000,
    do_sample = True
)

llm = HuggingFacePipeline(pipeline=text_generation_pipeline)
