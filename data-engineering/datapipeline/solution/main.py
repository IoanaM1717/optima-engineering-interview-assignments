# Import libraries
import pandas as pd
import json

def export_year_json(df: pd.DataFrame, year: int) -> None:
    """
    Function filters a given dataframe by a given year then outputs it to a json file.
    ---
    Parameters

    df : pd.DataFrame -  dataframe containing race data
    year : int -  year to filter by

    Returns

    None
    """
    year_df = df[df['year'] == year]
    year_df = year_df.drop(columns='year')
    json_data = year_df.to_dict(orient='records')
    filename = f"data-engineering/datapipeline/results/stats_{year}.json"

    try:
        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=4)
    except Exception as e:
        print(f"Error writing file for year {year}: {e}")


def main(source_races_csv: str,source_results_csv: str) -> str: 
    """
    Function reads the source csv files and outputs a json file containing all races in a year, for all available years.
    ---
    Arguments

    source_races_csv : str - path to the races csv file
    source_results_csv : str - path to the results csv file

    Returns

    returns success message on completion or None if an error occurs

    
    """
    try:
        # Create dataframes from csv files
        source_races_df = pd.read_csv(source_races_csv)
        source_results_df = pd.read_csv(source_results_csv)
        # Replace nulls
        source_races_df = source_races_df.fillna('00:00:00')
        # Join source dataframes into a single dataframe
        joined_df = pd.merge(source_races_df,source_results_df, on = 'raceId', how = 'inner')
        # Join date & time columns and convert to timestamp
        joined_df['timestamp'] = pd.to_datetime(joined_df['date'] + ' ' + joined_df['time'])
        joined_df['timestamp'] = joined_df['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S.000')
        # Filter rows - only keep the winner of every race
        filtered_df = joined_df[joined_df['position'] == 1]
        # Filter columns - remove columns not needed for json export
        filtered_df = filtered_df.drop(['date', 'time', 'resultId', 'raceId', 'position'], axis = 1)
        # Sort dataframe
        filtered_df = filtered_df.sort_values(by = ['year', 'round'], ascending = [False, False])
        # Rename columns
        column_mapping = {
            'name' : 'Race Name',
            'round' : 'Race Round',
            'timestamp' : 'Race Datetime',
            'driverId' : 'Race Winning driverId',
            'fastestLapTime': 'Race Fastest Lap'  
        }
        filtered_df = filtered_df.rename(columns=column_mapping)

        # Iterate over available years and export
        for year in filtered_df['year'].unique():
            export_year_json(filtered_df, year)

        return "Files created successfully!"
    
    except Exception as e:
        print(f"Pipeline error: {e}")
        return None

        
# Set csv file path variables
source_races = 'data-engineering/datapipeline/source-data/races.csv'
source_results = 'data-engineering/datapipeline/source-data/results.csv'
# Run the pipeline to create the json files
result = main(source_races,source_results)

print(result)