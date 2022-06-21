""""
Mini Example for the pyam transformation see
"""


import pyam
import pandas as pd

def example():
    SIMPLE_DF = pd.DataFrame([
        ['model_a', 'scen_a', 'World', 'Primary Energy', 'EJ/y', 1, 6.],
        ['model_a', 'scen_a', 'World', 'Primary Energy|Coal', 'EJ/y', 0.5, 3],
        ['model_a', 'scen_b', 'World', 'Primary Energy', 'EJ/y', 2, 7],
    ],
        columns=pyam.IAMC_IDX + [2005, 2010],
    )

    print(SIMPLE_DF)
    df_simple = pyam.IamDataFrame(SIMPLE_DF)
    print(df_simple.timeseries())


if __name__ == "__main__":

    # load an example dataframe that was already prepared to fit the need
    # see
    df = pd.read_pickle("VAR_FLO_dev.pickle")
    print(df)
    df = df.groupby(['region', 'variable', 'process', 'commodity', 'unit', 'year',  'model', 'scenario']).sum().reset_index()
    print(df)
    cols = ['variable', 'process', 'commodity']
    df['variable'] = df[cols].apply(lambda row: '|'.join(row.values.astype(str)), axis=1)
    df.drop(['process', 'commodity'], axis=1, inplace=True)
    print(df)
    df_simple = pyam.IamDataFrame(df)

    print(df_simple)