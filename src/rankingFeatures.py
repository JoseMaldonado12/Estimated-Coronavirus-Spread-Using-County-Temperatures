# Finding correlations and ranking features 

import numpy as np 
import pandas as pd 
from sklearn.linear_model import LassoCV

# Preparing training and testin data
data = np.genfromtxt('final.csv', delimiter = ",")
#data = np.delete(data, 6, 1)
#data = np.delete(data, 5, 1)
#data = np.delete(data, 4, 1)
features = ["Latitude", "Longitude", "Elevation", "Temperature", "WindSpeed", "Rain"]

X = data[1:data.shape[0]-1, 1:7]
Y = data[1:data.shape[0]-1, 7:8]
tr = int(X.shape[0]*0.8)
te = X.shape[0] - tr
Xtr = X[0:tr]
Xte = X[tr:tr+te]
Ytr = Y[0:tr]
Yte = Y[tr:tr+te]

# Using LassoCV to find coef of important features
# We get coef of the importance in relation to the target
lcv = LassoCV().fit(Xtr, Ytr)
importance = np.abs(lcv.coef_)
coef = {}
for i in range(6):
    coef[features[i]] = importance[i]
coef1 = sorted(coef.items(), key=lambda x: x[1], reverse=True)
for (f,c) in coef1:
    #print("Feature:", f, "\nCoef:", c)
    pass
ranking1 = ["Latitude", "Temperature", "Rain", "Longitude", "Wind Speed", "Elevation"]
'''
Feature: Latitude 
Coef: 0.02152277460760391
Feature: Temperature 
Coef: 0.01048501111894712
Feature: Rain 
Coef: 0.0011337726939069585
Feature: Longitude 
Coef: 0.0007183706504282805
Feature: WindSpeed 
Coef: 2.1580535226731523e-05
Feature: Elevation 
Coef: 1.2414793809479373e-05
'''

# Using Pandas correlation
# Positive number means positive relation, nevative number means negative relation
# Higher the number, higher the relation
data1 = pd.read_csv("final.csv", sep = ",")
cor = data1.corr()
ranking2 = ["Temperature", "Longitude", "Rain", "Wind Speed", "Elevation", "Latitude"]
'''
                Latitude    Longitude  Elevation  Temperature  Windspeed   Rain     Growth %
Latitude        1.000000     0.281789   0.091905    -0.756511  -0.001808 -0.057583 -0.002971
Longitude       0.281789     1.000000  -0.333725    -0.266655  -0.040929 -0.120775  0.053067
Elevation       0.091905    -0.333725   1.000000    -0.119441   0.144285  0.048483 -0.009103
Temperature    -0.756511    -0.266655  -0.119441     1.000000  -0.015703  0.001107 -0.177541
Windspeed      -0.001808    -0.040929   0.144285    -0.015703   1.000000 -0.023887 -0.017797
Rain           -0.057583    -0.120775   0.048483     0.001107  -0.023887  1.000000  0.051253
Growth %       -0.002971     0.053067  -0.009103    -0.177541  -0.017797  0.051253  1.000000
'''

# Finding variance of features
variance = X.var(axis = 0)

for i in range(6):
    print("Feature", features[i], "\nVariance:", round(variance[i],3))
ranking3 = ["Temperature", "Rain", "Latitude", "Elevation", "Wind Speed", "Longitude"]

'''
Feature Latitude 
Variance: 474.218
Feature Longitude 
Variance: 21.512
Feature Elevation 
Variance: 266.062
Feature Temperature 
Variance: 98302.3
Feature WindSpeed 
Variance: 135.293
Feature Rain 
Variance: 56032.569
'''

'''
Out of the 3 rankings, Temperature, Rain and Latitude seem to be ranking high. 
It is possible that these 3 are the features that affect the growth % the most.
We will try training on these 3 features alone, the other 3 features and then on all features
and make comparison.
'''