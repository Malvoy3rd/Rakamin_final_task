# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 08:53:38 2022

@author: avifa
"""
import numpy as np
import pandas as pd
import glob
import os
import collections


df1 = pd.read_csv('D:/仕事-Kerjaan/Intern Rakamin/Final Task/home-credit-default-risk/application_test.csv')
df2 = pd.read_csv('D:/仕事-Kerjaan/Intern Rakamin/Final Task/home-credit-default-risk/application_train.csv')
Ndf1 = df1['SK_ID_CURR'].count()
Target = np.empty(Ndf1) ; Target.fill(2)
df1.insert(1,"TARGET",Target,True)

RAW_DATASET = df2.append(df1)

PREVIOUS_DATASET = pd.read_csv('D:/仕事-Kerjaan/Intern Rakamin/Final Task/home-credit-default-risk/previous_application.csv')
CLEAR_PREVIOUS_DATASET = PREVIOUS_DATASET.drop_duplicates(subset=['SK_ID_CURR','NAME_CONTRACT_TYPE', 'NAME_CONTRACT_STATUS'])
test1 = CLEAR_PREVIOUS_DATASET[(CLEAR_PREVIOUS_DATASET.NAME_CONTRACT_TYPE == 'Revolving loans') & (CLEAR_PREVIOUS_DATASET.NAME_CONTRACT_STATUS == 'Approved')] #Locate who has approved revolving loans
# print([item for item, count in collections.Counter(test1['SK_ID_CURR']).items() if count > 1]) #make sure SK_ID_ISN'T Duplicated
test2 = CLEAR_PREVIOUS_DATASET[(CLEAR_PREVIOUS_DATASET.NAME_CONTRACT_TYPE == 'Revolving loans') & (CLEAR_PREVIOUS_DATASET.NAME_CONTRACT_STATUS != 'Approved')] #Locate who has not approved revolving loans
#cause there must be duplicates, so erase the duplicate SK_ID_CURR
Temp = test2.drop_duplicates(subset=['SK_ID_CURR'])
ID_NAPP_RELV = Temp.SK_ID_CURR
ID_APP_RELV = test1.SK_ID_CURR


APP_PREV_DATA = PREVIOUS_DATASET[PREVIOUS_DATASET['NAME_CONTRACT_STATUS']=='Approved']
NOTAPP_PREV_DATA = PREVIOUS_DATASET[PREVIOUS_DATASET['NAME_CONTRACT_STATUS']!='Approved']
C_APP_PREV_DATA = APP_PREV_DATA.drop_duplicates(subset=['SK_ID_CURR'])
N_APP_PREV_DATA = C_APP_PREV_DATA['SK_ID_CURR'].count()

NCal = APP_PREV_DATA[APP_PREV_DATA['NAME_CONTRACT_TYPE']=='Cash loans']['SK_ID_CURR'].count()
NCol = APP_PREV_DATA[APP_PREV_DATA['NAME_CONTRACT_TYPE']=='Consumer loans']['SK_ID_CURR'].count()
NRel = APP_PREV_DATA[APP_PREV_DATA['NAME_CONTRACT_TYPE']=='Revolving loans']['SK_ID_CURR'].count()
NXNA = APP_PREV_DATA[APP_PREV_DATA['NAME_CONTRACT_TYPE']=='XNA']['SK_ID_CURR'].count()

print(NCal,NCol,NRel,NXNA)
#NRel/(NCal+NCol+NRel)*100 #percentage approved revolving loan


#APP_PREV_DATA['SK_ID_CURR'].count()/PREVIOUS_DATASET['SK_ID_CURR'].count()*100 #percentage approved

dTARGET = C_APP_PREV_DATA[~C_APP_PREV_DATA.SK_ID_CURR.isin(test1.SK_ID_CURR)]
dTARGET = dTARGET[~dTARGET.SK_ID_CURR.isin(Temp.SK_ID_CURR)]
dTARGET = RAW_DATASET[RAW_DATASET.SK_ID_CURR.isin(dTARGET.SK_ID_CURR)]
Age = abs(round(dTARGET.DAYS_BIRTH/(30*12)))
dTARGET.insert(7,"AGE",Age,True)
n25 = dTARGET[dTARGET['AGE'].between(20,25)]['AGE'].count()
n35 = dTARGET[dTARGET['AGE'].between(26,35)]['AGE'].count()
n45 = dTARGET[dTARGET['AGE'].between(36,45)]['AGE'].count()
n55 = dTARGET[dTARGET['AGE'].between(46,55)]['AGE'].count()
n65 = dTARGET[dTARGET['AGE'].between(56,65)]['AGE'].count()
n70 = dTARGET[dTARGET['AGE'].between(66,70)]['AGE'].count()
print(n25,n35,n45,n55,n65,n70)

prod_dTARGET = dTARGET[dTARGET['AGE'].between(25,45)]
notowncar_prod_dTARGET = prod_dTARGET[prod_dTARGET['FLAG_OWN_CAR']=='N']
notownhf_prod_dTARGET = prod_dTARGET[prod_dTARGET['FLAG_OWN_REALTY']=='N']
maxincome_prod_dTARGET = max(prod_dTARGET['AMT_INCOME_TOTAL'])
minincome_prod_dTARGET = min(prod_dTARGET['AMT_INCOME_TOTAL'])
occup_prod_dTARGET = [item for item, count in collections.Counter(prod_dTARGET['OCCUPATION_TYPE']).items() if count >= 1]

#PREVIOUS_DATASET.drop_duplicates(subset=['SK_ID_CURR'])['SK_ID_CURR'].count()/RAW_DATASET['SK_ID_CURR'].count()*100 # YANG TELAH APPLY DI PREVIOUS APPS
#N_APP_PREV_DATA/RAW_DATASET.SK_ID_CURR.count()*100

# REF_PREV_DATA = PREVIOUS_DATASET[PREVIOUS_DATASET['NAME_CONTRACT_STATUS']=='Refused']
# C_REF_PREV_DATA = REF_PREV_DATA.drop_duplicates(subset=['SK_ID_CURR'])
# N_REF_PREV_DATA = C_REF_PREV_DATA['SK_ID_CURR'].count()

# CAN_PREV_DATA = PREVIOUS_DATASET[PREVIOUS_DATASET['NAME_CONTRACT_STATUS']=='Canceled']
# C_CAN_PREV_DATA = CAN_PREV_DATA.drop_duplicates(subset=['SK_ID_CURR'])
# N_CAN_PREV_DATA = C_CAN_PREV_DATA['SK_ID_CURR'].count()

# UNO_PREV_DATA = PREVIOUS_DATASET[PREVIOUS_DATASET['NAME_CONTRACT_STATUS']=='Unused offer']
# C_UNO_PREV_DATA = UNO_PREV_DATA.drop_duplicates(subset=['SK_ID_CURR'])
# N_UNO_PREV_DATA = C_UNO_PREV_DATA['SK_ID_CURR'].count()

#import collections
#print([item for item, count in collections.Counter(df3['SK_ID_CURR']).items() if count > 1]) # To see if it's there a duplicate data