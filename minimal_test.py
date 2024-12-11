# minimal_test.py

print("minimal_test.py is running...")

from transformers import pipeline
import logging

def main():
    print("Initializing text generation model...")
    try:
        # Initialize the pipeline with a smaller model
        generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M", device=-1)
        print("Model initialized successfully.")

        # Generate a response
        prompt = "You are a helpful assistant. What are the benefits of renewable energy?"
        print(f"Generating response for prompt: {prompt}")
        response = generator(prompt, max_length=100, num_return_sequences=1)
        print("Response:", response[0]['generated_text'].strip())
    except Exception as e:
        print("An error occurred:", e)
        logging.error(f"Error in minimal_test.py: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
