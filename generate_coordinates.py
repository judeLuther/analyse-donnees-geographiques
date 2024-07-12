#!/usr/bin/env python
import requests
import numpy as np

#Simulate geographic points located in France.
def generate_coordinates(num_points):
    # Limites géographiques de la France métropolitaine
    # min_latitude = 41.333
    # max_latitude = 51.124
    # min_longitude = -5.559
    # max_longitude = 9.662

    #Geographical boundaries of metropolitan France.
    min_latitude = 41.36444102895123
    max_latitude = 51.071251619334184
    min_longitude = -5.097472113430539
    max_longitude =  9.539254917829398

    #Generating random coordinates.
    latitudes = np.random.uniform(min_latitude, max_latitude, num_points)
    longitudes = np.random.uniform(min_longitude, max_longitude, num_points)
    coordinates = np.column_stack((longitudes, latitudes))

    return coordinates

# Function to check if a coordinate is within a departement
def check_coordinate_is_in_a_departement(coordinate, polygon):
    lon, lat = coordinate
    polygon = np.array(polygon[0])
    return np.any((lon >= polygon[:, 0]) & (lat <= polygon[:, 1]))


def find_genereted_coordinates_departement(url, df_coordinates):

    # Make the HTTP GET request
    response = requests.get(url)
    # Parse the JSON response
    data = response.json()

    # Create a list to store the "dep" values for each coordinate in df
    dep_values = []

    # Iterate over each coordinate in df and check if it falls within any polygon
    for _, row in df_coordinates.iterrows():
        coordinate = (row['Longitude'], row['Latitude'])
        dep = None
        for feature in data["features"]:
            polygon = feature['geometry']['coordinates']
            if check_coordinate_is_in_a_departement(coordinate, polygon):
                    dep = feature['properties']['dep']
                    break
        dep_values.append(dep)

    # Create a new DataFrame with coordinates and "department" values
    df_with_dep = df_coordinates.copy()
    df_with_dep['department'] = dep_values

    return df_with_dep