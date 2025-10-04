import pandas as pd
from unidecode import unidecode
from rapidfuzz import fuzz, process
from datetime import datetime

# ----------------- SETTINGS -----------------
year = datetime.now().year
last_year = year - 1

# ----------------- LOAD CSVs -----------------
fantrax_template_df = pd.read_csv("FantraxPlayers_5xvrqu1fmg2626hw.csv")  # template for output
yahoo_df = pd.read_csv(f"yahoo_projected_{year}_prices.csv")
fantrax_prev_df = pd.read_csv(f"fantrax_previous_year_{last_year}_prices.csv")

# ----------------- NORMALIZE NAMES -----------------
def normalize_name(name):
    return unidecode(str(name)).lower().strip()

fantrax_template_df['name_norm'] = fantrax_template_df.iloc[:, 2].apply(normalize_name)
yahoo_df['name_norm'] = yahoo_df['Name'].apply(normalize_name)
fantrax_prev_df['name_norm'] = fantrax_prev_df['name'].apply(normalize_name)

# ----------------- FUZZY MATCHING -----------------
def build_fuzzy_name_map(source_names, target_names, threshold=80):
    mapping = {}
    for s in source_names:
        match = process.extractOne(
            s, target_names, scorer=fuzz.token_sort_ratio
        )
        if match:
            candidate, score, _ = match
            if score >= threshold:
                mapping[s] = candidate
    return mapping

# Map Yahoo and previous-year names to template names
yahoo_to_template = build_fuzzy_name_map(
    yahoo_df['name_norm'].unique(), fantrax_template_df['name_norm'].unique()
)
prev_to_template = build_fuzzy_name_map(
    fantrax_prev_df['name_norm'].unique(), fantrax_template_df['name_norm'].unique()
)

# Assign fuzzy-mapped names
yahoo_df['name_mapped'] = yahoo_df['name_norm'].map(lambda n: yahoo_to_template.get(n))
fantrax_prev_df['name_mapped'] = fantrax_prev_df['name_norm'].map(lambda n: prev_to_template.get(n))

# Re-map the template itself so names align with fuzzy matches
reverse_map = {**{v: v for v in yahoo_to_template.values()},
               **{v: v for v in prev_to_template.values()}}
fantrax_template_df['name_norm'] = fantrax_template_df['name_norm'].map(lambda n: reverse_map.get(n, n))

# Keep only players present in all datasets
valid_names = set(yahoo_df['name_mapped'].dropna()).intersection(
    set(fantrax_prev_df['name_mapped'].dropna())
)
fantrax_template_df = fantrax_template_df[fantrax_template_df['name_norm'].isin(valid_names)].reset_index(drop=True)

# ----------------- BUILD DICTIONARIES -----------------
yahoo_dict = dict(zip(yahoo_df['name_mapped'], yahoo_df['Projected Auction Value']))
fantrax_prev_dict = dict(zip(fantrax_prev_df['name_mapped'], fantrax_prev_df['value']))
fantrax_prev_keeper = dict(zip(fantrax_prev_df['name_mapped'], fantrax_prev_df['keeper']))

# ----------------- FUNCTIONS -----------------
def get_yahoo_value(name):
    if not name:
        return 0
    return int(yahoo_dict.get(name, 0))

def get_fantrax_prev_value(name):
    return int(fantrax_prev_dict.get(name, 0))

def compute_new_price(row):
    # If no team → return 1
    if pd.isna(row.iloc[3]) or str(row.iloc[3]).strip() == "":
        return 1

    fantrax_price = get_fantrax_prev_value(row['name_norm'])
    yahoo_price = get_yahoo_value(row['name_norm'])

    # Check keeper status
    is_keeper = bool(fantrax_prev_keeper.get(row['name_norm'], False))

    try:
        if is_keeper:
            new_price = round(1.1 * ((0.62 * float(fantrax_price)) + (0.38 * float(yahoo_price))))
        else:
            new_price = int(yahoo_price)
    except:
        new_price = 1
    return int(new_price)

# ----------------- APPLY FORMULA -----------------
fantrax_template_df.iloc[:, 5] = fantrax_template_df.apply(compute_new_price, axis=1)

# Drop helper column
fantrax_template_df.drop(columns=['name_norm'], inplace=True)

# ----------------- SAVE RESULT -----------------
output_file = f"fantrax_cleaned_final_prices.csv"
fantrax_template_df.to_csv(output_file, index=False)
print(f"Updated Fantrax CSV created: {output_file}")
