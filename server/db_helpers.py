import pymysql
import configparser
import time
import datetime

class DB_Connector:

    # connection to aws mysql db
    # mysqlconfig = configparser.RawConfigParser()
    # mysqlconfig.read('credentials/mysql-db.credentials')
    # mysql_db_host = mysqlconfig.get("mysql_db", "mysql_db_host")
    # mysql_db_user = mysqlconfig.get("mysql_db", "mysql_db_user")
    # mysql_db_name = mysqlconfig.get("mysql_db", "mysql_db_name")
    # mysql_db_pass = mysqlconfig.get("mysql_db", "mysql_db_pass")

    mysql_db_host = 'proddatabase-1.c8bp7i67is8n.ap-southeast-1.rds.amazonaws.com'
    mysql_db_user = 'admin'
    mysql_db_name = 'MyDatabase'
    mysql_db_pass = 'adminpw0401'

    @classmethod
    def get_mysql_connection(self):
        connection_mysql = cursor = None

        try:
            host_mysql = self.mysql_db_host
            connection_mysql = pymysql.connect(
                db=self.mysql_db_name,
                user=self.mysql_db_user,
                password=self.mysql_db_pass,
                host=host_mysql,
                charset='utf8',
                autocommit=True)

        except (Exception, pymysql.Error) as error:
            print("exception")
            print(error)

        if connection_mysql is None:
            return False
        else:
            return connection_mysql
    
    @classmethod
    def set_up_mysql_tables(self):
        mysql_db = self.get_mysql_connection()
        with mysql_db.cursor() as cursor:
            #create P2P_API_REQUEST table
            cursor.execute(
                ''' CREATE TABLE IF NOT EXISTS P2P_API_REQUEST(
                P2P_API_REQ_ID INT AUTO_INCREMENT NOT NULL,
                CARR CHAR(10),
                PICKUP_LAT CHAR(100),
                PICKUP_LONG CHAR(100),
                DROPOFF_LAT CHAR(100),
                DROPOFF_LONG CHAR(100),
                CRT_DT CHAR(100),
                REQ_ID INT,
                PRIMARY KEY (`P2P_API_REQ_ID`)
            )''')

            cursor.execute(
                ''' CREATE TABLE IF NOT EXISTS REQUEST_T(
                    REQ_ID INT AUTO_INCREMENT NOT NULL,
                    USER_ID CHAR(10),
                    PICKUP_LAT CHAR(100),
                    PICKUP_LONG CHAR(100),
                    DROPOFF_LAT CHAR(100),
                    DROPOFF_LONG CHAR(100),
                    CRT_DT CHAR(100),
                    PRIMARY KEY (`REQ_ID`)
                )''')
            
            cursor.execute(
                ''' CREATE TABLE IF NOT EXISTS P2P_API_RESP(
                    P2P_API_RESP_ID INT AUTO_INCREMENT NOT NULL,
                    P2P_API_REQ_ID INT,
                    CARR CHAR(10),
                    CARR_SERVICEID CHAR(10),
                    CARR_SERVICENM CHAR(20),
                    FARE FLOAT,
                    ETA FLOAT,
                    DEEPLINK CHAR(100),
                    CRT_DT CHAR(100),
                    PRIMARY KEY (`P2P_API_RESP_ID`)
                )''')
            
            cursor.execute(
                ''' CREATE TABLE IF NOT EXISTS PREDICT_T(
                    PREDICT_ID INT AUTO_INCREMENT NOT NULL,
                    REDIRECT_ID CHAR(50),
                    OUTCOME CHAR(255),
                    CRT_DT CHAR(100),
                    PRIMARY KEY (`PREDICT_ID`)
                )''')
            
            cursor.close()
            mysql_db.close()

        return 

    @classmethod
    def insert_request_data(self,data):
        mysql_db = self.get_mysql_connection()
        with mysql_db.cursor() as cursor:
            insertrows = {
                'USER_ID' : data[0],
                'PICKUP_LAT':data[1],
                'PICKUP_LONG' : data[2],
                'DROPOFF_LAT': data[3],
                'DROPOFF_LONG': data[4],
                'CRT_DT' : data[5]
            }
            cursor.execute("""INSERT INTO MyDatabase.REQUEST_T(USER_ID,PICKUP_LAT,PICKUP_LONG,DROPOFF_LAT, DROPOFF_LONG,CRT_DT) 
                VALUES(%(USER_ID)s,%(PICKUP_LAT)s,%(PICKUP_LONG)s,%(DROPOFF_LAT)s,%(DROPOFF_LONG)s,%(CRT_DT)s)""",insertrows)
            
            cursor.close()
            mysql_db.close()

        return 
    
    @classmethod
    def insert_p2p_request(self,data):
        mysql_db = self.get_mysql_connection()
        with mysql_db.cursor() as cursor:
            insertrows = {
                'CARR' : data[0],
                'PICKUP_LAT':data[1],
                'PICKUP_LONG' : data[2],
                'DROPOFF_LAT': data[3],
                'DROPOFF_LONG': data[4],
                'CRT_DT' : data[5],
                'REQ_ID':data[6]
            }
            cursor.execute("""INSERT INTO MyDatabase.P2P_API_REQUEST(CARR,PICKUP_LAT,PICKUP_LONG,DROPOFF_LAT,DROPOFF_LONG,CRT_DT,REQ_ID) 
                VALUES(%(CARR)s,%(PICKUP_LAT)s,%(PICKUP_LONG)s,%(DROPOFF_LAT)s,%(DROPOFF_LONG)s,%(CRT_DT)s,%(REQ_ID)s)""",insertrows)
            
            cursor.close()
            mysql_db.close()

        return 
    
    @classmethod
    def insert_p2p_response(self,data):
        mysql_db = self.get_mysql_connection()
        with mysql_db.cursor() as cursor:
            insertrows = {
                'P2P_API_REQ_ID' : data[0], #data[0]
                'CARR':data[1],
                'CARR_SERVICEID' : data[2],
                'CARR_SERVICENM': data[3],
                'FARE': data[4],
                'ETA' : data[5],
                'DEEPLINK':data[6],
                'CRT_DT':data[7]
            }
            cursor.execute("""INSERT INTO MyDatabase.P2P_API_RESP(P2P_API_REQ_ID,CARR,CARR_SERVICEID,CARR_SERVICENM,FARE,ETA,DEEPLINK,CRT_DT) 
                VALUES(%(P2P_API_REQ_ID)s,%(CARR)s,%(CARR_SERVICEID)s,%(CARR_SERVICENM)s,%(FARE)s,%(ETA)s,%(DEEPLINK)s,%(CRT_DT)s)""",insertrows)
            
            cursor.close()
            mysql_db.close()

        return
    
    @classmethod
    def insert_predict(self,data):
        mysql_db = self.get_mysql_connection()
        with mysql_db.cursor() as cursor:
            insertrows = {
                'USER_ID' : '1', #data[0]
                'PICKUP_LAT':'1',
                'PICKUP_LONG' : '1',
                'DROPOFF_LAT': '1',
                'DROPOFF_LONG': '1',
                'CRT_DT' : '1'
            }
            cursor.execute("""INSERT INTO MyDatabase.PREDICT_T(REDIRECT_ID,OUTCOME,CRT_DT) 
                VALUES(%s,%s,%s)""",data)
            
            cursor.close()
            mysql_db.close()

        return
    
    @classmethod
    def get_request_id(self):
        mysql_db = self.get_mysql_connection()
        with mysql_db.cursor() as cursor:
            cursor.execute('''SELECT MAX(REQ_ID) from MyDatabase.REQUEST_T''')
        result = cursor.fetchall()

        cursor.close()
        mysql_db.close()
        return result
    
    @classmethod
    def get_request_record(self,requestId):
        mysql_db = self.get_mysql_connection()
        with mysql_db.cursor() as cursor:
            cursor.execute("SELECT * FROM MyDatabase.REQUEST_T WHERE REQ_ID = " + str(requestId[0][0]))
        request_result = cursor.fetchall()
        
        cursor.close()
        mysql_db.close()
        return request_result
    
    @classmethod
    def get_p2p_req_id(self,requestId):
        mysql_db = self.get_mysql_connection()
        with mysql_db.cursor() as cursor:
            cursor.execute('''SELECT * from MyDatabase.P2P_API_REQUEST WHERE REQ_ID ='''+ str(requestId[0][0]))
        response_result = cursor.fetchall()

        cursor.close()
        mysql_db.close()
        return response_result