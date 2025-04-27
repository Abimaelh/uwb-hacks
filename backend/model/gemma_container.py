import os
import kagglehub
import kaggle
from huggingface_hub import login
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    raise ValueError("HuggingFace API key not found")

login(token=HUGGINGFACE_API_KEY)

# Download latest version
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")
model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-2b-it",
    torch_dtype=torch.bfloat16
)

# Initialize pipeline
nlp_pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)

def extractTopics(inputText: str):
    system_prompt = (
        "You are a civic data assistant helping extract public policy topics from user messages. "
        "Given an input text, output a clean list of the main issues, separated by commas. "
        "Do not include extra words. Do not repeat topics. Keep it concise."
    )

    prompt = f"{system_prompt}\n\nInput: {inputText}\n\nTopics:"

    try:
        output = nlp_pipe(prompt, max_new_tokens=50, temperature=0.2, do_sample=False)
        raw_text = output[0]['generated_text']
        
        # Extract only the part after 'Topics:'
        if 'Topics:' in raw_text:
            topics_part = raw_text.split('Topics:')[-1].strip()
        else:
            topics_part = raw_text.strip()

        # Split into a clean list
        topics = [topic.strip().lower() for topic in topics_part.split(',') if topic.strip()]

        # Optional: remove duplicates
        topics = list(dict.fromkeys(topics))
        print(type(topics))
        return topics

    except Exception as e:
        print(f"Error extracting topics: {e}")
        return []

# Example usage
if __name__ == "__main__":
    test_text = "Homelessness and electric bills in Seattle, as well as rising healthcare costs."
    topics = extractTopics(test_text)
    print("Extracted Topics:", topics)
