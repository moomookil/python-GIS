# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:35:19 2017

@author: Brian
"""

import sys,csv


NaN=float('NaN')
  
def isNaN (n):
    return n!=n

#recreate the printf function without relying on futurisms
def printf(str, *args):
    sys.stdout.write(str % args)
    #sys.stdout.flush()

#return a subset of a dictionary from a list of desired keys
def getDictCols(dict,cols):
    return {k:dict[k] for k in cols}
    
# make the constant (without numpy)
NaN=float('NaN')
 
 #Parsenums (simplified for comma-free required, and only floats desired)
def parseNums(x):
    try:
        return float(x)
    except:
        return NaN

#Convert all "NULL"s to blanks w/o creating a whole new dictionary
#modify in-place elements of the the dictionary rather than creating a whole new one
#We could have used a dictionary comprehension if we wanted to return a New dictionary
#but that creates a data dependent memory footprint, the cost is a performance hit since
#all cells are updated, even ones that do not need it.
#def Nulls_To_Blanks(row):
#      map(lambda (k,v) : row.update({k:"" if v=="NULL" else v}),dict.iteritems(row))
###This version is better as it does not perform unecessory updates and
###Note the use of filter since map builds a return value that can be prevented with filter and False
def Nulls_To_Blanks(row):
      filter(lambda (k,v) : row.update({k:""}) if v=="NULL" else False ,dict.iteritems(row))      
#This version returns a new copy with values changed as needed
#def Nulls_To_Blanks(Row):
#    return {(k,("" if v=="NULL" else v)) for (k,v) in dict.iteritems(Row)} 

#use parse_Nums to convert a list of named columns into Numbers
def Numify_Columns(Row,Columns):
    for column in Columns:
        Row[column]=parseNums(Row[column])      

#read through the file with a _generator_ row-by-row memory usage rather than list creation
#(or pandas dataframe creation)

            
#################### START
#Constants and Globals
FILE='c:/Users/Brian/Downloads/MERGED2014_15_PP.csv'
OUTFILE='c:/Users/Brian/Downloads/filter.csv'

NumCols = ['TUITFTE'
,'SAT_AVG'
,'ADM_RATE'
,'COSTT4_A'
,'UGDS'
,'DEBT_MDN'
,'LONGITUDE'
,'LATITUDE'
]
OutCols=[
'STABBR'
,'CITY'
,'INSTNM'
,'TUITFTE'
,'SAT_AVG'
,'ADM_RATE'
,'COSTT4_A'
,'UGDS'
,'DEBT_MDN'
,'LONGITUDE'
,'LATITUDE'
]
missing = 0
KCount=0
roose = 0.0
data=open(FILE, 'rU')
reader = csv.DictReader(data)
data_out=open(OUTFILE,'wb')
#dw = csv.DictWriter(data_out, delimiter=',',quoting=csv.QUOTE_MINIMAL, fieldnames=reader.fieldnames)
dw = csv.DictWriter(data_out, delimiter=',',quoting=csv.QUOTE_MINIMAL,fieldnames=OutCols )
dw.writer.writerow(dw.fieldnames)

#dw.writerow(dict((fn,fn) for fn in reader.fieldnames)) 
Columns=["NPT4"+str(x)+"_PRIV" for x in range(1,6)]  
for idx,Row in enumerate (reader):
    
    #printf('\b\b\b\b\b\b\b\b\b%d',idx)
    #if Row["STABBR"] != "IL":
    #    continue
    #Private Not-for-Profit
    if not Row["CONTROL"]=="2":
        continue
    #If it has the same Canegie Classification     
    if not (Row["CCBASIC"]=="18" or  Row["CCBASIC"]=="19"):
        continue  
     
    #Nulls_To_Blanks(Row)
    Numify_Columns(Row,Columns)
     
        
    '''
    #######Note that the pythony way below,
    #######with lists, maps, zips, comprehensions,
    #######is the more awkward way
    #Get Elements of the Dictionary from the Column names in Columns
    #Equality test removes NaNs
    #We could have used 'False' instead of NaN but we preserved our parseNums function this way
    Vals=filter(lambda y: y==y, [Row[x] for x in Columns])
    ValCount=len(Vals)
    #If there are at least 2 prices to compare
    #and If any latter one is greater than an earlier one
    if ValCount>1 and 0<len(filter(lambda (x,y): y-x, zip(Vals[:-1],Vals[1:]))):
    '''
    Vals=[Row[name] for name in Columns]    
   
    if Vals!=sorted(Vals): 
        Numify_Columns(Row,NumCols)
        if Row['INSTNM'] == 'Roosevelt University':
            roose = Row['TUITFTE'] 
        
        if isNaN(Row['INEXPFTE']) or isNaN(Row['SAT_AVG']) or isNaN(Row['ADM_RATE']) or isNaN(Row['COSTT4_A']) or isNaN(Row['UGDS'] or isNaN(Row['DEBT_MDN']) 
            or isNaN(Row['LONGITUDE']) or isNaN(Row['LATITUDE'])):
            missing += 1
            
        else:
            if roose >= Row['TUITFTE'] * .8 and roose <= Row['TUITFTE'] * 1.2:
                dw.writerow(getDictCols(Row,OutCols))
                                                                    
    else:       
        KCount+=1
   
data_out.close()
#data_out=NaN
data.close()

print "Roosevelt Compare", roose
print "KCount", KCount 
print "Missing", missing
