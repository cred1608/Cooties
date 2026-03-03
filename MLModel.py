#second part of the STEM project
#bring in the packages we are using
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
#new package for machine learning
from sklearn.tree import DecisionTreeRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor



#setting the info to read from the csv file
columns = ['DATE', 'TMAX', 'TMIN', 'PRCP']
#creating a variable to hold the info we read from the file named df
df = pd.read_csv("input.csv", usecols=columns)
#print the contents to a console window
#print("Contents in csv file:\n", df)
df = df.dropna()
#removes the dashes from the dates
df['DATE'] = df['DATE'].str.replace('-','')
#setting Date as the data used to predict weather
inDate = df['DATE']
#turning the Data to a numpy array to be able to use it easier
inDateArray = np.array(inDate.values)
#turning the array into a 2d array
inDateArray = inDateArray.reshape(-1,1)
#print("Contents in csv file:\n", df)
#setting the data predicted to be the Temp and rain
outData = df.drop(columns = ['DATE'])
#turning the Data to a numpy array to be able to use it easier
outDataArray = np.array(outData.values)
#print(inDate)

#make our prediction and results a function
def Date_Weather(Date):
    #make a model to teach
    model = RandomForestRegressor(max_depth = 10, random_state = 5)
    #set data for the model to learn
    model.fit(inDateArray,outData)

    #predict the weather for the date below
    prediction = model.predict([[Date]])
    #print(prediction)
    #make a new array thats a single array from the 2d array
    flat_prediction = prediction.flatten()
    #print(flat_prediction)
    #set all the values in the single array to only two decimals in length
    num_prediction = [round(numeric_string,2) for numeric_string in flat_prediction]

    #check size of array
    sizeofarray = len(num_prediction)
    #print(sizeofarray)

    #format array to match input format setting the second and third variable
    #in the array to one decimal point
    num_prediction[1] = round(num_prediction[1],1)
    num_prediction[2] = round(num_prediction[2],1)
    #print(num_prediction)
    #return the formatted prediction value to wherever it was called
    return num_prediction
#test the method/function we just made.

