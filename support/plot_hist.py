import pandas as pd
import time
import matplotlib.pyplot as plt

filename = "data/delay_distribution.csv"
data = pd.read_csv(filename, index_col=0)

data.plot()

plt.ylim([0,500])
plt.xlim([-3000,3000])
plt.xlabel('Delay')
plt.ylabel('Count')
plt.title('Delay distribution')

filename = "output/" + str(time.strftime("%y%m%d")) + "_" + str(time.strftime("%H%M%S")) + "_plot.png"
plt.savefig(filename)
plt.show()
