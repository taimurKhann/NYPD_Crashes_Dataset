import folium 
import pandas as pd
import pymongo as pm
import math
from constants import MONGO_CLIENT_HOST

#Connecting to Mongodb
mongoClient = pm.MongoClient(MONGO_CLIENT_HOST)
db = mongoClient.mydb

crashes_data = pd.DataFrame(db.Crashes_Collection.find())
stations_data = pd.DataFrame(db.Stations_Collection.find())

#Crashes List
LAT=list(crashes_data['latitude'])
LON=list(crashes_data['longitude'])
BOROUGH=list(crashes_data['borough'])
STREET=list(crashes_data['on_street_name'])


borough_list = {"MANHATTAN":'green',"QUEENS":'blue',"BROOKLYN":'red',"BRONX":'darkgreen',"STATEN ISLAND":'purple'}


fg = folium.FeatureGroup('Bicyle Stations')
fg_manhattan = folium.FeatureGroup('Manhattan')
fg_queens = folium.FeatureGroup('Queens')
fg_brooklyn = folium.FeatureGroup('Brooklyn')
fg_bronx = folium.FeatureGroup('Bronx')
fg_staten_island = folium.FeatureGroup('Staten Island')

br_counts = {"MANHATTAN":0,"QUEENS":0,"BROOKLYN":0,"BRONX":0,"STATEN ISLAND":0}
br_fg_list = {"MANHATTAN":fg_manhattan,"QUEENS":fg_queens,"BROOKLYN":fg_brooklyn,"BRONX":fg_bronx,"STATEN ISLAND":fg_staten_island}
for lt,ln,br,st in zip(LAT,LON,BOROUGH,STREET):
	if not math.isnan(lt) and not math.isnan(ln) and br != '' and br_counts[br] <= 500:
		br_counts[br] += 1
		br_fg_list[br].add_child(folium.Marker(location=[lt,ln],popup="lt:"+str(lt)+" ln:"+str(ln)+"Street:"+str(st),icon=folium.Icon(color=borough_list[br])))

#Stations List
LAT=list(stations_data['latitude'])
LON=list(stations_data['longitude'])

for lt,ln in zip(LAT,LON):
	fg.add_child(folium.Marker(location=[lt,ln],popup="lt:"+str(lt)+" ln:"+str(ln),icon=folium.Icon(color='black',icon='bicycle',prefix='fa')))

map=folium.Map(location=[40.770042,-73.93057],zoom_start=7)

for key, value in br_fg_list.items():
	map.add_child(value)

map.add_child(fg)
folium.LayerControl().add_to(map)
map.save('/var/www/html/index.html')



