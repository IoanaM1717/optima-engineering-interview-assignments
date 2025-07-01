## Introduction

The assignment was completed using the pandas module, reading the csv files as dataframes and joining them in a single dataframe.

The new dataframe then was transformed to join the date and time columns and cast them as a new timestamp column, then filtered the rows to only display the winner of every race.

Then, the columns that were not needed to create the json file were dropped and the dataframe was saved as a dictionary.

Using the json module, the dictionary was saved to a json file for a single year in a separate function, which was then looped for every year available in the data.

## Running the solution

The code was created in a python virtual environment, with a generated requirements.txt file.

To run the code the following commands need to be run:

cd engineering-recruitment-assignments/data-engineering/datapipeline/solution
pip install -r requirements.txt
python main.py
pytest test.py


The code will overwrite the existing json files in the results folder and generate new ones.

The pytest command will run all available unit tests in the test.py file

## Other considerations

The results.csv file contains a number of null values for position and fastestLapTime, which could indicate that the respective drivers did not finish the race.
The nulls could be replaced with a more descriptive value, but those rows were not needed for this particular task.

Also, there are a number of races with no match in the results.csv, which would indicate incomplete data and the correct course of action would be reaching back to the stakeholder or team that provided the data in a live scenario.

Another assupmtion is that the source files would be ovewritten with new files containing updated data. For this solution to work in a live environment, there would need to be an additional function that filters the source data to only read the new lines added.


## Further steps

For deploying to a cloud provider, specifically google cloud the following changes to the code would be needed:
- Uploading the files to google cloud storage
- Using the google cloud python module to read the csv files from GCS
- Change the json creation function to load the json files to a Google Bucket
- Deploy the function using Cloud Function
- Set a schedule for the cloud function to run