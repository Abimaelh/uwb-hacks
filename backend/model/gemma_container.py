import kagglehub
import kaggle
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

# Download latest version
model_path = kagglehub.model_download("keras/gemma/keras/gemma_1.1_instruct_2b_en")
print("Path to model files:", model_path)

# Load the model (assuming you have enough GPU/CPU memory)
# You might need to adjust based on exact KaggleHub directory structure
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", torch_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained(model_path)

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

        return topics

    except Exception as e:
        print(f"Error extracting topics: {e}")
        return []

# Example usage
if __name__ == "__main__":
    test_text = "Homelessness and electric bills in Seattle, as well as rising healthcare costs."
    topics = extractTopics(test_text)
    print("Extracted Topics:", topics)
