""""
Take a dump and convert it to a pyam.DataFrame
"""

import pyam
import pandas as pd



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