#!/usr/bin/env python
import requests
import pandas as pd
import io

#Function to retrieve CSV data from the internet and create a DataFrame
def get_data_csv_from_internet(url):

    # Send an HTTP GET request to the URL and fetch the CSV data
    response = requests.get(url)
    csv_data = response.text

    # Create a DataFrame from the CSV data
    return pd.read_csv(io.StringIO(csv_data), delimiter=';')