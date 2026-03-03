#end product of the first section
#name the packages we are using
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#setting some parameters for the window that will show the plot
plt.rcParams["figure.autolayout"] = True
#setting the info to read from the csv file
columns = ['DATE', 'TMAX', 'TMIN', 'PRCP']
#creating a variable to hold the info we read from the file named df
df = pd.read_csv("input.csv", usecols=columns)
#print the contents to a console window
print("Contents in csv file:\n", df)
#set to a scatter plot with the date horizontal and the temperature vertical, and the strength of the color showing the amount of percipitation
df.plot.scatter(x = 'DATE', y = 'TMAX', c = 'PRCP', colormap = 'jet', figsize=(16, 6))
#show the graph in a window from matplotlib
plt.show()
