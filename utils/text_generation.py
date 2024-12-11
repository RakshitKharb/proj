# main/utils/text_generation.py

from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch
import logging

logger = logging.getLogger(__name__)

# Initialize the text generation model once
try:
    logger.info("Initializing text generation model...")
    model_name = "EleutherAI/gpt-neo-125M"  # Consider upgrading to "EleutherAI/gpt-neo-1.3B" for better performance
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    logger.info(f"Tokenizer eos_token_id before: {tokenizer.eos_token_id}")

    # Ensure eos_token_id is set
    if tokenizer.eos_token_id is None:
        tokenizer.eos_token_id = 50256
        logger.info("Set eos_token_id to 50256")
    else:
        logger.info(f"Tokenizer eos_token_id after: {tokenizer.eos_token_id}")

    # Ensure pad_token_id is set
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
        logger.info(f"Set pad_token_id to eos_token_id: {tokenizer.eos_token_id}")
    else:
        logger.info(f"Tokenizer pad_token_id: {tokenizer.pad_token_id}")

    # Set model_max_length to guide the tokenizer
    tokenizer.model_max_length = 512

    model = AutoModelForCausalLM.from_pretrained(model_name)
    text_generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=-1  # Use -1 for CPU
    )
    logger.info("Text generation model initialized successfully.")
except Exception as e:
    logger.error(f"Text Generation Initialization Error: {e}")
    raise e

def generate_text_response(prompt, max_new_tokens=150):
    """
    Generates a text response using the text generation model.
    """
    try:
        logger.info("Generating text response...")
        generated = text_generator(
            prompt,
            max_new_tokens=max_new_tokens,  # Use max_new_tokens instead of max_length
            num_return_sequences=1,
            do_sample=True,             # Enable sampling
            temperature=0.7,            # Balance between determinism and creativity
            top_p=0.9,                  # Nucleus sampling
            pad_token_id=tokenizer.eos_token_id if tokenizer.eos_token_id is not None else 50256,
            repetition_penalty=1.3,     # Discourages repetition
            no_repeat_ngram_size=3      # Prevents repeating trigrams
            # early_stopping=True        # Removed to align with num_beams=1
        )
        response = generated[0]['generated_text'].strip()
        logger.info("Text response generated successfully.")
        return response
    except Exception as e:
        logger.error(f"Text Generation Error: {e}")
        raise e

def summarize_text(text, max_new_tokens=150):
    """
    Summarizes the given text using the text generation model.
    """
    try:
        logger.info("Generating summary for the text...")
        prompt = f"Summarize the following text in a concise paragraph:\n\n{text}\n\nSummary:"
        summary = generate_text_response(prompt, max_new_tokens=max_new_tokens)
        logger.info("Summary generated successfully.")
        # Remove the prompt from the generated text
        summary = summary.split("Summary:")[-1].strip()
        return summary
    except Exception as e:
        logger.error(f"Text Summarization Error: {e}")
        raise e
