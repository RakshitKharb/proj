# main/views.py

import os
import logging
from django.shortcuts import render
from django.conf import settings
from .utils.summarize_youtube import summarize_youtube_video
from .utils.text_generation import generate_text_response, summarize_text
from .utils.image_generation import generate_image_from_prompt
import base64

logger = logging.getLogger(__name__)

def index(request):
    response = None
    image_url = None
    summary = None
    error = None

    if request.method == 'POST':
        input_type = request.POST.get('input_type')

        if input_type == 'text':
            user_text = request.POST.get('text_input')
            if user_text:
                try:
                    response = generate_text_response(user_text)
                    logger.info(f"Text Query Success: {user_text}")
                except Exception as e:
                    error = str(e)
                    logger.error(f"Text Query Error: {e}")
            else:
                error = "Please enter a text query."
                logger.warning("Text Query Warning: Empty input.")

        elif input_type == 'image_upload':
            file = request.FILES.get('image_input')
            if not file:
                error = "No file uploaded."
                logger.warning("Image Upload Warning: No file uploaded.")
            else:
                if file.name == '':
                    error = "No selected file."
                    logger.warning("Image Upload Warning: No file selected.")
                else:
                    try:
                        from PIL import Image
                        image = Image.open(file).convert("RGB")
                        image_url = image_to_data_uri(image)
                        response = "Image uploaded and processed successfully."
                        logger.info("Image Upload Success.")
                    except Exception as e:
                        error = f"Error processing image: {str(e)}"
                        logger.error(f"Image Upload Error: {e}")

        elif input_type == 'youtube':
            youtube_url = request.POST.get('youtube_input')
            if youtube_url:
                try:
                    summary = summarize_youtube_video(youtube_url)
                    logger.info(f"YouTube Summarization Success for URL: {youtube_url}")
                except Exception as e:
                    error = f"Error summarizing YouTube video: {str(e)}"
                    logger.error(f"YouTube Summarization Error for URL {youtube_url}: {e}")
            else:
                error = "Please enter a YouTube video URL."
                logger.warning("YouTube Summarization Warning: Empty URL.")

        elif input_type == 'generate_image':
            prompt = request.POST.get('image_prompt')
            if prompt:
                try:
                    image_url = generate_image_from_prompt(prompt)
                    response = "Image generated successfully."
                    logger.info(f"Image Generation Success for prompt: {prompt}")
                except Exception as e:
                    error = f"Error generating image: {str(e)}"
                    logger.error(f"Image Generation Error for prompt '{prompt}': {e}")
            else:
                error = "Please enter an image prompt."
                logger.warning("Image Generation Warning: Empty prompt.")

    context = {
        'response': response,
        'image_url': image_url,
        'summary': summary,
        'error': error
    }

    return render(request, 'main/index.html', context)

def image_to_data_uri(image):
    """
    Converts a PIL Image to a data URI for displaying in HTML.
    """
    import base64
    from io import BytesIO

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"
