import json
import os
import time
import requests

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "YOUR_DISCORD_WEBHOOK_URL")
DATA_FILE = "tracked_data.json"

TRACK_LIST = [
    "1091500",  # Cyberpunk 2077
    "292030",   # The Witcher 3: Wild Hunt
    "1245620",  # Elden Ring
    "271590",   # GTA V
    "252490",   # Rust
]

def load_history():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_history(history):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def get_steam_game_price(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=us&l=english"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if not data or not data.get(str(app_id), {}).get("success"):
            return None

        game_data = data[str(app_id)]["data"]
        name = game_data.get("name", "Unknown Game")
        image = game_data.get("header_image", "")
        store_url = f"https://store.steampowered.com/app/{app_id}"

        if game_data.get("is_free"):
            return {
                "name": name,
                "is_discounted": False,
                "discount_percent": 0,
                "current_price": "Free",
                "original_price": "Free",
                "image": image,
                "store_url": store_url
            }

        price_overview = game_data.get("price_overview")
        if not price_overview:
            return None

        discount_percent = price_overview.get("discount_percent", 0)
        current_price = price_overview.get("final_formatted", "N/A")
        original_price = price_overview.get("initial_formatted", "N/A")

        return {
            "name": name,
            "is_discounted": discount_percent > 0,
            "discount_percent": discount_percent,
            "current_price": current_price,
            "original_price": original_price,
            "image": image,
            "store_url": store_url
        }
    except Exception as e:
        print(f"Error fetching app {app_id}: {e}")
        return None

def send_discord_notification(game_info):
    if not DISCORD_WEBHOOK_URL or DISCORD_WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_URL":
        print("Discord Webhook URL is missing.")
        return

    embed = {
        "title": f"🚨 Steam Price Alert: {game_info['name']}",
        "url": game_info["store_url"],
        "color": 3066993,
        "fields": [
            {"name": "Discount", "value": f"%{game_info['discount_percent']}", "inline": True},
            {"name": "Current Price", "value": game_info["current_price"], "inline": True},
            {"name": "Original Price", "value": game_info["original_price"], "inline": True}
        ],
        "image": {"url": game_info["image"]},
        "footer": {"text": "Steam Price Tracker Bot"}
    }

    payload = {"embeds": [embed]}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code in [200, 204]:
            print(f"Notification sent for {game_info['name']}")
        else:
            print(f"Failed to send notification: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending webhook: {e}")

def main():
    history = load_history()
    updated = False

    for app_id in TRACK_LIST:
        game_info = get_steam_game_price(app_id)
        if not game_info:
            continue

        last_state = history.get(app_id, {})
        last_discount = last_state.get("discount_percent", 0)

        # Eğer oyun şu an indirimdeyse
        if game_info["is_discounted"]:
            # Daha önce indirimde değilse veya indirim oranı değiştiyse bildirim gönder
            if game_info["discount_percent"] != last_discount:
                send_discord_notification(game_info)
                history[app_id] = {
                    "discount_percent": game_info["discount_percent"],
                    "current_price": game_info["current_price"]
                }
                updated = True
        else:
            # İndirim bitmişse geçmiş durumunu temizle
            if app_id in history and history[app_id].get("discount_percent", 0) > 0:
                history[app_id] = {
                    "discount_percent": 0,
                    "current_price": game_info["current_price"]
                }
                updated = True

        time.sleep(1)

    if updated:
        save_history(history)
        print("History data updated.")
    else:
        print("No price changes detected. No notification sent.")

if __name__ == "__main__":
    main()
