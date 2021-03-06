import numpy as np
import pandas as pd
import matplotlib.pyplot as mat
import networkx as nx

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

part = part[(part.attendance != 0) | (part['nb.repeat'] == 0)]
print(part.shape)


#print(part.iloc[:, 5:7])
#part = part[part.eq(part.iloc[:, 5:7]).all(1)]

part = part[part.eq(part.iloc[:, 5], axis=0).iloc[:, 5:33].all(1) == 0]
print(part.shape)

np_matr = np.asmatrix(part.iloc[:,2:33], np.int)

# корреляции
#========================================================================================================
corr = np.corrcoef(np.transpose(np_matr))
print(corr.shape[1])
for i in range(corr.shape[0]):
    for j in range(corr.shape[1]):
        if (corr[i,j] < 0.8):
            corr[i,j] = 0
        if (corr[i,j] >= 0.8):
            corr[i,j] = 1

Graph = nx.from_numpy_matrix(corr)
cliques_list = list(nx.find_cliques(Graph))
#nx.draw_circular(Graph)
np.savetxt("corr_cliques.csv", cliques_list, delimiter=";", fmt='%s')
#=========================================================================================================

#частоты
#=========================================================================================================
freq = np.zeros([5, np_matr.shape[1]], float )
for i in range(np_matr.shape[0]):
    for j in range(np_matr.shape[1]):
        freq[np_matr[i,j]-1,j] = freq[np_matr[i,j]-1,j] + (1 / np_matr.shape[0])
freq = np.transpose(freq)
np.savetxt("freqs.csv", freq, delimiter=";", fmt='%.3f')

xx= np.arange(1,31,1)
yy = np.arange(0,1,0.05)
mat.plot(range(31), freq[:, 0], 'o', color='black', label='1')
mat.plot(range(31), freq[:, 1], 'o', color='red', label='2')
mat.plot(range(31), freq[:, 2], 'o', color='yellow', label='3')
mat.plot(range(31), freq[:, 3], 'o', color='blue', label='4')
mat.plot(range(31), freq[:, 4], 'o', color='green', label='5')
mat.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
mat.xticks(xx)
mat.yticks(yy)
mat.show()

#=========================================================================================================
#print(np.average(corr[:,1]))

average = np.mean(np_matr[:, :np_matr.shape[1]], axis = 1)
#print(average.shape)

dispersion = np.var(np_matr[:, :np_matr.shape[1]], axis = 1)
#print(dispersion)

fig = mat.figure()
mat.hist(average)
mat.grid(True)
#mat.show()


#corr[:, 36] = dispersion

np.savetxt("corr_arr.csv", corr, delimiter=';', fmt='%.3f')

np.savetxt("our_class.csv", part, delimiter=';', fmt='%.3f')
