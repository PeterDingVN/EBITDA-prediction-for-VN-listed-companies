import pandas as pd
from panelsplit.cross_validation import PanelSplit
from sklearn.model_selection import GridSearchCV
import hyparam_testingmodel as hyper_param
import hyperparam_main as hyper_mainpar

class TrainTestPipe:
    def __init__(self, data):
        self.data = data

    def holdout_and_split(self, panel_col, level):
        data_used = self.data.copy()
        data_used = data_used.set_index(panel_col)
        rate = 3

        # Unique idx
        get_index = data_used.index.get_level_values(level).unique()
        idx_holdout = int(max(get_index))
        idx_val = sorted(get_index, reverse=True)[:rate]

        # Hold out set
        df_holdout = data_used[data_used.index.get_level_values(level) == idx_holdout]
        df_input = data_used[data_used.index.get_level_values(level) != idx_holdout]

        # Train val split
        X_train = df_input[~df_input.index.get_level_values(level).isin(idx_val)].drop(columns='ebitda')
        y_train = df_input['ebitda'][~df_input.index.get_level_values(level).isin(idx_val)]
        X_val = df_input[df_input.index.get_level_values(level).isin(idx_val)].drop(columns='ebitda')
        y_val = df_input['ebitda'][df_input.index.get_level_values(level).isin(idx_val)]

        return df_input, df_holdout, X_train, X_val, y_train, y_val

    def hyper_parameter_tuning(self, n_splits, test_size, test: bool = True):
        if test:
            # input data
            df_input = self.holdout_and_split(panel_col=['company', 'year'],
                                              level=1)[0]
            X_input = df_input.drop(columns='ebitda')
            y_input = df_input['ebitda']

            # Cross-validation method
            periods = df_input.index.get_level_values(level=1)
            cv_strat = PanelSplit(periods = periods, n_splits = n_splits, test_size = test_size)

            # Cross-val process
            # Scoring criteria
            scorer_criteria = hyper_param.scoring_criteria

            # Pipeline for cross_val
            result_final = []

            for name, (algo, hy_param) in hyper_param.regressors.items():
                print(f'Processing {name}: ...')
                grid_search = GridSearchCV(algo,
                                           param_grid=hy_param,
                                           scoring = scorer_criteria,
                                           cv=cv_strat,
                                           refit = 'r2')
                grid_fit = grid_search.fit(X_input, y_input)

                # Get the evaluation score for each hyper_param
                results = grid_fit.cv_results_
                results = pd.DataFrame(results)
                results['algo_used'] = f'{name}'
                result_final.append(results[['algo_used', 'params', 'mean_test_r2', 'mean_test_mape', 'mean_test_rmse']])

            # Result summary
            eval_output = pd.concat(result_final, ignore_index=True)
            eval_output.sort_values(by=['mean_test_r2', 'mean_test_rmse', 'mean_test_mape'],
                                    ascending=False,
                                    inplace=True)
        else:
            # input data
            df_input = self.holdout_and_split(panel_col=['company', 'year'],
                                              level=1)[0]
            X_input = df_input.drop(columns='ebitda')
            y_input = df_input['ebitda']

            # Cross-validation method
            periods = df_input.index.get_level_values(level=1)
            cv_strat = PanelSplit(periods=periods, n_splits=n_splits, test_size=test_size)

            # Cross-val process
            # Scoring criteria
            scorer_criteria = hyper_mainpar.scoring_criteria

            # Pipeline for cross_val
            result_final = []

            for name, (algo, hy_param) in hyper_mainpar.regressors.items():
                print(f'Processing {name}: ...')
                grid_search = GridSearchCV(algo,
                                           param_grid=hy_param,
                                           scoring=scorer_criteria,
                                           cv=cv_strat,
                                           refit='r2')
                grid_fit = grid_search.fit(X_input, y_input)

                # Get the evaluation score for each hyper_param
                results = grid_fit.cv_results_
                results = pd.DataFrame(results)
                results['algo_used'] = f'{name}'
                result_final.append(
                    results[['algo_used', 'params', 'mean_test_r2', 'mean_test_mape', 'mean_test_rmse']])

            # Result summary
            eval_output = pd.concat(result_final, ignore_index=True)
            eval_output.sort_values(by=['mean_test_r2', 'mean_test_rmse', 'mean_test_mape'],
                                    ascending=False,
                                    inplace=True)
        return eval_output









