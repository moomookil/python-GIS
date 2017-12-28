# -*- coding: utf-8 -*-
"""
Created on Tue Dec 05 19:46:56 2017

@author: Brian
"""

"""
Admission Rate Code (simplified)
with GIS plotting example
Note that basemap is not in the default canopy installation
"""
from mpl_toolkits.basemap import Basemap #not in default canopy
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import csv

#SEE http://matplotlib.org/basemap/users/geography.html
#SEE https://github.com/matplotlib/basemap/tree/master/examples

plt.close('all')
FILE='c:/Users/Brian/Downloads/filter.csv'
LATLON='C:/Users/Brian/Downloads/state_latlon.csv'

def read_school_data(path):
    with open(path, 'rU') as data:
        reader = csv.DictReader(data)
        for row in reader:
            yield row

NaN=float('NaN')
 
 #Parsenums (simplified for comma-free required, and only floats desired)
def parseNums(x):
    try:
        return float(x)
    except:
        return NaN
    
#use parse_Nums to convert a list of named columns into Numbers
def Numify_Columns(Row,Columns):
    for column in Columns:
        Row[column]=parseNums(Row[column])    
Long=[]
Lat=[]
state_school = {}


for Row in read_school_data(FILE):
    Numify_Columns(Row,("LONGITUDE","LATITUDE"))
    Long.append(Row["LONGITUDE"])
    Lat.append(Row["LATITUDE"])
    state_school[Row['INSTNM']] = (Row['LONGITUDE'],Row['LATITUDE'])

state_latlon={}
state_centers=[]
for Row in read_school_data(LATLON):
    Numify_Columns(Row,("longitude","latitude"))
    state_latlon[Row["state"]]=(Row["longitude"],Row["latitude"])
   
print len(Long), len(Lat)   
# setup Lambert Conformal basemap.
# set resolution=None to skip processing of boundary datasets.
plt.figure(figsize=(30,30))
#m = Basemap(width=12000000,height=9000000,projection='lcc',
#            resolution='l',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)

#SEE http://matplotlib.org/basemap/api/basemap_api.html
m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
        projection='lcc',lat_1=33,lat_2=45,lon_0=-95)   
m.readshapefile('c:/Users/Brian/Downloads/StateShapes/StateShapes/st99_d00', name='states', drawbounds=True)                 
# collect the state names from the shapefile attributes so we can
# look up the shape obect for a state by it's name
state_names = []
for shape_dict in m.states_info:
    state_names.append(shape_dict['NAME'])

ax = plt.gca() # get current axes instance

# get Texas and draw the filled polygon
seg = m.states[state_names.index('Illinois')]
poly = Polygon(seg, facecolor= (0, 1, 1, 0.3),edgecolor='y',zorder=1)
ax.add_patch(poly)        
# draw a land-sea mask for a map background.
# lakes=True means plot inland lakes with ocean color.
m.shadedrelief()
#overlay a translucent white mask
#m.drawlsmask(land_color=(1,1,1,0.5),ocean_color=(0,0,0,0),lakes=True)

#http://matplotlib.org/api/markers_api.html
x2,y2 = (-90,15)
m.scatter(Long,Lat,latlon=True,color="red",s=20,marker='D',zorder=2)
for i, state in enumerate (state_school.keys()):
    plt.annotate(state_school.keys()[i], xy=m(state_school[state][0],state_school[state][1]),  xycoords='data',
                xytext=(x2, y2), textcoords='offset points',
                color='crimson', fontsize=10,
                arrowprops=dict(arrowstyle="fancy", color='brown'),
                )

for state in state_latlon.keys():
    x,y=m(state_latlon[state][0],state_latlon[state][1])         
    plt.text(x-1e05,y,state,fontsize=20)  

#x, y = m(-87.63,41.88)
#plt.text(x, y, '*Chicago',fontsize=20)
plt.show()