import pandas as pd
import requests
from AAC_challenge import utils

from sklearn.preprocessing import OneHotEncoder

API_KEY = ''

def load_csv(dataset):
    """params: 
       'cats' to load cat outcomes dataset
       'all' to load entire outcomes dataset
       'intakes' to load entire intakes dataset
       'merged_with_locations' to load merged outcomes and intakes with lat and long"""
    if dataset == 'cats':
        cat_df = pd.read_csv("../raw_data/aac_data/aac_shelter_cat_outcome_eng.csv")
        return cat_df
    elif dataset == 'all':
        all_df = pd.read_csv("../raw_data/aac_data/aac_shelter_outcomes.csv")
        return all_df
    elif dataset == 'intakes':
        intake_df = pd.read_csv("../raw_data/aac_data/intakes.csv")
        return intake_df
    elif dataset == 'merged_with_locations':
        merged_df = pd.read_csv('../raw_data/merged_with_locations.csv')
        return merged_df

def clean_cat_dataset(cat_df):
    # drop some columns
    cat_df.drop(columns=['count', 'breed2', 'color2', 'monthyear', 'sex_upon_outcome',
                         'age_upon_outcome', 'sex_age_outcome',
                         'age_group', 'dob_year', 'dob_month', 'dob_monthyear', 'breed1',
                         'outcome_hour'], inplace = True)
    # replace double brown coat
    cat_df.coat = [x.strip() for x in cat_df.coat]
    # drop rows where outcome is NaN
    rows_to_drop = cat_df[cat_df.outcome_type.isna()]['outcome_type'].index
    cat_df.drop(index=rows_to_drop, inplace = True)
    # drop duplicates
    cat_df = cat_df.drop_duplicates(inplace=False).reset_index()
    # map cat/kitten to kitten (1 yes or no 0)
    cat_df['Cat/Kitten (outcome)'] = cat_df['Cat/Kitten (outcome)'].apply(lambda x: 0 if (x == 'Cat') else 1)
    # map binary features to 0 1
    cat_df.cfa_breed = cat_df.cfa_breed.apply(lambda x: 0 if (x == False) else 1)
    cat_df.domestic_breed = cat_df.domestic_breed.apply(lambda x: 0 if (x == False) else 1)
    cat_df['Spay/Neuter'] = cat_df['Spay/Neuter'].apply(lambda x: 0 if (x == 'No') else 1)
    cat_df.sex = cat_df.sex.apply(lambda x: 0 if (x == 'Male') else 1)
    # get has_name column then drop name column
    cat_df['has_name'] = utils.get_has_name(cat_df)
    cat_df.drop(columns='name', inplace = True)
    # get top_breeds
    cat_df['top_breeds'] = cat_df.breed.apply(utils.map_top_breeds)
    cat_df['top_coats'] = cat_df.coat.apply(utils.map_top_coats)
    # get adopted or not
    cat_df['adopted_or_not'] = cat_df.outcome_type.apply(utils.get_adopted_or_not)
    cat_df.drop(columns='outcome_subtype', inplace = True)
    # imputing missing values with most frequent
    cat_df = utils.impute_most_frequent(cat_df)
    cat_df.drop(columns=['index', 'animal_type'], inplace = True)
    # handle datetime columns
    cat_df['date_of_birth'] = pd.to_datetime(cat_df['date_of_birth'])
    cat_df['datetime'] = pd.to_datetime(pd.to_datetime(cat_df['datetime']).dt.date)
    cat_df['outcome_year_month'] = pd.to_datetime(cat_df['outcome_year'].astype(str) + '-' + cat_df['outcome_month'].astype(str))
    # rename columns
    cat_df.rename(columns={'datetime': 'outcome_datetime', 'Cat/Kitten (outcome)': 'kitten_outcome',
                           'Spay/Neuter': 'sterilized_outcome', 'Periods': 'periods',
                           'Period Range': 'period_range', 'color1': 'main_color'}, inplace=True)
    cat_df.kitten_outcome = cat_df.kitten_outcome.astype(str).astype(int)
    cat_df.sterilized_outcome = cat_df.sterilized_outcome.astype(str).astype(int)
    cat_df.cfa_breed = cat_df.cfa_breed.astype(str).astype(int)
    cat_df.domestic_breed = cat_df.domestic_breed.astype(str).astype(int)
    cat_df.has_name = cat_df.has_name.astype(str).astype(int)
    cat_df.adopted_or_not = cat_df.adopted_or_not.astype(str).astype(int)
    cat_df.sex = cat_df.sex.astype(str).astype(int)
    return cat_df

def clean_intake_dataset(intake_df, animal_type):
    if animal_type == 'cats':
        intake_df = intake_df[intake_df['Animal Type'] == 'Cat']
    intake_df.drop(columns='Animal Type', inplace = True)
    intake_df.rename(columns={'Animal ID': 'animal_id', 'Name': 'name',
                           'DateTime': 'intake_datetime', 'MonthYear': 'intake_month_year',
                           'Found Location': 'found_location', 'Intake Type': 'intake_type',
                           'Intake Condition': 'intake_condition', 'Sex upon Intake': 'sex_upon_intake',
                           'Age upon Intake': 'age_upon_intake', 'Breed': 'breed', 'Color': 'color'}, inplace=True)
    intake_df.drop(columns='name', inplace = True)
    # get intake_age_days
    intake_df['n_age'] = [int(x.split()[0]) for x in intake_df.age_upon_intake]
    intake_df['month_week_year'] = [x.split()[1] for x in intake_df.age_upon_intake]
    intake_df['month_week_year'] = intake_df['month_week_year'].apply(utils.get_n_days)
    intake_df['intake_age_days'] = intake_df['n_age'] * intake_df['month_week_year']
    intake_df.drop(columns=['age_upon_intake', 'n_age', 'month_week_year'], inplace=True)
    # handle intake_datetime
    intake_df['intake_datetime'] = pd.to_datetime(pd.to_datetime(intake_df['intake_datetime']).dt.date)
    # split sex_upon_intake
    intake_df.sex_upon_intake = intake_df.sex_upon_intake.replace('Unknown', 'Unknown Unknown')
    intake_df['sterilized_intake'] = [x.split()[0] for x in intake_df.sex_upon_intake]
    intake_df['sterilized_intake'] = intake_df['sterilized_intake'].apply(lambda x: 0 if (x == 'Intact') else 1)
    intake_df.drop(columns=['sex_upon_intake', 'breed', 'color'], inplace = True)
    intake_df.drop_duplicates(inplace=True)
    return intake_df

def get_clean_cat_dataset(dataset):
    cat_df = load_csv(dataset)
    cat_df = clean_cat_dataset(cat_df)
    return cat_df

def get_clean_intake_dataset(dataset, animal_type):
    intake_df = load_csv(dataset)
    intake_df = clean_intake_dataset(intake_df, animal_type)
    return intake_df

def merge_intakes_outcomes():
    outcomes = get_clean_cat_dataset('cats')
    intakes = get_clean_intake_dataset('intakes', 'cats')
    merged_df = outcomes.merge(intakes, how='left', on='animal_id')
    merged_df.dropna(inplace=True)
    merged_df['days_spent_at_shelter'] = (merged_df['outcome_datetime'] - merged_df['intake_datetime']).dt.days
    merged_df['age_diff_days'] = (merged_df['outcome_age_(days)'] - merged_df['intake_age_days'])
    merged_df = merged_df[merged_df['days_spent_at_shelter'] >= 0]
    merged_df.drop(columns=['coat', 'color', 'breed', 'main_color'], inplace=True)
    merged_df['found_location'] = utils.format_address(merged_df['found_location'])
    return merged_df

def get_lat_lon_from_address(address):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}'
    response = requests.get(url)
    location = response.json()
    if location['status'] == 'OK':
        lat, lon = location['results'][0]['geometry']['location']['lat'], location['results'][0]['geometry']['location']['lng']
    else:
        lat, lon = 0, 0
    return lat, lon

def get_X_y():
    cat_df = merge_intakes_outcomes()
    features_df = cat_df[['top_breeds', 'top_coats', 'kitten_outcome', 'sex', 'sterilized_intake',
                          'sterilized_outcome', 'outcome_age_(days)', 'intake_datetime', 'found_location',
                          'intake_type', 'intake_condition', 'intake_age_(days)', 
                          'cfa_breed', 'domestic_breed', 'coat_pattern', 'has_name']]

    target = cat_df['adopted_or_not'].astype(str).astype(float)
    top_breeds_encoded = encode_feature(features_df, 'top_breeds')
    coat_pattern_encoded = encode_feature(features_df, 'coat_pattern')
    coat_encoded = encode_feature(features_df, 'top_coats')
    features_df = pd.concat([features_df, top_breeds_encoded, coat_pattern_encoded, coat_encoded], axis=1)
    features_df.drop(columns=['top_breeds', 'coat_pattern', 'top_coats'], inplace = True)
    return features_df, target

def encode_feature(df, feature_name):
    enc = OneHotEncoder(sparse = False)
    enc.fit(df[[feature_name]])
    feature_encoded = pd.DataFrame(enc.transform(df[[feature_name]]), columns=enc.get_feature_names())
    return feature_encoded

def get_prediction_outcome():
    pass
