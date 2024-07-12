#!/usr/bin/env python
import requests
import pandas as pd
import numpy as np

#This function does one thing, returns the periods (J and J+1)
def get_echeance_items_data_from_internet(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Initialize NumPy arrays with specific data types to store the data
        dtype = np.dtype([
            ('domain_id', object),
            ('max_color_id', 'int64'),
            ('phenomenon_id', 'int64'),
            ('phenomenon_max_color_id', 'int64')
        ])
        df_array_j = np.empty(0, dtype=dtype)
        df_array_j1 = np.empty(0, dtype=dtype)

        # Loop through each element in the "periods" list
        for period in data["product"]["periods"]:
            echeance = period["echeance"]
            domain_ids = period["timelaps"]["domain_ids"]

            for domain in domain_ids:
                domain_id = domain["domain_id"]
                max_color_id = domain["max_color_id"]
                phenomenon_items = domain["phenomenon_items"]

                # Create an array of the same length as phenomenon_items for domain_id
                domain_id_arr = np.full(len(phenomenon_items), domain_id, dtype=object)

                # Extract the values for other columns from phenomenon_items
                phenomenon_ids = np.array([item["phenomenon_id"] for item in phenomenon_items], dtype='int64')
                phenomenon_max_color_ids = np.array([item["phenomenon_max_color_id"] for item in phenomenon_items], dtype='int64')

                # Create the rows as structured arrays
                rows = np.array(list(zip(domain_id_arr, np.full(len(phenomenon_items), max_color_id), phenomenon_ids, phenomenon_max_color_ids)), dtype=dtype)

                if echeance == "J":
                    df_array_j = np.concatenate((df_array_j, rows))
                elif echeance == "J1":
                    df_array_j1 = np.concatenate((df_array_j1, rows))

        # Create the DataFrames from the NumPy arrays
        df_j = pd.DataFrame(df_array_j)
        df_j1 = pd.DataFrame(df_array_j1)

        return  df_j, df_j1

    else:
        print("Error: Failed to retrieve data from the URL.")
        return []