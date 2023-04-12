import requests
from db_helpers import *
from datetime import datetime
import random
import math
import json
import numpy as np
from position_helper import Position_helper as ph

import pickle
from haversine import haversine
from datetime import timedelta
import pandas as pd

class Mock_Service:

    @classmethod
    #Convert user key-in address to start and end long lat, return a list with long & lat
    def matchLocationToLatLng(self,data):
        #json format-startLocation,endLocation
        final_info = []
        pick_up_info = ph.get_position_address_info(data['startLocation'])
        drop_off_info = ph.get_position_address_info(data['endLocation'])
        if len(pick_up_info)>=2 and len(drop_off_info)>=2:
            final_info.append(pick_up_info[0])
            final_info.append(drop_off_info[0])
            final_info.append(pick_up_info[1])
            final_info.append(drop_off_info[1])
            
        if final_info and len(final_info)==4:
            return final_info
        else:
            list = [
                ('103.77306074465929', '103.84606404435159','1.3055810931553957', '1.2909247436596356'),
                ('103.84606404435159', '103.84044929736973','1.2964639690580968', '1.421210263478729'),
                ('103.85011812607583', '103.83387870486484','1.2964639690580968', '1.3437726777593682')
            ]
            index = random.randrange(3)
            return list[index]

    @classmethod
    def mockSearch(self,data):
        today = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        #pickup_long, dropoff_long, pickup_lat, dropoff_lat
        lng1,lng2,lat1,lat2=  self.matchLocationToLatLng(data)

        ## TO BE EDITTED - Need to change the USER ID logic according to cognito table###
        DB_Connector.insert_request_data(['USER00002',lat1,lng1,lat2,lng2 , today])

        requestId = DB_Connector.get_request_id()

        DB_Connector.insert_p2p_request(['GRAB',lat1,lng1,lat2,lng2 ,today, requestId[0]])
        DB_Connector.insert_p2p_request(['GOJEK',lat1,lng1,lat2,lng2 ,today, requestId[0]])
        DB_Connector.insert_p2p_request(['TADA',lat1,lng1,lat2,lng2 ,today, requestId[0]])

        basefare = random.uniform(4, 6)
        #calculate distance between pick and drop off, and generate an add-up fare based on the distance
        dic_result = self.haversineDist(lng1,lng2,lat1,lat2)
        fare1, fare2, fare3 = [basefare + random.uniform(2, 4) * dic_result for _ in range(3)]
        baseEta = math.floor(basefare)*2
        eta1, eta2, eta3 = [baseEta + random.uniform(0, 2) for _ in range(3)]

        requestRecord = DB_Connector.get_p2p_req_id(requestId)
        app_list=['GRAB','GOJEK','TADA']
        for i in range(len(requestRecord)):
            DB_Connector.insert_p2p_response((requestRecord[i][0], app_list[i], '227', 'JUSTGRAB', fare1, eta1, 'grab link', today))

        result =  {
            'pickupLat': lat1,
            'pickupLng': lng1,
            'dropoffLat': lat2,
            'dropoffLng': lng2, 
            'grab': {
                'fare': round(fare1, 2),
                'eta': round(eta1, 0),
            },
            'gojek': {
                'fare': round(fare2, 2),
                'eta': round(eta2, 0),
            },
            'tada': {
                'fare': round(fare3, 2),
                'eta': round(eta3, 0),
            },
        }
        return json.dumps(result)

    @classmethod
    def mockPredict(self): 

        result = None 

        # get relevant data from db
        requestId = DB_Connector.get_request_id()
        requestRecord = DB_Connector.get_request_record(requestId)

        request_df = pd.DataFrame(data=requestRecord, columns=[
            'REQ_ID','USER_ID','PICKUP_LAT',
            'PICKUP_LONG','DROPOFF_LAT',
            'DROPOFF_LONG','CRT_DT'
        ])

        ## preprocess dataframe with different time dimensions
        mytest_df = self.timeDimension(request_df)
        distance_km = self.haversineDist(request_df['PICKUP_LONG'][0],request_df['DROPOFF_LONG'][0],request_df['PICKUP_LAT'][0],request_df['DROPOFF_LAT'][0])
        #add haversine distance to df
        mytest_df['distance_km'] = distance_km

        # call OneHot encoder from S3
        unr_one = 'https://app-storage01.s3.ap-southeast-1.amazonaws.com/model_predict/Onehot_Grab_v2.pkl'
        responseOH = requests.get(unr_one)
        if responseOH.status_code == 200:
            oneHot = pickle.loads(responseOH.content)
            mytest = oneHot.transform(mytest_df[['day_of_week','weekend']])
            onehot_df = pd.DataFrame(mytest, columns = oneHot.get_feature_names_out())#?? or use .get_feature_names() in old version
            mytest_df = pd.concat([mytest_df,onehot_df],axis=1)
            mytest_df = mytest_df.drop(['day_of_week','weekend'],axis=1)
            mytest_df = mytest_df[['distance_km','year','month','day','hour','minute',
            'day_of_week_Monday',
            'day_of_week_Saturday',
            'day_of_week_Sunday',
            'day_of_week_Thursday',
            'day_of_week_Tuesday',
            'day_of_week_Wednesday',
            'weekend_1']]
        else:
            print('got error when get the One Hot pkl file')

        #load model pkl file, call DT Model from S3
        url_rf = 'https://app-storage01.s3.ap-southeast-1.amazonaws.com/model_predict/Model_DT_Grab_v2.pkl'
        responseRF = requests.get(url_rf)
        if responseRF.status_code == 200:
            RFModel = pickle.loads(responseRF.content)
            predicted_grab = RFModel.predict(mytest_df)
            predicted_gojek = predicted_grab + np.random.randn(2).round(2)
            predicted_tada = predicted_grab + np.random.randn(2).round(2)
        else:
            print('got error when get the RF Model pkl file')

        result =  {
                'grab': {
                    'fare': round(predicted_grab[0], 2)
                },
                'gojek': {
                    'fare': round(predicted_gojek[0], 2)
                },
                'tada': {
                    'fare': round(predicted_tada[0], 2)
                },
            }

        #insert final result into PREDICT_T 
        DB_Connector.insert_predict((requestId, predicted_grab[0].item(), requestRecord[0][-1]))
        DB_Connector.insert_predict((requestId, predicted_gojek[0].item(), requestRecord[0][-1]))
        DB_Connector.insert_predict((requestId, predicted_tada[0].item(), requestRecord[0][-1]))

        return json.dumps(result)

    # calculate distance by using this function
    @classmethod   
    def haversineDist(self,pickup_long, dropoff_long, pickup_lat, dropoff_lat):
        pick_up = (float(pickup_lat),float(pickup_long))
        drop_off = (float(dropoff_lat), float(dropoff_long))
        final_distance = haversine(pick_up, drop_off)
        return final_distance

    #get time dimensions such as year, month etc.
    @classmethod
    def timeDimension(self,df):
        #add n minutes to current time
        df['CRT_DT'] = pd.to_datetime(df['CRT_DT']) + timedelta(minutes=10) #??

        #add different time dimensions
        df_processed = pd.DataFrame()
        df_processed['year'] = pd.to_datetime(df['CRT_DT']).dt.year
        df_processed['month'] = pd.to_datetime(df['CRT_DT']).dt.month
        df_processed['day'] = pd.to_datetime(df['CRT_DT']).dt.day
        df_processed['day_of_week'] = pd.to_datetime(df['CRT_DT']).dt.day_name()
        df_processed['hour'] = pd.to_datetime(df['CRT_DT']).dt.hour
        df_processed['minute'] = pd.to_datetime(df['CRT_DT']).dt.minute

        #weekend indicator
        if df_processed['day_of_week'][0] == "Saturday" or df_processed['day_of_week'][0] == "Sunday":
            df_processed['weekend'] = 1
        else: 
            df_processed['weekend'] = 0

        return df_processed
    
    # need to modify further
    # #define P2P_API_REQ_ID
    # P2P_API_REQ_ID = P2P_API_REQ['P2P_API_REQ_ID'].loc[(P2P_API_REQ['REQ_ID']==REQ_ID) & (P2P_API_REQ['CARR']=='GRAB')][0]

    # #locate corresponding fare returned from API
    # actual_fare = P2P_API_RESP['FARE'].loc[P2P_API_RESP['P2P_API_REQ_ID']==P2P_API_REQ_ID][0]

    # #return final string
    # if predicted_price[0]> actual_fare:
    #     print('The price will surge in the next 10 minutes.')
    # elif predicted_price[0] < actual_fare:
    #     print('The price will dip in the next 10 minutes.')
    # else:
    #     print('The price will stay the same in the next 10 minutes.')