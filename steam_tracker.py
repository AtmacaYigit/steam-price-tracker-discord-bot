import requests
import json

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1540992368155689010/XK5IVXkR43z1Cfax4umplrB68WbhMqk7Yl28dS4IDZucZzAsjGcylslhTvUW_ffcdq8jYOUR_DISCORD_WEBHOOK_URL"
TRACK_LIST = ["1091500", "292030"]  # Cyberpunk 2077, The Witcher 3


def get_steam_game_price(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=us&l=en"
    try:
        response = requests.get(url)
        data = response.json()
        
        if str(app_id) in data and data[str(app_id)]["success"]:
            game_data = data[str(app_id)]["data"]
            name = game_data.get("name", "Unknown")
            header_image = game_data.get("header_image", "")
            store_url = f"https://store.steampowered.com/app/{app_id}/"
            
            if game_data.get("is_free", False):
                return {
                    "name": name, "is_free": True, "discount_percent": 0,
                    "final_price": "Free", "image": header_image, "url": store_url
                }
            
            price_data = game_data.get("price_overview")
            if price_data:
                return {
                    "name": name,
                    "is_free": False,
                    "discount_percent": price_data.get("discount_percent", 0),
                    "initial_price": price_data.get("initial_formatted", ""),
                    "final_price": price_data.get("final_formatted", "N/A"),
                    "image": header_image,
                    "url": store_url
                }
    except Exception as e:
        print(f"Error: {e}")
    return None


def send_discord_notification(game):
    if not DISCORD_WEBHOOK_URL or "YOUR_DISCORD" in DISCORD_WEBHOOK_URL:
        print("Please provide a valid Discord Webhook URL.")
        return

    color = 0x2ecc71 if game["discount_percent"] > 0 else 0x3498db
    
    embed_data = {
        "title": f"🎮 {game['name']}",
        "url": game["url"],
        "color": color,
        "fields": [
            {"name": "Current Price", "value": game["final_price"], "inline": True},
            {"name": "Discount", "value": f"%{game['discount_percent']}", "inline": True}
        ],
        "image": {"url": game["image"]},
        "footer": {"text": "Steam Price Tracker Bot"}
    }
    
    if game["discount_percent"] > 0:
        embed_data["fields"].append(
            {"name": "Original Price", "value": game["initial_price"], "inline": True}
        )

    payload = {
        "content": "🔔 **Steam Price Alert!**",
        "embeds": [embed_data]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 204:
        print(f"[{game['name']}] notification sent to Discord successfully.")
    else:
        print(f"Discord error: {response.status_code}")


for app_id in TRACK_LIST:
    game_info = get_steam_game_price(app_id)
    if game_info and game_info["discount_percent"] > 0:
        send_discord_notification(game_info)