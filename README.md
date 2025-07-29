# EBITDA-prediction-for-VN-listed-companies

## Project's goal
Build a forecasting model that forecasts EBITDA of 2691 listed companies in Vietnam, based on 19 features, the detail of which is given in ...###########

## Execution
### Data collection
- The input data was taken from FinProX on 2911 companies across 10 years from 2015 to 2024.
- Then, since many values are missing not at random (either because the companies are yet to be listed or they closed down before 2024), they are dropped.
- This led to an unbalanced dataset with poorer forecasting power (since many companies have null values in all 10 years, hence being dropped completely).

### EDA

<img width="1220" height="617" alt="image" src="https://github.com/user-attachments/assets/eeefaa44-fce6-4cd3-95ac-3a1b114851fc" />

The linechart shows a slight upward trend in ebitda among all companies over 10 years. However, there is also high variance in ebitda among companies in each year, shown by the light blue shade around the line, which is very significant.


<img width="272" height="192" alt="image" src="https://github.com/user-attachments/assets/1232dd1a-d759-4dcb-a603-29cb9db29f49" />
<img width="274" height="57" alt="image" src="https://github.com/user-attachments/assets/9ae224ac-bd00-4432-8270-7121a140efbe" />

Correlation-wise, while fixed asset, long_liability, equity_fund, cash, and revenue have positive correlation with ebitda, admin cost and cogs have negative correlation with ebitda.

Further EDA reveals Multi-collinearity and Hetereokedasticity within the data as well. 
Particularly, to test for multi-collinearuty, I used VIF, showing multicollineairty among many features, including fixed_asset, long_liability, short_liability, and equity fund as the features with most serious issues. However, since my model focused more on forecasting than intepreting features, this might not be a concerning problem. 
To test for hetereokedasticity, Breusch_Pagan test was conducted. The p-value returned was 0.0, much lower than 0.05 threshold, indicating hetereokedasticity issue. This issue with different variance could pose a challenge to regression, mostly linear models. Therefore, I intetionally avoid linear models (OLS for example).

### Main model


## Limitation


