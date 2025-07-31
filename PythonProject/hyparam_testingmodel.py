from sklearn.ensemble import RandomForestRegressor as rf
from sklearn.svm import SVR as svr
from xgboost import XGBRegressor as xgb
from sklearn.metrics import r2_score as r2, root_mean_squared_error as rmse, mean_absolute_percentage_error as mape, \
    make_scorer

# Scoring criteria
scoring_criteria = {
    'r2': make_scorer(r2),
    'mape': make_scorer(mape),
    'rmse': make_scorer(rmse)
}

# # Random forest
# param_rf = {
#     'n_estimators': [100, 200, 300, 400],# 150, 200, 300],
#     'max_depth': [None, 5, 10, 15],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 5, 10]
# }

# XGBoost
param_xg = {
    'n_estimators': [100, 200, 300], #, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth' : [2, 5, 8],
    'subsample' : [0.5]
}

# # SVR
# param_svr = {
#     'kernel': ['rbf', 'poly'],
#     'C': [1, 5] #, 10, 20]
# }

# Regressor
regressors = {
    # 'Randome_forest' : (rf(), param_rf),
    # 'SVR' : (svr(), param_svr),
    'XGBoost' : (xgb(), param_xg)
}

