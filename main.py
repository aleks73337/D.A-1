import numpy as np
import pandas as pd
# import sklearn
#import matplotlib.pyplot as mpl

X = pd.read_csv("turkiye-student-evaluation_generic.csv")
gr = X.groupby(["class"])
n = 13

for name, group in gr:
    if (name == n):
        part = group
print(part.shape)
#print(part.iloc[:,5:33])
#print(part.shape)
#print(part.head(2))

part = part[part.attendance != 0]
print(part.shape)

#print(part.iloc[:, 5:7])
#part = part[part.eq(part.iloc[:, 5:7]).all(1)]

part = part[part.eq(part.iloc[:, 5], axis=0).iloc[:, 5:33].all(1) == 0]
print(part.shape)

np_matr = np.asmatrix(part.iloc[:,2:33], np.int)
corr = np.corrcoef(np.transpose(np_matr))

#print(np.average(corr[:,1]))

np.savetxt("corr_arr.csv", corr, delimiter=';', fmt='%.3f')

np.savetxt("our_class.csv", part, delimiter=';', fmt='%.3f')