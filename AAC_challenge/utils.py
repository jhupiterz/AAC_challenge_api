import pandas as pd
import numpy as np
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