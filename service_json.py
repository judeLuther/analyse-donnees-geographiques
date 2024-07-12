#!/usr/bin/env python
import requests
import pandas as pd


def get_coordinates_points_from_internet(url):
    # Make the HTTP GET request
    response = requests.get(url)
    # Parse the JSON response
    data = response.json()

    # Create an empty list to store the features
    features = []

    # Iterate over each feature in the JSON data
    for feature in data["features"]:
        # Extract the required properties (coordinates, region, department)
        coordinates = feature["geometry"]["coordinates"]
        codgeo = feature["properties"]["codgeo"]
        department = feature["properties"]["dep"]
        
        # Create a dictionary with the extracted properties
        feature_dict = {
            "coordinates": coordinates,
            "codgeo": codgeo,
            "department": department
        }
        
        # Add the feature dictionary to the list
        features.append(feature_dict)
    

     # Create an initial dataframe using the given list 'data'
    df = pd.DataFrame(features, columns=['coordinates', 'codgeo', 'department', 'longitude', 'latitude'])

    # Extract the longitude and latitude values from the 'coordinates' list using lambda functions and assign them to the respective columns
    df['longitude'] = df['coordinates'].apply(lambda x: x[0])
    df['latitude'] = df['coordinates'].apply(lambda x: x[1])

    # Drop the 'coordinates' column from the dataframe since we have extracted the longitude and latitude values
    df.drop('coordinates', axis=1, inplace=True)

    return df