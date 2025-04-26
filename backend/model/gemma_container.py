import kagglehub

# Download latest version
path = kagglehub.model_download("keras/gemma/keras/gemma_1.1_instruct_2b_en")

print("Path to model files:", path)

def extractTopics(inputText):

    topics = []

    return topics


"""
from transformers import pipeline

pipe = pipeline("text-generation", model="google/gemma-2b-it")  # adjust based on your local setup

def extract_topics(text):
    prompt = f"List the main issues from this text: '{text}'."
    output = pipe(prompt, max_new_tokens=50, temperature=0.3)
    raw_text = output[0]["generated_text"]
    topics = [t.strip().lower() for t in raw_text.split(',')]
    return topics
"""