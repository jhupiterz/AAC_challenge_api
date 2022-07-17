from fastapi import FastAPI
import pandas as pd
import pickle
from AAC_challenge import data
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/predict")
def predict(sex, coat_pattern, has_name, breed, coat, intake_type, intake_condition,
            intake_age_days, sterilized_intake, days_spent_at_shelter, lat, lon):
    intake_age_days = int(float(intake_age_days))
    days_spent_at_shelter = int(float(days_spent_at_shelter))
    lat = float(lat)
    lon = float(lon)
    # encode male/female
    if sex == 'male':
        sex = 0
    elif sex == 'female':
        sex = 1
    # generate encoded coat_pattern df
    coat_patterns = [0,0,0,0,0,0,0,0,0]
    coat_pattern_df = pd.DataFrame([coat_patterns], columns = ['agouti', 'brindle', 'calico',
                                                             'point', 'smoke', 'tabby',
                                                             'torbie', 'tortie', 'tricolor'])
    coat_pattern_df[coat_pattern] = 1
    # encode has_name
    if has_name == 'yes':
        has_name = 1
    elif has_name == 'no':
        has_name = 0
    # generate encoded breed_df
    breeds = [0,0,0,0,0,0]
    breed_df = pd.DataFrame([breeds], columns = ['american shorthair', 'domestic longhair',
                                                'domestic mediumhair', 'domestic shorthair',
                                                'other', 'siamese'])
    breed_df[breed] = 1
    # generate encoded coat_df
    coats = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    coat_df = pd.DataFrame([coats], columns = ['black', 'blue', 'brown', 'calico', 'cream', 'flame', 'gray', 'lynx',
                                              'orange', 'other', 'seal', 'silver', 'torbie', 'tortie', 'white'])
    coat_df[coat] = 1
    # generate encoded intake_type_df
    intake_types = [0,0,0,0]
    intake_type_df = pd.DataFrame([intake_types], columns = ['euthanasia request', 'owner surrender', 'public assist', 'stray'])
    intake_type_df[intake_type] = 1
    # generate encoded intake_condition_df
    intake_conditions = [0,0,0,0,0,0,0,0]
    intake_condition_df = pd.DataFrame([intake_conditions], columns = ['aged', 'feral', 'injured', 'normal', 'nursing', 'other', 'pregnant', 'sick'])
    intake_condition_df[intake_condition] = 1
    # encode sterilized intake
    if sterilized_intake == 'yes':
        sterilized_intake = 1
    elif sterilized_intake == 'no':
        sterilized_intake = 0
    X = pd.DataFrame([sex], columns = ['sex'])
    X['has_name'] = [has_name]
    X['intake_age_days'] = [intake_age_days]
    X['sterilized_intake'] = [sterilized_intake]
    X['days_spent_at_shelter'] = [days_spent_at_shelter]
    X['lat'] = [lat]
    X['lon'] = [lon]
    X = pd.concat([X, breed_df, coat_pattern_df, coat_df, intake_type_df, intake_condition_df], axis = 1)

    loaded_model = pickle.load(open('gbc_model.sav', 'rb'))
    pred = int(loaded_model.predict(X)[0])
    proba_0 = loaded_model.predict_proba(X)[0][0]
    proba_1 = loaded_model.predict_proba(X)[0][1]

    return dict(prediction=pred, prob_0=proba_0, prob_1=proba_1)