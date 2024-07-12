#!/usr/bin/env python
import folium
import os
import numpy as np

def create_interative_map(france_data, df_points_alertes, j="J"):

    # Créer une carte centrée de la France
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    """Ajouter le Choropleth à la carte
    Pour relier ces informations (df) à la carte, toujours dans la fonction Choropleth(), 
    nous devons définir les éléments suivants :
    geo_data : les contours au format GeoJSON ;
    key_on : l'item dans le GeoJSON avec lequel nous ferons la jointure ;
    data : le DataFrame dans lequel nous avons les informations statistiques ;
    columns : les deux colonnes à prendre:
        1. clé de jointure(department)
        2. mesure statistique(max_color_id)
    fill_color : la palette de couleurs à utiliser (provenant de Color Brewer) """
    
    folium.Choropleth(
    geo_data=france_data,
    name='choropleth',
    data=df_points_alertes,
    columns=['department', 'max_color_id'],
    key_on='feature.properties.dep',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Legend'
    ).add_to(m)

    """ Définir la couleur en fonction de la valeur de max_color_id de l'alerte dans le DataFrame
    • "1" : vert
    • "2" : jaune
    • "3" : orange
    • "4" : rouge """
    style_function = lambda x: {
    'fillColor': 'green' if int(x['properties']['max_color_id']) == 1 \
          else 'yellow' if int(x['properties']['max_color_id']) == 2 \
            else 'orange' if int(x['properties']['max_color_id']) == 3 \
                else 'orange' if int(x['properties']['max_color_id']) == 4 \
                else 'green',
    'color': 'black',
    'weight': 1,
    'fillOpacity': 0.7
    }

    # Ajouter les contours des communes à la carte avec la couleur définie
    for feature in france_data['features']:
        dep = feature['properties']['dep']
        libgeo = feature['properties']['libgeo']
        for value in df_points_alertes['domain_id'].values:
            if dep == value:
                df_filtered = df_points_alertes[df_points_alertes['domain_id'] == dep]
                color_id = df_filtered['max_color_id'].iloc[0]
                feature['properties']['max_color_id'] = int(color_id)
                popup_text = f"Department: {dep}<br>Location: {libgeo}"
                break
            else:
                popup_text = f"Department: <br>Location: "
                feature['properties']['max_color_id'] = "0"
        geojson = folium.GeoJson(feature, style_function=style_function)
        folium.Popup(popup_text).add_to(geojson)
        geojson.add_to(m)

    # Ajouter la légende
    folium.LayerControl().add_to(m)

    
    folder_name = "interactive_maps"

    current_directory = os.getcwd()

    folder_path = os.path.join(current_directory, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Sauvegarder la carte en format html dans le dossier interactive_maps
    if j=="J":
        file_path = os.path.join(folder_path, 'map_jour_j.html')
        m.save(file_path)
    elif j=="GJ":
        file_path = os.path.join(folder_path, 'map_of_genereted_points_jour_j.html')
        m.save(file_path)
    elif j=="GJ1":
        file_path = os.path.join(folder_path, 'map_of_genereted_points_jour_j_1.html')
        m.save(file_path)
    else:
        file_path = os.path.join(folder_path, 'map_jour_j_1.html')
        m.save(file_path)