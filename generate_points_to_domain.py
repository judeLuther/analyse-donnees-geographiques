#!/usr/bin/env python
# Function to generate a DataFrame by merging point_df and phenomenon_df 
# based on department and domain_id columns
def generate_points_domain_id_dataframe(point_df, phenomenon_df):

    # Merge the DataFrames based on the department and domain_id columns
    merged_df = point_df.merge(phenomenon_df, how='left', left_on='department', right_on='domain_id')

    return merged_df

