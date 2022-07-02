import pandas as pd
from AAC_challenge import utils

def load_csv(dataset):
    if dataset == 'cats':
        cat_df = pd.read_csv("../raw_data/aac_data/aac_shelter_cat_outcome_eng.csv")
        return cat_df
    elif dataset == 'all':
        all_df = pd.read_csv("../raw_data/aac_data/aac_shelter_outcomes.csv")
        return all_df

def clean_cat_dataset(cat_df):
    # drop some columns
    cat_df.drop(columns=['count', 'breed2', 'color2', 'monthyear', 'sex_upon_outcome',
                         'age_upon_outcome', 'Cat/Kitten (outcome)', 'sex_age_outcome',
                         'age_group', 'dob_year', 'dob_month', 'dob_monthyear', 'breed1',
                         'outcome_hour'], inplace = True)
    # replace double brown coat
    cat_df.coat.replace('brown ', 'brown', inplace = True)
    # drop rows where outcome is NaN
    rows_to_drop = cat_df[cat_df.outcome_type.isna()]['outcome_type'].index
    cat_df.drop(index=rows_to_drop, inplace = True)
    # drop duplicates
    cat_df = cat_df.drop_duplicates(inplace=False).reset_index()
    # map yes/no to 0 1
    cat_df.cfa_breed = cat_df.cfa_breed.apply(lambda x: 0 if (x == False) else 1)
    cat_df.domestic_breed = cat_df.domestic_breed.apply(lambda x: 0 if (x == False) else 1)
    cat_df['Spay/Neuter'] = cat_df['Spay/Neuter'].apply(lambda x: 0 if (x == 'No') else 1)
    # get has_name column then drop name column
    cat_df['has_name'] = utils.get_has_name(cat_df)
    cat_df.drop(columns='name', inplace = True)
    # get adopted or not
    cat_df['adopted_or_not'] = cat_df.outcome_type.apply(utils.get_adopted_or_not)
    cat_df.drop(columns='outcome_subtype', inplace = True)
    # imputing missing values with most frequent
    cat_df = utils.impute_most_frequent(cat_df)
    cat_df.drop(columns=['index', 'animal_id', 'animal_type'], inplace = True)
    # handle datetime columns
    cat_df['date_of_birth'] = pd.to_datetime(cat_df['date_of_birth'])
    cat_df['datetime'] = pd.to_datetime(cat_df['datetime']).dt.date
    cat_df['outcome_year_month'] = pd.to_datetime(cat_df['outcome_year'].astype(str) + '-' + cat_df['outcome_month'].astype(str))
    # rename columns
    cat_df.rename(columns={'datetime': 'outcome_datetime', 'Spay/Neuter': 'sterilized', 'Periods': 'periods',
                       'Period Range': 'period_range', 'color1': 'main_color'}, inplace=True)
    return cat_df

def get_clean_cat_dataset(dataset):
    cat_df = load_csv(dataset)
    cat_df = clean_cat_dataset(cat_df)
    return cat_df
