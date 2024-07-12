#!/usr/bin/env python
import time
import os
import requests
import pandas as pd
from service_json import get_coordinates_points_from_internet
from url import url_points, url_departement, url_alertes, url_contours_geojson, url_departement_de_france
from service_csv import get_data_csv_from_internet
from service_phenomenon import get_echeance_items_data_from_internet
from generate_points_to_domain import generate_points_domain_id_dataframe
from join_points_to_departement import join_points_to_department
from maps import create_interative_map
from generate_coordinates import generate_coordinates, find_genereted_coordinates_departement
from utils import phenomenon_mapping

def afficher_menu():
    print("=== MENU ===")
    print("1. Simuler des points géographiques et gérérer les cartes intéractives J et J+1")
    print("2. Générer les datasets departement-alertes et les cartes intéractives alertes jour J et J+1")
    print("3. Quitter")
    print()

def executer_option(option):
    #get data coordonates Latitude and Longitude
    points = get_coordinates_points_from_internet(url_points)

    #get departement codgeo; libgeo; reg
    dep_df = get_data_csv_from_internet(url_departement)

    #get alertes data for period J and J+1(les données d'alerte pour la date du 2023-06-15 14:02:33)
    phenomenon_df_j, phenomenon_df_j1 = get_echeance_items_data_from_internet(url_alertes)

    #Join points from internet to departement
    new_dataframe = join_points_to_department(points, dep_df)

    #Retrieve the JSON in GeoJSON format for contours
    response = requests.get(url_contours_geojson)
    france_data = response.json()

    #Simulate geographic points and generate interactive maps for Period J and Period J+1.
    if option == 1:
        ##Request to enter the number of points to generate."
        num_points = input("Please enter a number of points: ")

        ## Generating N geographic points."
        coordinates = generate_coordinates(int(num_points))

        ## Creating the DataFrame containing the geographic points.
        df = pd.DataFrame(coordinates, columns=['Longitude', 'Latitude'])
        
        ## For each point, find its department.
        new_df = find_genereted_coordinates_departement(url_departement_de_france, df)

        ## Removing points that are not located within a department.
        new_df = new_df.dropna(subset=['department'])
        
        ## Handling the J period.

        ###create a data frame, which contains the points generated, then the following columns 
        ###which will specify the level of alert for the different “phenomenon id” for period J.
        df_points_domain=generate_points_domain_id_dataframe(new_df, phenomenon_df_j)

        ### Add the "phenomenon" column based on the mapping to df_points_domain
        df_points_domain['phenomenon'] = df_points_domain['phenomenon_id'].map(phenomenon_mapping)

        ###Save df_points_domain to csv
        save_file(folder_name="datasets" ,filename="genereted_points_alertes_jour_J.csv", df=df_points_domain)
        
        ###Create map for jour J
        create_interative_map(france_data, df_points_domain, j="GJ")

        ##Handling the J+1 period
       
        ###create a data frame, which contains the points generated, then the following columns 
        ##which will specify the level of alert for the different “phenomenon id” for period J+1.
        df_points_domain=generate_points_domain_id_dataframe(new_df, phenomenon_df_j1)

        ### Add the "phenomenon" column based on the mapping to df_points_domain
        df_points_domain['phenomenon'] = df_points_domain['phenomenon_id'].map(phenomenon_mapping)

        ###Save csv file
        save_file(folder_name="datasets" ,filename="genereted_points_alertes_jour_J_1.csv", df=df_points_domain)
    
        ###Create map for jour J
        create_interative_map(france_data, df_points_domain, j="GJ1")

    #Generate the department-alerts datasets and the interactive maps for alerts for J and J+1 periods.
    if option == 2:

        ## Handling the J period
        ### create a data frame, which contains the points, then the following columns 
        ### which will specify the level of alert for the different “phenomenon id” for period J.
        df_points_domain=generate_points_domain_id_dataframe(new_dataframe, phenomenon_df_j)

        ###save dataframe df_points_domain to csv
        save_file(folder_name="datasets" ,filename='france_alertes_jour_j.csv', df=df_points_domain)

        ###create map for period J
        create_interative_map(france_data, df_points_domain)

        ###create a data frame, which contains the points, then the following columns 
        ###which will specify the level of alert for the different “phenomenon id” for period J+1.
        df_points_domain=generate_points_domain_id_dataframe(new_dataframe, phenomenon_df_j1)

        ###save df_points_domain to csv
        save_file(folder_name="datasets" ,filename='france_alertes_jour_j_1.csv', df=df_points_domain)
        
        ###create map for period J+1
        create_interative_map(france_data, df_points_domain, j="")
        

def menu():
    quitter = False

    while not quitter:
        afficher_menu()
        choix = input("Sélectionnez une option : ")

        try:
            option = int(choix)
            executer_option(option)

            if option == 3:
                quitter = True
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre.")


#This function create the file in the current repository folder_name.
def save_file(filename, folder_name, df):
    # Get the current directory
    current_dir = os.getcwd()

    # Create the complete file path
    folder_path = os.path.join(current_dir, folder_name)

    #This code checks if the folder already exists. If not, it creates
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    csv_file_path = os.path.join(folder_path, filename)

    #Save dataframe
    df.to_csv(csv_file_path, index=False, sep=";", encoding="utf-8")