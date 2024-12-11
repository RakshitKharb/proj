# test_text_generation.py

print("test_text_generation.py is running...")  # Debugging

from utils.text_generation import generate_text_response
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    print("Starting text generation test...")  # Debugging
    prompt = "You are a helpful assistant. What are the benefits of renewable energy?"
    try:
        response = generate_text_response(prompt)
        print("Response:", response)
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
