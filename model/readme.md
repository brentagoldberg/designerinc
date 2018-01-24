# Model
Folder contains model tuning and model output information

## Files

### Run_model notebook

This is where the magic is.

Downloads the data into a pandas DataFrame, runs transform_df.py (pipeline), then runs predict_style_model.py.

This is where the models live rather than 300-600MB pickle files each for the 12 different models. Metrics are stored in this object as well.

Includes scirpts to add prediction columns to the dataframe. Used for initial testing of clustering for recommender system.

### Style Category Classifier notebook

Notebook used to find the best classifier and test the effectiveness of features.
Outputs from these model tests are stored in "model_tuning_data/" there are 18 model iteration data stored here.

### predict_style_model.py

This file outputs the 12 models in one dictionary within the class object. 

Also has functions to print out (and saves) metrics, graphs, and feature importance data as the model is being built.

Includes natural language processing and and random forest classifier calls.

Includes filtering for labeled data and train-test-split for model creation ### shall deprecate to use oob

### transform_df.py (aka pipeline)

This file transforms the basic pandas DataFrame download to one the model uses.
