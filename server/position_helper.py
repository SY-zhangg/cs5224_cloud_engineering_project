import configparser
import pandas as pd
import requests
import json

class Position_helper:

    #read from config file
    # position_api_cred = configparser.RawConfigParser()
    # position_api_cred.read('credentials/position-api.credentials')
    # position_api_token = position_api_cred.get("position_api", "position_api_token")

    position_api_token = 'd2bd91704c97c44710daab267b9fdcce'

    @classmethod
    def get_position_address_info(self,pick_up):    

        api_key = self.position_api_token

        # pick_up = "501 Jln. Ahmad Ibrahim, Singapore 639937"

        base_url = 'http://api.positionstack.com/v1/forward?'+'access_key='+str(api_key)+'&query='+pick_up

        x  = None

        positionInfoLict = []
        
        try:
            # get postion info
            x = requests.get(base_url)   
            if x.status_code == 200:
                if x.content:
                    j = x.json()
                    for i in j['data']:
                        if i['country'] == 'Singapore' and i['confidence'] > 0.5:
                            positionInfoLict.append(i.get('longitude'))
                            positionInfoLict.append(i.get('latitude'))
        except Exception as e:
            print('Error:', e)
            print('get position address info failed: {}:{}'.format(
                str(pick_up)))
        
        return positionInfoLict