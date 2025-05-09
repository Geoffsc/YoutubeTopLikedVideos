from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
import re

# Replace with your API key
API_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_channel_id_from_url(url):

    parsed = urlparse(url)
    path = parsed.path.strip("/")
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    if path.startswith("channel/"):
        return path.split("/")[1]

    elif path.startswith("user/") or path.startswith("c/") or path.startswith("@"):
        # Extract handle or username
        identifier = path.split("/")[-1]
        if identifier.startswith("@"):
            identifier = identifier[1:]

        # Use search endpoint to resolve to channelId
        response = youtube.search().list(
            q=identifier,
            type="channel",
            part="snippet",
            maxResults=1
        ).execute()

        if not response["items"]:
            raise ValueError(f"No channel found for handle: {identifier}")

        return response["items"][0]["snippet"]["channelId"]

    else:
        raise ValueError(f"Invalid YouTube URL format: {url}")


def get_all_video_ids(channel_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    video_ids = []
    next_page_token = None

    while True:
        response = youtube.search().list(
            channelId=channel_id,
            part="id",
            order="date",
            maxResults=50,
            pageToken=next_page_token,
            type="video"
        ).execute()

        video_ids += [item["id"]["videoId"] for item in response["items"]]
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return video_ids

def get_video_stats(video_ids):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    stats = []
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i+50]
        response = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(chunk)
        ).execute()

        for item in response["items"]:
            stats.append({
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']}",
                "likes": int(item["statistics"].get("likeCount", 0))
            })
    return stats

def main():
    youtube_url = input("Enter YouTube channel URL: ").strip()
    channel_id = get_channel_id_from_url(youtube_url)
    print(f"Resolved channel ID: {channel_id}")

    video_ids = get_all_video_ids(channel_id)
    print(f"Found {len(video_ids)} videos")

    video_stats = get_video_stats(video_ids)
    sorted_videos = sorted(video_stats, key=lambda x: x["likes"], reverse=True)

    print("\nTop liked videos:")
    for video in sorted_videos[:10]:
        print(f"{video['likes']} likes - {video['title']} ({video['url']})")

if __name__ == "__main__":
    main()
