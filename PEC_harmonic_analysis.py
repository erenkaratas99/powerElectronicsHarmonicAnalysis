# -*- coding: utf-8 -*-

#Copyright : Eren Karataş
#Linkedin : erenkaratass
#Github : erenkaratas99
#GSM : 0539 642 32 27

import math
import pandas as pd

def createIndexList(n):
    tempIndexes = []
    for i in range(1,n+1,2):
        tempIndexes.append(i)
    return tempIndexes

def listFreq(n,init_freq):
    tempFreqs = []
    for i in range(1,n+1,2):
        tempFreqs.append(i*init_freq)
    return tempFreqs

def listVn(n,V_DC):
    tempVns = []
    for i in range(1,n+1,2):
        tempVns.append(round((4*V_DC)/(i*math.pi),2))
    return tempVns

def listImpedence(n,freq,R,L): #R : Ohm , L : Henry
    tempZ = []
    for i in range(1,n+1,2):
        tempZ.append(round(math.sqrt(R**2+(i*2*math.pi*freq*L)**2),2))
    return tempZ
    
def listCurrent(n,ZList,VnList):
    tempCurrent = []
    if len(ZList) == len(VnList):
        for i in range(len(VnList)):
            tempCurrent.append(round(VnList[i]/ZList[i],2))
        return tempCurrent
    else:
        for i in range(1,n+1,2):
            tempCurrent.append('NaN')
        return tempCurrent

def listPower(R,listIn):
    tempPower = []
    for i in range(len(listIn)):
        tempPower.append(round(((listIn[i]/math.sqrt(2))**2)*R,2))
    return tempPower

def returnTHD_v(Vdc):
    numerator = math.sqrt(Vdc**2- (4*Vdc/(math.sqrt(2)*math.pi)))
    denominator = (4*Vdc/(math.sqrt(2)*math.pi))
    THD = numerator/denominator
    return THD*100        

def returnTHD_i(listIns):
    temp = []
    for i in range(1,len(listIns)):
        temp.append(listIns[i])
    temp = [(each/math.sqrt(2))**2 for each in temp]
    numerator = math.sqrt(sum(temp))
    denominator = listIns[0]/math.sqrt(2)
    THD_i = numerator/denominator
    return THD_i*100

listOFreqs = listFreq(9,60) #enter f (frequency)
df_Freqs = pd.DataFrame(listOFreqs)

listOIndexes = createIndexList(9)
df_indexes = pd.DataFrame(listOIndexes)

listOVns = listVn(9,400) #enter Vdc
df_Vn = pd.DataFrame(listOVns)

listOZ = listImpedence(9,60,10,0.025) #enter f (frequeny), R (ohm), L (Henry)
df_Z = pd.DataFrame(listOZ)

listOIn = listCurrent(9,listOZ,listOVns) 
df_In = pd.DataFrame(listOIn)

listOP = listPower(10,listOIn) #enter R (ohm)
df_P = pd.DataFrame(listOP)


main = pd.concat([df_indexes, df_Freqs, df_Vn, df_Z, df_In, df_P], axis=1) 
main.columns = ['n', 'f (Hz)', 'Vn (V)', 'Z (omega)', 'In (A)' , 'P (w)']
main.set_index('n',inplace=True)
print(main)

THD_V = returnTHD_v(400)
print("\nTHD_V : {}%".format(round(THD_V,3))) #THD for voltage
THD_I = returnTHD_i(listOIn)
print("\nTHD_I : {}%".format(round(THD_I,3))) #THD for current
