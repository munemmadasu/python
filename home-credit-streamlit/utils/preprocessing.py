import numpy as np
def clean_data(df):
    #Fix employment anomaly
    df["DAYS_EMPLOYED"]=df["DAYS_EMPLOYED"].replace(
        365243,
        np.nan
    )
    return df

#from utils.preprocessing import clean_data