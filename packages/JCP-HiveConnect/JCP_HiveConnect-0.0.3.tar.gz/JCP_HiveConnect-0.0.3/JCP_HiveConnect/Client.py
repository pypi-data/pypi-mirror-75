import configparser
from HiveConnect import HiveConnect
import os
thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'App.ini')
appConfig = configparser.ConfigParser()
appConfig.read(initfile)
host = appConfig.get("CoreContext", "host")
username = appConfig.get("CoreContext", "user")
password = appConfig.get("CoreContext", "password")
myHive = HiveConnect(host,username,password)
data = myHive.fetch('select STORE_NBR, REGION_CD, DISTRICT_CD, STATE_NBR, STORE_CITY, STORE_STATE_CD, STORE_POSTAL_CD from marketing.stores_data limit 2')
print(data)

