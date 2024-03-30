import pandas as pd

# Load your dataset into a Pandas DataFrame
dataset = pd.read_csv('d22.csv')

def get_crop_details(predicted_crop_name):
    # Search for the predicted crop name in the dataset
    matched_rows = dataset[dataset['crop name '] == predicted_crop_name]

    if matched_rows.empty:
        return 'Crop not found.'

        # Extract the desired values from the matched row(s)
    life_span = matched_rows.iloc[0]['life spam ']
    total_cost = matched_rows.iloc[0]['approximate cost ']
    fertilizers = matched_rows.iloc[0]['organic fertilizers']
    season = matched_rows.iloc[0]['best season ']
    vl = matched_rows.iloc[0]['video link ']
    return life_span, total_cost, fertilizers, season, vl

