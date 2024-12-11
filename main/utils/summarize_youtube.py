# main/utils/summarize_youtube.py

from .text_generation import summarize_text
import yt_dlp  # Use yt-dlp instead of youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import logging

def summarize_youtube_video(youtube_url):
    """
    Downloads the transcript of a YouTube video and summarizes it.
    """
    try:
        ydl_opts = {
            'skip_download': True,
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            video_title = info_dict.get('title', None)
            video_id = info_dict.get('id', None)
            if not video_id:
                raise ValueError("Could not extract video ID from the URL.")

        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Choose the English transcript
        transcript = transcript_list.find_transcript(['en'])
        transcript_data = transcript.fetch()

        # Combine the transcript text
        full_text = " ".join([entry['text'] for entry in transcript_data])

        # Summarize the transcript
        summary = summarize_text(full_text, max_length=300)
        logging.info(f"YouTube video '{video_title}' summarized successfully.")
        return summary

    except TranscriptsDisabled:
        logging.error(f"Transcripts are disabled for video: {youtube_url}")
        return "Transcripts are disabled for this YouTube video."
    except NoTranscriptFound:
        logging.error(f"No transcript found for video: {youtube_url}")
        return "No transcript found for this YouTube video."
    except Exception as e:
        logging.error(f"Error summarizing YouTube video {youtube_url}: {e}")
        return f"An error occurred while summarizing the video: {e}"
