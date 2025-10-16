╔══════════════════════════════════════════════════════════════╗
║              🏆  THE ULTIMATE LEAGUE  –  SCRIPT GUIDE        ║
╚══════════════════════════════════════════════════════════════╝

📦  BEFORE THE DRAFT
────────────────────

1️⃣  Download Yahoo ADP prices at a specific time from 
        https://basketball.fantasysports.yahoo.com/nba/draftanalysis?type=salcap
    → file:  `yahoo_projected_prices.json`

2️⃣  Feed this file into:
        fetch_yahoo_projected_prices.py
    → Output: CSV with Yahoo projected auction prices per player

3️⃣  Run:
        fetch_fantrax_salary_prices.py
    → Output: `fantrax_previous_year_{year}_prices.csv`
      (includes player name, rostered status, and salary)

4️⃣  Download Fantrax blank player spreadsheet:  
    Commissioner → League Setup → Salaries & Contracts →  
    ➜ “Get Blank Player Spreadsheet (CSV)”

5️⃣  Run:
        update_fantrax_csv_prices.py
    → Output: final keeper prices CSV

6️⃣  Make a **backup** of this file just in case.

7️⃣  Drop all players from each team in Fantrax.

8️⃣  Import the updated CSV:
        Commissioner → League Setup → Salaries & Contracts →  
        “Choose file to upload completed spreadsheet”

9️⃣  Reassign all players to their correct teams.


📅  AFTER KEEPERS ARE CHOSEN (BEFORE THE DRAFT)
───────────────────────────────────────────────
We update the **SAL** column for free agents only.  
(keepers remain unchanged)

1️⃣  Run:
        fetch_fantrax_salary_prices.py
    → Output: `fantrax_previous_year_{year}_prices.csv`

2️⃣  Open `update_fantrax_csv_prices.py` and **edit the pricing rule:**

        ✅ Before draft:
            # new_price = int(yahoo_price)  # Set Yahoo projected price for all FAs in the draft pool.

3️⃣  Run the script again.

4️⃣  Import the output CSV file back into Fantrax:
        Commissioner → League Setup → Salaries & Contracts →  
        “Choose file to upload completed spreadsheet”


🏁  AFTER THE DRAFT
───────────────────

1️⃣  Open `update_fantrax_csv_prices.py` and **edit the pricing rule:**

    ✅  After draft:
        new_price = 5   # Set fixed price for all FAs

2️⃣  Run the script again.

3️⃣  Import the output CSV file into Fantrax:
        Commissioner → League Setup → Salaries & Contracts →  
        “Choose file to upload completed spreadsheet”


🎉  AAAAND WE’RE DONE!
──────────────────────
All keeper and free agent prices are now up to date!

** Some comments in the files that look like duplicates exist only for naming purposes.