# test_summarize_youtube.py

from utils.summarize_youtube import summarize_youtube_video

def main():
    youtube_url = "https://youtu.be/V-ypx6Rmu_k?si=82jLTOPy_ZoN0o3V"  # Replace with a valid URL with transcript
    try:
        summary = summarize_youtube_video(youtube_url)
        print("Summary:", summary)
    except ValueError as ve:
        print("Error:", ve)
    except Exception as e:
        print("Unexpected Error:", e)

if __name__ == "__main__":
    main()
