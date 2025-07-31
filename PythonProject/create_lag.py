def create_lag(df, id_col, time_col, cols, lag_num):
    import pandas as pd
    all_group = []

    # step 1: chunk data into group
    for id, grp in df.groupby(id_col):

        # step 2: sort ascending
        grp_lag = grp.sort_values(by=time_col, ascending=True)

        # step 3: do shifting for specified features/target_var
        for col in cols:
            for lag in range(1, lag_num+1):
                grp_lag[f'{col}_lag_{lag}'] = grp_lag[col].shift(lag)

        # step 4: drop all NaN
        grp_lag = grp_lag.dropna()

        # step 5: append into all_group
        all_group.append(grp_lag)

    result_tb = pd.concat(all_group, axis=0).sort_values(by=[id_col, time_col])

    return result_tb



