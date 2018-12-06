#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import math
from operator import itemgetter
from statistics import mode
from scipy.stats import mode


# In[2]:


dataTrain = np.genfromtxt('DataTrain_Tugas3_AI.csv', delimiter=",")
dataTest = np.genfromtxt('DataTest_Tugas3_AI.csv', delimiter=",")

dataTest = np.delete(dataTest, (0), axis=0)
dataTrain = np.delete(dataTrain, (0), axis=0)


# In[3]:


dataValidasi = []
dataTrainValidasi = []
for i in range (200) :
    dataValidasi.append(dataTrain[i])
for item in range (200, 800, +1) :
    dataTrainValidasi.append(dataTrain[item])
# pd.DataFrame(dataValidasi, columns=["data ke-","X1","X2","X3","X4","X5","Y"])


# In[4]:


def euclideanDistance(x1,x2) :
    return math.sqrt(math.pow((x2[1]-x1[1]),2) + math.pow((x2[2]-x1[2]),2) + math.pow((x2[3]-x1[3]),2) + math.pow((x2[4]-x1[4]),2) + math.pow((x2[5]-x1[5]),2))


# In[5]:


def knnFunction(k, tes, train) :
    temp = []
    distance = []
    #lakukan brute force tiap 1 data tes ke semua data train
    for item in range (len(tes)) :
        for i in range (len(train)) :
            temp.append(item + 1)
            temp.append(euclideanDistance(tes[item], train[i]))
            temp.append(int(train[i][6]))
            distance.append(temp)
            temp = []
    distance = np.array(distance)
    
    #untuk memisahkan array pada data ke - i
    #ini yang tampil nanti pd.DataFrame(arr[199], columns=["Data test ke - ","Nilai euclidean","Klasifikasi"])
    i = 1
    arr = []
    while i <=  len(tes) :
        arr.append(distance[distance[:,0] == i])
        i += 1
    
    #untuk mengurutkan array berdasarkan nilai euclid
    # ini yang tampil nanti pd.DataFrame(arSort[199], columns=["Data test ke - ","Nilai euclidean","Klasifikasi"])
    arSort = []
    for n in range (len(tes)) :
        arSort.append(sorted(arr[n], key=itemgetter(1)))
    
    #mengambil k nilai terkecil
    #ini yang tampil nanti pd.DataFrame(arrKNN[199], columns=["Data test ke - ","Nilai euclidean","Klasifikasi"])
    arrKNN = []
    temp = []
    for i in range (len(tes)) :
        for n in range (k) :
            temp.append(arSort[i][n])
        arrKNN.append(temp)
        temp = []
    
    #mengambil kolom klasifikasi
    temp = []
    klasifikasiClass = []
    for i in range (len(tes)) :
        for n in range (k) :
            temp.append(arrKNN[i][n][2])
        klasifikasiClass.append(mode(temp))
        temp = []
        
    return klasifikasiClass


# In[6]:


def cariNilaiK(dataValidasi, dataTrainValidasi) :
    hmm = []
    j = 0
    arrayDataValidasi = []
    for i in range (len(dataValidasi)) :
        s = knnFunction(i+1, dataValidasi, dataTrainValidasi)
        hmm.append(i+1)
        for item in range (len(dataValidasi)) :
            if s[item][0] == dataValidasi[item][6] :
                j += 1
        hmm.append(j)
        arrayDataValidasi.append(hmm)
        hmm = []
        j = 0
        
    nilaiMaks = (max(arrayDataValidasi, key=itemgetter(1)))
    return nilaiMaks


# In[7]:


#data train di split menjadi 10 bagian
j = 0
arrayValidasi = []
while j < 800 :
    dataValidasi = []
    dataTrainValidasi = []
    for i in range (j, j+80, +1) :
        dataValidasi.append(dataTrain[i])
    for i in range (j) :
        dataTrainValidasi.append(dataTrain[i])
    for item in range (j+80, 800, +1) :
        dataTrainValidasi.append(dataTrain[item])
    arrayValidasi.append(cariNilaiK(dataValidasi, dataTrainValidasi))
    j += 80


# In[8]:


pd.DataFrame(arrayValidasi)


# In[9]:


k = max(arrayValidasi, key=itemgetter(1))
print (k[0])


# In[10]:


klasifikasiArray = knnFunction(k[0], dataTest, dataTrain)
kalsifikasiArray = np.array(klasifikasiArray)


# In[11]:


np.savetxt("TebakanTugas3.csv",[x[0] for x in klasifikasiArray],delimiter=",")

