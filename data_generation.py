import pandas as pd
import numpy as np

# Define data categories and ranges
locations = ["New York, NY", "Phoenix, AZ", "Los Angeles, CA", "San Diego, CA", "San Antonio, TX"]
listing_types = ["for_rent", "for_sale"]
styles = ["APARTMENT", "SINGLE_FAMILY", "CONDOS", "TOWNHOMES", "OTHER"]
beds_range = (1, 5)
baths_range = (1, 3)
sqft_range = (800, 3000)
year_built_range = (1950, 2020)
stories_range = (1, 3)
parking_range = (0, 3)

style_prob = [0.225, 0.225, 0.225, 0.225, 0.1]  # Adding up to 1 including 10% chance of NaN
beds_prob = [0.18, 0.18, 0.18, 0.18, 0.18, 0.1]  # Including NaN
baths_prob = [0.2, 0.4, 0.3, 0.1]  # Only for full baths, excluding NaN which is added below

# Number of records
num_records = 500

# Generate data
data = {
    "prompt": [],
    "location": np.random.choice(locations, num_records),
    "listing_type": np.random.choice(listing_types, num_records),
    "style": np.random.choice(styles, num_records, p=style_prob),
    "beds": np.random.choice(list(range(beds_range[0], beds_range[1] + 1)) + [np.nan], num_records, p=beds_prob),
    "full_baths": np.random.choice(list(range(baths_range[0], baths_range[1] + 1)) + [np.nan], num_records, p=baths_prob),
    "sqft": np.random.choice([np.nan] + list(range(sqft_range[0], sqft_range[1] + 1)), num_records),
    "year_built": np.random.choice([np.nan] + list(range(year_built_range[0], year_built_range[1] + 1)), num_records, p=[0.2] + [0.8/(year_built_range[1] - year_built_range[0] + 1)] * (year_built_range[1] - year_built_range[0] + 1)),
    "list_price": np.random.choice([np.nan] + list(range(100000, 1000000, 50000)), num_records, p=[0.1] + [0.9/18] * 18),
    "stories": np.random.choice([np.nan] + list(range(stories_range[0], stories_range[1] + 1)), num_records, p=[0.2, 0.4, 0.2, 0.2]),
    "parking_garage": np.random.choice([np.nan] + list(range(parking_range[0], parking_range[1] + 1)), num_records, p=[0.4, 0.1, 0.3, 0.1, 0.1])
}

# Convert items into natural language
data["listing_type_NL"] = ["buy" if x == "for_sale" else x for x in data["listing_type"]]
data["listing_type_NL"] = ["rent" if x == "for_rent" else x for x in data["listing_thype_NL"]]

data["style_NL"] = [x.lower().replace("_", " ") if not pd.isna(x) else x for x in data["style"]]
# also make style not plural
data["style_NL"] = [x[:-1] if x[-1] == 's' else x for x in data["style_NL"]]

# Generate prompts based on other fields
for i in range(num_records):
    if data['style'][i] != 'OTHER':
        prompt = f"I'm looking to {data['listing_type_NL'][i]} a {data['style_NL'][i]} in {data['location'][i]}"
    else:
        prompt = f"I'm looking to {data['listing_type_NL'][i]} in {data['location'][i]}"
    if not np.isnan(data['beds'][i]):
        prompt += f" with {int(data['beds'][i])} bedrooms"
    if not np.isnan(data['full_baths'][i]):
        prompt += f" and {int(data['full_baths'][i])} bathrooms"
    if not np.isnan(data['sqft'][i]):
        prompt += f", with at least {int(data['sqft'][i])} square feet"
    if not np.isnan(data['year_built'][i]):
        prompt += f", built after {int(data['year_built'][i])}"
    if not np.isnan(data['list_price'][i]):
        prompt += f", priced around {int(data['list_price'][i])}"
    if not np.isnan(data['stories'][i]):
        prompt += f", with {int(data['stories'][i])} stories"
    if not np.isnan(data['parking_garage'][i]):
        prompt += f", with parking for at least {int(data['parking_garage'][i])} cars"
    data['prompt'].append(prompt)

# Create DataFrame
expanded_data = pd.DataFrame(data)

# Save to CSV file
expanded_data.to_csv('expanded_real_estate_data.csv', index=False)
