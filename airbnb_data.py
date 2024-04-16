import pandas as pd
import pymongo
 
   



client=pymongo.MongoClient("mongodb+srv://suryasadasivamm:Surya0807@guvi.yn6kwzt.mongodb.net/?retryWrites=true&w=majority&appName=guvi")
Vb=client["sample_airbnb"]
col=Vb["listingsAndReviews"]

primary_table=[]
for i in col.find({},{"_id":1,'listing_url':1,'name':1,'property_type':1,'room_type':1,'bed_type':1,
                        'minimum_nights':1,'maximum_nights':1,'cancellation_policy':1,'accommodates':1,
                        'bedrooms':1,'beds':1,'number_of_reviews':1,'bathrooms':1,'price':1,
                        'cleaning_fee':1,'extra_people':1,'guests_included':1,'images.picture_url':1,
                        'review_scores.review_scores_rating':1,'amenities':1}):
  primary_table.append(i)
  
Table=pd.DataFrame(primary_table)
Table["images"]=Table['images'].apply(lambda x: x["picture_url"])
Table["review_scores"]=Table["review_scores"].apply(lambda x: x.get("review_scores_rating",0))
Table.info()
Table.describe()
Table.isnull().sum()

Table['bedrooms'].fillna(0, inplace=True)
Table['beds'].fillna(0, inplace=True)
Table['bathrooms'].fillna(0, inplace=True)
Table['cleaning_fee'].fillna('Not Specified', inplace=True)

Table.isnull().sum()

Table["minimum_nights"]=Table["minimum_nights"].astype(int)
Table["maximum_nights"]=Table["maximum_nights"].astype(int)
Table["bedrooms"]=Table["bedrooms"].astype(int)
Table["beds"]=Table["beds"].astype(int)
Table["bathrooms"]=Table["bathrooms"].astype(str).astype(float).astype(int)
Table["price"]=Table["price"].astype(str).astype(float).astype(int)
Table["cleaning_fee"]=Table["cleaning_fee"].apply(lambda x:int(float(str(x)))if x!="Not Specified" else "Not Specified")
Table["extra_people"]=Table["extra_people"].astype(str).astype(float).astype(int)
Table["guests_included"]=Table["guests_included"].astype(str).astype(int)

host = []
for i in col.find( {}, {'_id':1, 'host.host_name':1,'host.host_identity_verified':1,'host.host_id':1}):
    host.append(i)
host_table=pd.DataFrame(host)
host_table["host_id"]=host_table['host'].apply(lambda x: x["host_id"])
host_table["host_identity_verified"]=host_table['host'].apply(lambda x: x["host_identity_verified"])
host_table["host_name"]=host_table['host'].apply(lambda x: x["host_name"])
host_table.drop("host",axis=1,inplace=True)

host_table['host_identity_verified'] = host_table['host_identity_verified'].map({False:'No',True:'Yes'})
host_table.isnull().sum()
host_table.info()




address=[]
for i in col.find( {}, {'_id':1,'address':1}):
    address.append(i)
address_table=pd.DataFrame(address)

address_table["street"]=address_table['address'].apply(lambda x: x["street"] if x["street"]!='' else "Not Specified" )
address_table["suburb"]=address_table['address'].apply(lambda x: x["suburb"] if x["suburb"]!='' else "Not Specified" )
address_table["government_area"]=address_table['address'].apply(lambda x: x["government_area"] if x["government_area"]!='' else "Not Specified" )
address_table["market"]=address_table['address'].apply(lambda x: x["market"] if x["market"]!='' else "Not Specified" )
address_table["country"]=address_table['address'].apply(lambda x: x["country"] if x["country"]!='' else "Not Specified")
address_table["country_code"]=address_table['address'].apply(lambda x: x["country_code"] if x["country_code"]!='' else "Not Specified")
address_table["location_type"]=address_table['address'].apply(lambda x: x["location"]["type"])
address_table["longitude"]=address_table['address'].apply(lambda x: x["location"]["coordinates"][0] if x["location"]["coordinates"][0]!='' else "Not Specified")
address_table["latitude"]=address_table['address'].apply(lambda x: x["location"]["coordinates"][1] if x["location"]["coordinates"][1]!='' else "Not Specified")
address_table["is_location_exact"]=address_table['address'].apply(lambda x: x["location"]["is_location_exact"] if x["location"]["is_location_exact"]!='' else "Not Specified")

address_table.drop('address',axis=1,inplace=True)
address_table['is_location_exact'] =address_table['is_location_exact'].map({False:'No',True:'Yes'})


availability=[]
for i in col.find( {}, {'_id':1,'availability':1}):
    availability.append(i)
availability_table=pd.DataFrame(availability)

availability_table["availability_30"]=availability_table['availability'].apply(lambda x: x["availability_30"] if x["availability_30"]!='' else 0 )
availability_table["availability_60"]=availability_table['availability'].apply(lambda x: x["availability_60"] if x["availability_60"]!='' else 0 )
availability_table["availability_90"]=availability_table['availability'].apply(lambda x: x["availability_90"] if x["availability_90"]!='' else 0 )
availability_table["availability_365"]=availability_table['availability'].apply(lambda x: x["availability_365"] if x["availability_365"]!='' else 0 )

availability_table.drop("availability",axis=1, inplace =True)

Table_column=['_id', 'name', 'property_type','room_type',
       'minimum_nights', 'maximum_nights', 'cancellation_policy',
       'accommodates', 'bedrooms', 'beds', 'number_of_reviews', 'bathrooms',
       'price', 'cleaning_fee', 'extra_people', 'guests_included', 
       'review_scores','amenities','images']
host_table_column=['_id','host_name','host_identity_verified']
address_table_column=['_id', 'market', 'country', 'longitude', 'latitude']

map_table=pd.merge(Table[Table_column],host_table[host_table_column], on='_id')
map_table_1=pd.merge(address_table[address_table_column],availability_table, on='_id')
map_primary_table=pd.merge(map_table,map_table_1, on='_id')
exchange_rates = {
    'Australia': 0.73,    # 1 AUD = 0.73 USD
    'China': 0.15,        # 1 CNY = 0.15 USD
    'Hong Kong': 0.13,    # 1 HKD = 0.13 USD
    'Portugal': 1.18,     # 1 EUR = 1.18 USD
    'Spain': 1.18,        # 1 EUR = 1.18 USD
    'Canada': 0.80,       # 1 CAD = 0.80 USD
    'United States': 1.0, # 1 USD = 1.0 USD
    'Brazil': 0.19,       # 1 BRL = 0.19 USD
    'Turkey': 0.12        # 1 TRY = 0.12 USD
}
def convert_to_usd(row):
    return row['price'] * exchange_rates.get(row['country'], 1.0)

# Apply the conversion function to each row
map_primary_table['price_usd'] = map_primary_table.apply(convert_to_usd, axis=1)

map_primary_table.to_csv("Airbnb_data.csv",index=False)

map_primary_table.info()