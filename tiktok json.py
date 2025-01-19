import json
from collections import Counter

file_path = "user_data_tiktok.json"

def find_key(data, target_key):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            result = find_key(value, target_key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_key(item, target_key)
            if result is not None:
                return result
    return None

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    browsing_history = find_key(data, "Video Browsing History")
    video_list = browsing_history.get("VideoList", []) if browsing_history else []
    print(f"You have watched {len(video_list)} TikToks.")

    if video_list:
        urls = [video.get("Link") for video in video_list]
        url_counts = Counter(urls)
        most_common_url, count = url_counts.most_common(1)[0]
        print(f"You've watched this TikTok {count} time(s): {most_common_url}")

    following_list = find_key(data, "Following List")
    following_count = len(following_list.get("Following", [])) if following_list else 0
    print(f"You are following {following_count} user(s).")

    followers_list = find_key(data, "Follower List")
    followers_count = len(followers_list.get("FansList", [])) if followers_list else 0
    print(f"You have {followers_count} follower(s).")

    like_list = find_key(data, "Like List")
    liked_videos_count = len(like_list.get("ItemFavoriteList", [])) if like_list else 0
    print(f"You have liked {liked_videos_count} TikTok video(s).")

except FileNotFoundError:
    print(f"The file '{file_path}' was not found. Please check the file path.")
except json.JSONDecodeError:
    print("The file does not contain valid JSON data.")
except Exception as e:
    print(f"An error occurred: {e}")
