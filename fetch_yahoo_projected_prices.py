import json
import pandas as pd
from datetime import datetime

# --- SETTINGS ---
INPUT_FILE = "yahoo_projected_2025_prices.json"

# Load the JSON
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

players = data["fantasy_content"]["league"]["players"]

player_info_list = []

for p in players:
    # Skip entries without 'player'
    if "player" not in p:
        continue

    player = p["player"]
    draft = player.get("draft_analysis", {})
    
    player_info = {
        "Name": player["name"]["full"],
        "Average Auction Cost": draft.get("average_cost"),
        "Average Pick": draft.get("average_pick"),
        "Projected Auction Value": player.get("projected_auction_value")
    }
    
    player_info_list.append(player_info)

# Convert to DataFrame
df = pd.DataFrame(player_info_list)

# Get current year dynamically
current_year = datetime.now().year
output_file = f"yahoo_projected_{current_year}_prices.csv"

# Save to CSV
df.to_csv(output_file, index=False, encoding="utf-8")

print(f"Saved Yahoo projected prices to {output_file}")
