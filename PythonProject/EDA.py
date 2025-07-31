def quartile_table(df, col):
    import pandas as pd
    df_inuse = df.copy()
    # data distribution
    q1 = df_inuse[col].quantile(0.25)
    q1_num = len(df_inuse[col][df_inuse[col] <= q1])

    q2 = df_inuse[col].quantile(0.5)
    q2_num = len(df_inuse[col][(df_inuse[col] < q2) & (df_inuse[col] > q1)])

    q3 = df_inuse[col].quantile(0.75)
    q3_num = len(df_inuse[col][(df_inuse[col] < q3) & (df_inuse[col] > q2)])

    q4_num = len(df_inuse[col][df_inuse[col] > q3])

    sum_tab = pd.DataFrame(data=[['q1', q1_num], ['q2', q2_num], ['q3', q3_num], ['q4', q4_num]],
                           columns=['Quartile range', 'Num obs'])

    return sum_tab

def multicolin(df):
    import pandas as pd
    from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
    exog_vars = df.select_dtypes(include='number').columns

    # Set up VIF method
    vif_data = pd.DataFrame()
    vif_data['features'] = exog_vars

    # Vif calculation
    vif_data['VIF'] = [vif(df[exog_vars].values, i)
                          for i in range(len(exog_vars))]

    return vif_data

def hetereo(df, endog, num_drop=None):
    import pandas as pd
    import statsmodels.formula.api as smf
    from statsmodels.compat import lzip
    import statsmodels.stats.api as sms

    # data setup
    df_used = df.copy()
    df_used = df_used.drop(columns=[num_drop])
    df_input = df_used.select_dtypes(include='number').columns
    exog_col = df_input.drop(endog)

    # Fit into model
    fitted_linear = smf.ols(f'{endog}~{'+'.join(exog_col)}', data=df_used[df_input]).fit()

    # Conduct the Breusch-Pagan test
    names = ['Lagrange multiplier statistic', 'p-value',
             'f-value', 'f p-value']
    test_result = sms.het_breuschpagan(fitted_linear.resid, fitted_linear.model.exog)

    return lzip(names, test_result)





