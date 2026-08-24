# 🎮 Steam Discount Tracker Discord Bot

A lightweight Python bot that checks Steam game prices using the official Steam Storefront API and sends rich Discord notifications when a tracked game is on sale.

## ✨ Features

* 🔎 Fetches game information and prices from the official Steam Storefront API
* 💰 Detects active Steam discounts
* 📢 Sends rich Discord Embed notifications through a webhook
* 🖼️ Displays the game's header image in the Discord notification
* 📊 Shows current price, original price, and discount percentage
* 🆓 Supports free-to-play games
* 🎮 Supports tracking multiple games using Steam App IDs
* ⚙️ Simple configuration through the Python script
* 🔗 Provides a direct link to the Steam store page

## 🖥️ Example

When a tracked game is discounted, the bot sends a Discord notification containing:

* Game name
* Current price
* Original price
* Discount percentage
* Game image
* Direct Steam store link

## 📸 Preview
<img width="489" height="730" alt="image" src="https://github.com/user-attachments/assets/a972778d-ec8f-4716-88c3-978bf9ebf836" />


## ⚙️ How It Works

The bot follows a simple process:

1. The configured Steam App IDs are loaded from `TRACK_LIST`.
2. The bot requests game information from the Steam Storefront API.
3. It checks the game's current price and discount percentage.
4. If a discount is detected, a Discord Embed is created.
5. The notification is sent to the configured Discord channel through a webhook.

## 🛠️ Technologies Used

* **Python**
* **Requests**
* **Steam Storefront API**
* **Discord Webhooks**
* **JSON**

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/AtmacaYigit/steam-price-tracker-discord-bot.git
cd steam-price-tracker-discord-bot
```

### 2. Install the required dependency

```bash
pip install requests
```

### 3. Configure the Discord Webhook

Open `steam_tracker.py` and replace:

```python
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"
```

with your Discord webhook URL.

> ⚠️ Never publish your real Discord webhook URL on GitHub.

### 4. Configure the games

Add the Steam App IDs of the games you want to track:

```python
TRACK_LIST = ["1091500", "292030"]
```

For example:

* `1091500` → Cyberpunk 2077
* `292030` → The Witcher 3: Wild Hunt

### 5. Run the bot

```bash
python steam_tracker.py
```

If a tracked game currently has a discount, the bot will send a notification to your configured Discord channel.

## 🎯 Finding Steam App IDs

You can find a game's App ID in its Steam store URL.

For example:

```text
https://store.steampowered.com/app/1091500/Cyberpunk_2077/
```

The App ID is:

```text
1091500
```

Add this ID to the `TRACK_LIST` in `steam_tracker.py`.

## 📁 Project Structure

```text
steam-price-tracker-discord-bot/
│
├── steam_tracker.py
└── README.md
```

## 🔮 Future Improvements

Possible improvements for future versions:

* [X] Automatic scheduled price checks
* [ ] Price history tracking
* [ ] SQLite database integration
* [ ] Configurable discount thresholds
* [ ] Discord slash commands
* [ ] Add and remove tracked games directly from Discord
* [X] Prevent duplicate notifications for the same discount
* [ ] Support multiple Discord servers/webhooks
* [ ] Track regional Steam prices
* [ ] Price history graphs

## 📌 Current Limitations

The current version runs the price check when the Python script is executed. It does not yet include an internal scheduler or database for persistent price history.

For continuous monitoring, the script can be executed periodically using tools such as **Windows Task Scheduler**, **cron**, or another external scheduling service.
