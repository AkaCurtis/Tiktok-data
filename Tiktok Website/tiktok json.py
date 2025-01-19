from flask import Flask, request, render_template, redirect, flash
import json
from collections import Counter

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flashing messages

def extract_data(file_data):
    try:
        # Parse JSON
        data = json.loads(file_data)

        # Video Browsing History
        browsing_history = find_key(data, "Video Browsing History")
        video_list = browsing_history.get("VideoList", []) if browsing_history else []
        video_count = len(video_list)

        # Most repetitive URL
        most_watched = None
        if video_list:
            urls = [video.get("Link") for video in video_list]
            url_counts = Counter(urls)
            most_common_url, count = url_counts.most_common(1)[0]
            most_watched = {
                "url": most_common_url,
                "count": count
            }

        # Following
        following_list = find_key(data, "Following List")
        following_count = len(following_list.get("Following", [])) if following_list else 0

        # Followers
        followers_list = find_key(data, "Follower List")
        followers_count = len(followers_list.get("FansList", [])) if followers_list else 0

        # Liked Videos
        like_list = find_key(data, "Like List")
        liked_videos_count = len(like_list.get("ItemFavoriteList", [])) if like_list else 0

        return {
            "video_count": video_count,
            "most_watched": most_watched,
            "following_count": following_count,
            "followers_count": followers_count,
            "liked_videos_count": liked_videos_count,
        }
    except json.JSONDecodeError:
        return None

def find_key(data, target_key):
    """Recursively search for a key in a nested JSON structure."""
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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if not uploaded_file:
            flash("No file uploaded. Please upload a valid JSON file.")
            return redirect(request.url)

        file_data = uploaded_file.read().decode("utf-8")
        extracted_data = extract_data(file_data)

        if extracted_data is None:
            flash("This file is not a JSON. Please upload a valid JSON file!")
            return redirect(request.url)

        return render_template("index.html", extracted_data=extracted_data)

    return render_template("index.html", extracted_data=None)

if __name__ == "__main__":
    app.run(debug=True)
