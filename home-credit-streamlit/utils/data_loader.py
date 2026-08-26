import streamlit as st
import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    # Use the file_path variable to read the CSV
    df = pd.read_csv(file_path)
    return df

   




#from utils.data_loader import load_data