import requests
import json
import pandas as pd
from datetime import datetime


# ---------------- SETTINGS ----------------
LEAGUE_ID = "5xvrqu1fmg2626hw"
URL = f"https://www.fantrax.com/fxpa/req?leagueId={LEAGUE_ID}"

# ---------------- COOKIES ----------------
cookies = {
    "cf_clearance": "d0mEzwhue5YrP9bqAiflUccOf2ceSJFliEBMsN5J9F0-1759443564-1.2.1.1-t0c_Q.kYNPj3V1nTM5ahqD8ol5S_xjXLFKPzhTBW.Hqbwq4bMEdWTEuVZg2jXyTpJNMpbVzb3WixjkVi6nF8d8rN3JebW6nVTv5gVv8bmjvVEWfXTpaIocVuefjdE7280mnRr7bs8jbWn6vbIlBcIXA520UsMmNlu9zFZEOf1v52ZG2nHB5rMs1SqTPV4v0_Z8ypx5ZGblAfuKEZwdUMaGYxfxJrWx9MRitZw9ZiwN8",
    "_cf_bm": "V1t2Eft4ms5LcteagFsq32nmCW.86HqbAP0rLdGt8_g-1759444435-1.0.1.1-u6l7M5k9UNiSaSLB6R8sP2lLlXR7z0cWpzM_h4ofPTzOMjpGYdOb3o.hhaM9Xu9CRsUyD4z8m5IIj2AncauzE7ydNq0PrS4CAbc0u2RiGb0",
    "uig": "2zowmigcmg69ydsr",
    "usnatUUID": "c5ea557e-1caf-4067-bc0b-291b090e90dd"
}

def fetch_page(page_number=1):
    payload = {
        "msgs": [
            {
                "method": "getPlayerStats",
                "data": {
                    "statusOrTeamFilter": "ALL",
                    "pageNumber": str(page_number)
                }
            }
        ]
    }
    resp = requests.post(URL, json=payload, cookies=cookies)
    resp.raise_for_status()

    # lala=resp.json()
    # print(json.dumps(lala, indent=2, ensure_ascii=False))  # pretty-print to console
    return resp.json()  

# Fetch first page to get total pages
first_page = fetch_page(1)
total_pages = first_page["responses"][0]["data"]["paginatedResultSet"]["totalNumPages"]

all_players = []

for page in range(1, total_pages + 1):
    print(f"Fetching page {page}/{total_pages}...")
    data = fetch_page(page)

    stats = data["responses"][0]["data"]["statsTable"]
    
    for row in stats:
        player_name = row["scorer"]["name"]
        value = row["cells"][4]["content"]  # fifth content contains the salary of the players
        isPartOfRoster = row["cells"][1]["content"] != "FA"
        all_players.append({"name": player_name, "value": value, "isPartOfRoster": isPartOfRoster})

# Save to CSV with dynamic last year in filename
last_year = datetime.now().year - 1
output_file = f"fantrax_previous_year_{last_year}_prices.csv"
# output_file = f"fantrax_prices_AFTER_keepers.csv"

df = pd.DataFrame(all_players)
df.to_csv(output_file, index=False, encoding="utf-8")

print(f"Saved {len(all_players)} players to {output_file}")



