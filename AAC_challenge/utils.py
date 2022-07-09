import pandas as pd
import numpy as np
import json
from sklearn.impute import SimpleImputer

def impute_most_frequent(df):
    columns = df.columns
    imp_most_fq = SimpleImputer(missing_values = np.nan, strategy='most_frequent')
    df = pd.DataFrame(imp_most_fq.fit_transform(df), columns=columns)
    return df

def get_has_name(df):
    names = df.name
    names = names.replace(np.nan, 0)
    names = names.apply(has_name)
    return names

def has_name(x):
    if x != 0:
        return 1
    return x

def get_adopted_or_not(x):
    if x == 'Adoption':
        return 1
    return 0

def map_top_breeds(x):
    if (x == 'domestic shorthair') | (x == 'domestic mediumhair') | (x == 'domestic longhair') | (x == 'siamese') | (x == 'american shorthair'):
        return x
    return 'other'

def map_top_coats(x):
    top_coats = ['black', 'brown', 'blue', 'orange', 'white', 'tortie', 'calico',
                 'torbie', 'cream', 'lynx', 'gray', 'seal', 'flame', 'silver']
    if x in top_coats:
        return x
    return 'other'

def get_n_days(x):
    if 'year' in x:
        return 365
    elif 'month' in x:
        return 30
    elif 'week' in x:
        return 7
    elif 'day' in x:
        return 1

def format_address(address):
    address = [x.replace(' in ', ' ') for x in address]
    address = [x.replace('(', '') for x in address]
    address = [x.replace(')', '') for x in address]
    return address

def read_json_data(json_file):
    with open(json_file, 'r') as myfile:
        data=myfile.read()
    research = json.loads(data)
    return research