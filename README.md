# EBITDA-prediction-for-VN-listed-companies

## Project's goal
Build a forecasting model that forecasts EBITDA of 2691 listed companies in Vietnam.

## Execution
### Data collection
- The input data is taken from FinProX on 2911 companies across 10 years from 2015 to 2024.
- Then, since many values are missing not at random (either because the companies are yet to be listed or they closed down before 2024), they are dropped.
- This led to an unbalanced dataset with poorer forecasting power (since many companies have null values in all 10 years, hence being dropped completely).

### EDA
