from sodapy import Socrata
import pymongo as pm
import pandas as pd
import utils as util
import sys
from constants import MY_APP_TOKEN, SOCRATA_URL, SOCRATA_DATASET_IDENTIFIER, SOCRATA_DATA_LIMIT, MONGO_CLIENT_HOST, WHERE_CLAUSE, MONGO_ATLAS

if __name__=="__main__":
	print("CreditShelf....")

	#Connecting to Mongodb
	mongoClient = pm.MongoClient(MONGO_CLIENT_HOST)
	db = mongoClient.mydb

	
	#client = pm.MongoClient(MONGO_ATLAS)
	#db = client.mydb

	#Connecting to Socrata for api call to cityofnewyork dataset
	client = Socrata(SOCRATA_URL, MY_APP_TOKEN)

	limit = SOCRATA_DATA_LIMIT
	offset = 0

	db.Crashes_Staging.remove({})
	db.Crashes_Collection.remove({})

	#Extracting data from api call
	results = client.get(SOCRATA_DATASET_IDENTIFIER, limit=limit, offset=offset, where=WHERE_CLAUSE)


	while results:
		db.Crashes_Staging.insert(results)
		result_df = pd.DataFrame(results)

		#converting long and lat to numeric
		result_df[["longitude","latitude"]] = result_df[["longitude","latitude"]].apply(pd.to_numeric)
		#print(result_df)


		#print(result_df.groupby("on_street_name")["latitude"].transform(lambda x: x.fillna(x.mean())))
		# Filling null borough with empty values
		result_df['borough'] = result_df['borough'].fillna('')			
	
		#missing latitude is calculated with the help of on_street_name	
		result_df['latitude'] = result_df['latitude'].fillna(result_df.groupby('on_street_name')['latitude'].transform('mean'))
		result_df['longitude'] = result_df['longitude'].fillna(result_df.groupby('on_street_name')['longitude'].transform('mean'))
		#print(result_df)

		missing_borough_df = result_df[result_df['borough']!='']
		
		points = []
		for index, row in missing_borough_df.iterrows():
		    points.append((row['latitude'],row['longitude']))

		#print(result_df[(result_df['borough']=='') & ((result_df['latitude']!=0) & (result_df['latitude'].notnull()))])

		for index, row in result_df.iterrows():
			if row['borough'] == '' and row['latitude']!=0:
				index_pos = util.closest_node((row['latitude'],row['longitude']),points)
				temp_df = result_df.loc[[index_pos],['borough']]
				#print(result_df.loc[[index],['borough','latitude','longitude']])
				for temp_index, temp_row in temp_df.iterrows():
					result_df.loc[[index],['borough']] = temp_row['borough']
				#result_df.loc[[index],['borough']] = result_df.loc[[index_pos],['borough']]
				#print(result_df.loc[[index],['borough','latitude','longitude']])

		records_df = result_df[["borough","on_street_name","longitude","latitude"]]
		#print(records_df)
		records = records_df.to_dict('records')
		#print(records)
		rd2 = result_df[(result_df['on_street_name']=="EAST 36 STREET                  ")]
		#print(rd2[['borough','on_street_name','latitude','longitude']])

		db.Crashes_Collection.insert(records)#db.Crashes_Staging.find({'longitude':{"$exists":"true"}}))
		offset += limit
		results = client.get(SOCRATA_DATASET_IDENTIFIER, limit=limit, offset=offset, where=WHERE_CLAUSE)
		

	#print(util.get_collision_list_by_borough("MANHATTAN",db).count())

