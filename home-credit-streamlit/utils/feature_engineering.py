import numpy as np

def create_features(df):
    #Age
    df["AGE"]=abs(df["DAYS_BIRTH"])/365
    #Employement years
    df["EMPLOYMENT_YEARS"]=abs(df["DAYS_EMPLOYED"])/365
    #Credit Income Ratio
    df["CREDIT_INCOME_RATIO"]=(df["AMT_CREDIT"]/df["AMT_INCOME_TOTAL"])
      # Annuity Income Ratio
    df["ANNUITY_INCOME_RATIO"] = (df["AMT_ANNUITY"]/df["AMT_INCOME_TOTAL"])
    # Credit Goods Ratio
    df["CREDIT_GOODS_RATIO"] = (df["AMT_CREDIT"]/df["AMT_GOODS_PRICE"])
    # Average External Score
    df["AVG_EXT_SCORE"] = df[
        [
            "EXT_SOURCE_1",
            "EXT_SOURCE_2",
            "EXT_SOURCE_3"
        ]
    ].mean(axis=1)

    return df

#from utils.feauters import create_feautres