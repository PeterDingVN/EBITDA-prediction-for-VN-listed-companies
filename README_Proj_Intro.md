# EBITDA-prediction-for-VN-listed-companies

## Project's goal
Build a forecasting model that forecasts EBITDA of over 2000 listed companies in Vietnam, based on 19 features, the detail of which is given in this file: all_variables.txt

## Execution
### Data collection
- The input data was taken from FinProX on 2911 companies across 10 years from 2015 to 2024.
- Then, since many values are missing not at random (either because the companies are yet to be listed or they closed down before 2024), they are dropped.
- This led to an unbalanced dataset with poorer forecasting power, however (since many companies have null values in all 10 years, hence being dropped completely). But this result is accpetable because the number of companies, after dropping, is still high (>2000) and most dropped companies are private or otc (over the counter).

### EDA

<img width="1220" height="617" alt="image" src="https://github.com/user-attachments/assets/eeefaa44-fce6-4cd3-95ac-3a1b114851fc" />

The linechart shows a slight upward trend in ebitda among all companies over 10 years. However, there is also high variance in ebitda among companies in each year, shown by the light blue shade around the line, which is very significant.


<img width="272" height="192" alt="image" src="https://github.com/user-attachments/assets/1232dd1a-d759-4dcb-a603-29cb9db29f49" />
<img width="274" height="57" alt="image" src="https://github.com/user-attachments/assets/9ae224ac-bd00-4432-8270-7121a140efbe" />

Correlation-wise, while fixed asset, long_liability, equity_fund, cash, and revenue have positive correlation with ebitda, admin cost and cogs have negative correlation with ebitda.

Further EDA reveals Multi-collinearity and Hetereokedasticity within the data as well. 
Particularly, to test for multi-collinearuty, I used VIF, showing multicollineairty among many features, including fixed_asset, long_liability, short_liability, and equity fund as the features with most serious issues. However, since my model focused more on forecasting than intepreting features, this might not be a concerning problem. 
To test for hetereokedasticity, Breusch_Pagan test was conducted. The p-value returned was 0.0, much lower than 0.05 threshold, indicating hetereokedasticity issue. This issue with different variance could pose a challenge to regression, mostly linear models. Therefore, I intetionally avoid linear models (OLS for example).

### Choosing algorithms
- For the scope of this project, I'll limit my choice to most popular models and algorithms for forecasting problem:

    - Support Vector Regression (SVR):
        + Nonparametric: The algorithm does not assume the distribution of data. (Arnout Van Messem, 2019, https://doi.org/10.1016/bs.host.2019.08.003)
        + Robust to outliers: at its core, SVR works only with "hardest-to-be-classified" data points, not caring about the whole dataset. Since, I did not treat outliers in EDA, this characteristic of SVR proves useful. (A.V.Messem, 2019)
        + More, the algorithm can implicitly transform the data into linear problem (add dimensions) to self-improve without explicit programming. (A.V.Messem, 2019)

    - XGBoost:
        + Nonparametric
        + Support regularization, significantly reduce the need for feature engineering (though it cannot account for cases for adding features with more explanation power, it can account for cases where features are redundant) -> beneficial when domain knowledge is limited
        + Have been used in many panel data science researches (Shenlong Huang and Lingyun Hu, 2024; Reza Sotudeh et al., 2025; Jonathan Fuhr and Dominik Papies, 2024)

    - Random Forest:
        + Nonparametric
        + Random forest train data on multiple subsets of data, each using distinct subset of features, reducing overfitting as a result
        + However, normal RF model often assume independence among observations, violating panel data's structure. (Jianchang Hu and Silke Szymczak, 2023, https://doi.org/10.1093/bib/bbad002)

### Run process
- Cross-validation:
    + I used PanelSplit from 4Freye (here's his git link: https://github.com/4Freye/panelsplit) on 3 algorithms SVR, XGBoost and RFRegressor
    + However, the result is not favorable, because while R-squared, in general, is high (around 80 - 85%), RMSE and MAPE told a different stories. MAPE revolved around 5x10^24 while 
RMSE revolved around 1.10^12. Put this into scale, the maximum value of EBITDA is about 1x10^14, and the min is around -1x10^13. This meant huge error in forecasting.

### Solution
- Outlier drop: dropping all outliers outside IQR. This gives the best result in terms of MAPE and RMSE despite at a small expense of lower r2 (84% -> 77%)
- Scaling: log_transform also improved the data (in order to deal with negative and zero value, the following formula was applied: ```sign(+ or -)*log(|y|+1))```, but yeo-johnson transformation did not
- Add lag: lag for both target var and features that highly correlate with target_var (lag from 1 -> 3); this method also proved effective in improving RMSE, MAPE, though not R2
- Balanced data: balance out the data by dropping all companies that did not report for completely 10 years

### My choice
After, using cross-validation, plus engineering the features based on the four solutions above (I combined lag, scaling and balanced data), I came to final choice:
- Model: XGBoost (n_estmators = 300, learning_rate= 0.05, max_depth=6, subsample=0.5)
- After further testing, the hyper-param above causes overfitting, so new hyper-param was chosen as follwed: n_estimator = 100, max_depth = 3, same learn rate and subsample, to reduce overfitting issue.
- Result:
    + Train set:
      - RMSE: 9,663,491,627.04
      - MAPE: 0.18
      - R2: 0.87

    + Val set:
      - RMSE: 14,585,114,168.59
      - MAPE: 0.24
      - R2: 0.70
 
    + Test set:
      - RMSE: 12,458,954,615.85
      - MAPE: 0.20
      - R2: 0.77

## Limitation of the model
- Data input shortage: since the model returned best result when outliers are dropped based on IQR method, much outlier has been dropped in exchange for better prediction. However, this made the model less powerful in times of outlying or unexpected events that make ebitda abnormally high or low.
- MECE of algorithm: the model only used most commonly applied algorithm instead of trying all available algorithms, risking missing some good algorithms.

