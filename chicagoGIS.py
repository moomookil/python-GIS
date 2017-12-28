# -*- coding: utf-8 -*-
"""
Created on Tue Dec 05 19:40:30 2017

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
 
# setup Lambert Conformal basemap.
# set resolution=None to skip processing of boundary datasets.
plt.figure(figsize=(30,30))
#m = Basemap(width=12000000,height=9000000,projection='lcc',
#            resolution='l',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)

#SEE http://matplotlib.org/basemap/api/basemap_api.html
m = Basemap(llcrnrlon=-87.95,llcrnrlat=41.6,urcrnrlon=-87.49,urcrnrlat=42.05,
        projection='lcc',lat_1=40,lat_2=40.02,lon_0=-87.9)   
m.readshapefile('C:/Users/Brian/Downloads/chicagoGIS/chicagoGIS/chcgo', name='Neighborhoods', drawbounds=True)                 
# collect the state names from the shapefile attributes so we can
# look up the shape obect for a state by it's name
hood_names = []
for shape_dict in m.Neighborhoods_info:
    hood_names.append(shape_dict['community'])
ax = plt.gca() # get current axes instance

#seg = m.Neighborhoods[hood_names.index('EDGEWATER')]
#poly = Polygon(seg, facecolor= (0, 1, 0, 0.3),edgecolor='y',zorder=1)
#ax.add_patch(poly) 

to_plot = ["EDGEWATER", "BEVERLY", "CLEARING","PARK"]
poly = []; name = []
for coordinates, region in zip(m.Neighborhoods, m.Neighborhoods_info):
    if any(substr in region["community"] for substr in to_plot):
        poly.append(Polygon(coordinates,facecolor='#006400', edgecolor='#787878', lw=0.25, alpha=0.5))
        #Find the average as an estimate of the shape center
        #x=sum([x[0] for x in coordinates])/len(coordinates)
        x=min([x[0] for x in coordinates])
        
        y=sum([y[1] for y in coordinates])/len(coordinates)
        plt.text(x,y, region["community"],fontsize=10)
        name.append(region["community"])
        
# Turn polygons into patches using descartes
patches = []
for p in poly:
    ax.add_patch(p) 
#m.shadedrelief()
#overlay a translucent white mask
#m.drawlsmask(land_color=(1,1,1,0.5),ocean_color=(0,0,0,0),lakes=True)

#http://matplotlib.org/api/markers_api.html
plt.show()