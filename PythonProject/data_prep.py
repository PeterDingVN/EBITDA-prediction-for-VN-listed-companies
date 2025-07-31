import pandas as pd
import re

def prep_data(df_path):
    # Load the  raw data from Finpro
    df = pd.read_excel(df_path,
                       # sheet_name is optional
                       sheet_name='data')

    '''
    Example of df_path:
    "C:\\Users\\HP\\Downloads\\FiinProX_DE_Doanh_nghiep_20250721.xlsx"
    '''

    # Process
    # Unpivot table
    df_unpivot = df.melt(id_vars = ['STT', 'Mã', 'Tên công ty', 'Sàn'], value_vars=df.columns[4:])

    # Add year cols
    df_unpivot['Year'] = df_unpivot['variable'].apply(
        lambda x: re.search(r'\d{4}', x).group()
    )
    df_unpivot['Year'] = pd.to_numeric(df_unpivot['Year'], errors='coerce')

    # drop unnecessary cols
    df_unpivot.drop(columns=['STT', 'Tên công ty'], inplace=True)

    # clean variables column by adding 'vars_mini' column
    df_unpivot['vars_mini'] = df_unpivot['variable'].apply(
        lambda x: x.split('\n')[0]
    )
    df_unpivot['vars_mini'] = df_unpivot['vars_mini'].apply(
        lambda x: re.sub(r'\d+\.', '', x)
    )
    df_unpivot['vars_mini'] = df_unpivot['vars_mini'].apply(
        lambda x: x.strip()
    )
    # drop 'variable' column
    df_unpivot.drop(columns = 'variable', inplace=True)

    # pivot columns based on vars_mini
    df_unpivot = df_unpivot.pivot(
        index=['Mã', 'Sàn', 'Year'], columns='vars_mini', values='value'
    ).reset_index()

    # columns rename and reposition
    df_unpivot = df_unpivot.rename(columns={
        'Mã': 'company',
        'Sàn': 'platform',
        'Year': 'year',

        'EBITDA': 'ebitda',

        'Doanh thu thuần': 'revenue',

        'Giá vốn hàng bán': 'cogs',
        'Chi phí bán hàng': 'sales_cost',
        'Chi phí quản lý doanh  nghiệp': 'admin_cost',

        'Lợi nhuận thuần từ hoạt động kinh doanh': 'net_op_profit',

        'Các khoản phải thu ngắn hạn': 'short_receive',
        'Hàng tồn kho, ròng': 'in_stock',
        'Giá trị ròng tài sản đầu tư': 'invest_nav',
        'Phải thu dài hạn': 'long_receive',
        'Nợ dài hạn': 'long_liability',
        'Nợ ngắn hạn': 'short_liability',
        'Tiền và tương đương tiền': 'cash',
        'Tài sản cố định': 'fixed_asset',
        'Tài sản dài hạn khác': 'other_long_asset',
        'Tài sản dở dang dài hạn': 'cwip',
        'Tài sản ngắn hạn khác': 'other_short_asset',
        'Đầu tư dài hạn': 'long_invest',

        'Vốn và các quỹ': 'equity_fund',
        'Nguồn kinh phí và quỹ khác': 'other_fund',

        'Tỷ lệ sở hữu nhà nước': 'gov_own',
        'Tỷ lệ sở hữu nước ngoài': 'for_own'

    })

    df_final = df_unpivot[['company','platform','year','ebitda','revenue','cogs','sales_cost','admin_cost','net_op_profit',
        'short_receive','in_stock','invest_nav','long_receive','long_liability','short_liability','cash','fixed_asset',
        'other_long_asset','cwip','other_short_asset','long_invest','equity_fund','other_fund','gov_own','for_own'
    ]]

    return df_final

def save_file(df_, name):
    # Save as raw data
    df_.to_csv(f"{name}.csv", index=False)



