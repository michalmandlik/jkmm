import pandas as pd

filename = "data/delay_distribution.csv"
pd.read_csv(filename, quoting=2)['delay'].hist(bins=50)
