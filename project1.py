# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:17:07 2017

@author: Brian
"""

import csv
import matplotlib.pyplot as plt
from collections import OrderedDict

NaN=float('NaN')
 
def parseNums(x):
    try:
        return float(x)
    except:
        return NaN
    
def Numify_Columns(Row,Columns):
    for column in Columns:
        Row[column]=parseNums(Row[column])    
 
def Aggregate(Row):

    if Row["SAT_AVG"] != Row["SAT_AVG"] or Row["ADM_RATE"] != Row["ADM_RATE"] or Row["COSTT4_A"] != Row["COSTT4_A"] or Row["DEBT_MDN"] != Row["DEBT_MDN"]:    
        return 

    School=Row["INSTNM"] 
    
    SAT[School]= Row["SAT_AVG"]   
    ADM[School]= Row["ADM_RATE"]    
    COST[School] = Row["COSTT4_A"]
    DEBT[School] = Row["DEBT_MDN"]
    
def read_school_data(path):
    with open(path, 'rU') as data:
        reader = csv.DictReader(data)
        for row in reader:
            yield row
            
FILE='c:/Users/Brian/Downloads/filter.csv'
SAT = {}
ADM = {}
COST = {}
DEBT = {}
debtcostratio = {}

for Row in read_school_data(FILE):
    Numify_Columns(Row,("SAT_AVG", "ADM_RATE","COSTT4_A","DEBT_MDN"))
    Aggregate(Row)
    
debtcostratio= dict([(x, DEBT[x]/(COST[x]))  for x in COST.keys()])


SAT = OrderedDict(sorted(SAT.items(), cmp = lambda x,y: cmp(x[0],y[0])))
ADM = OrderedDict(sorted(ADM.items(), cmp = lambda x,y: cmp(x[0],y[0])))

plt.close('all')

plt.subplot(121)
plt.scatter(SAT.values(), ADM.values(), s = 75, color = 'g')
for i, txt in enumerate(SAT.keys()):
    plt.annotate(txt, (SAT.values()[i],ADM.values()[i]))
ax = plt.gca()
ax.set_axis_bgcolor('honeydew')
plt.title('SAT_AVG vs ADM_RATE')
plt.xlabel('SAT_AVG')
plt.ylabel('ADM_RATE')

plt.subplot(122)
plt.plot([x+0.1 for x in range(0,len(debtcostratio))],debtcostratio.values(), color = 'deeppink')
plt.bar([x+0.1 for x in range(0,len(debtcostratio))],debtcostratio.values(), color = 'firebrick')
ax = plt.gca()
ax.set_axis_bgcolor('azure')
plt.title('% of Debt for Cost of Attendance')
plt.xticks([x+0.1 for x in range(0,len(debtcostratio))],debtcostratio.keys(),rotation=270, fontsize=8)
plt.tight_layout()
plt.show()