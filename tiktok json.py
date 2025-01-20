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

def parse_price(price_str):
    try:
        return float(price_str.split()[0])
    except:
        return 0.0

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    browsing_history = find_key(data, "Video Browsing History")
    video_list = browsing_history.get("VideoList", []) if browsing_history else []
    total_videos = len(video_list)
    print(f"You have watched {total_videos} TikTok video(s).")

    if video_list:
        urls = [video.get("Link") for video in video_list if video.get("Link")]
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

    order_history = find_key(data, "Order History")
    order_histories = order_history.get("OrderHistories", {}) if order_history else {}
    total_orders = len(order_histories)
    total_spent = sum(
        parse_price(order.get("total_price", "0 USD")) for order in order_histories.values()
    )
    print(f"You have made {total_orders} order(s) through TikTok Shop.")
    print(f"Total amount spent on TikTok Shop: {total_spent:.2f} USD.")

    product_browsing_history = find_key(data, "Product Browsing History")
    product_browsed = product_browsing_history.get("ProductBrowsingHistories", []) if product_browsing_history else []
    total_products_browsed = len(product_browsed)
    print(f"You have browsed {total_products_browsed} product(s).")

    if product_browsed:
        shop_names = [product.get("shop_name") for product in product_browsed if product.get("shop_name")]
        shop_counts = Counter(shop_names)
        most_common_shop, shop_count = shop_counts.most_common(1)[0]
        print(f"Most visited shop: {most_common_shop} {shop_count} times.")

    favorite_videos = find_key(data, "Favorite Videos")
    favorite_video_list = favorite_videos.get("FavoriteVideoList", []) if favorite_videos else []
    total_favorited_videos = len(favorite_video_list)
    print(f"You have favorited {total_favorited_videos} TikTok videos.")

except FileNotFoundError:
    print(f"The file '{file_path}' was not found. Please check the file path.")
except json.JSONDecodeError:
    print("The file does not contain valid JSON data.")
except Exception as e:
    print(f"An error occurred: {e}")
