import pandas as pd

filename = '../data/100k_dataset.csv'
df = pd.read_csv(filename, iterator=True, chunksize=1000)

for chunk in df :
	print(chunk["actual_departure"][0])
 
