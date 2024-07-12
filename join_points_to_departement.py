#!/usr/bin/env python
import pandas as pd

# Function to join points_df to dept_df based on the 'codgeo' and 'department' columns
def join_points_to_department(points_df,dept_df):
    # Merge points_df and dept_df based on the 'codgeo' and 'department' columns
    merged_df = pd.merge(points_df, dept_df[['codgeo', 'libgeo']], left_on='department', right_on='codgeo', how='left')

    # Drop the redundant 'codgeo' column from the merged dataframe
    merged_df.drop('codgeo_y', axis=1, inplace=True)
    merged_df.rename(columns={'codgeo_x': 'codgeo'}, inplace=True)

    return merged_df