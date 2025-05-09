YouTube Top-Liked Videos Fetcher

This script fetches all videos from a given YouTube channel and returns the top liked videos using the YouTube Data API v3.

    Accepts channel URLs including:
    
        https://www.youtube.com/channel/CHANNEL_ID
        https://www.youtube.com/user/USERNAME
        https://www.youtube.com/c/CUSTOM_NAME
        https://www.youtube.com/@HANDLE (YouTube handles)

    Retrieves all videos from the channel

    Displays a list of top videos by like count

    Supports sorting and easy extension to export results to CSV/JSON

Requirements

    Python 3.7+

    A YouTube Data API key from Google Cloud Console: https://console.cloud.google.com

Install dependencies:

    pip install google-api-python-client

    If you're using a restricted Python environment (Debian/Ubuntu), run:

    pip install --user --break-system-packages google-api-python-client

Enter a valid YouTube channel URL when prompted:

      https://www.youtube.com/@LinusTechTips
  
      https://www.youtube.com/channel/UCXuqSBlHAE6Xw-yeJA0Tunw
