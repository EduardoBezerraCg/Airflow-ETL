import pandas as pd


#measuring corr
selected_features = ['Education', 'JoiningYear', 'City', 'PaymentTier', 'Age', 'Gender', 'EverBenched', 'ExperienceInCurrentDomain']
encoded_features = ['Education', 'Gender','EverBenched', 'City']
target = 'LeaveOrNot'



def preprocess(df):
    df = pd.get_dummies(df, columns=encoded_features)
    return df