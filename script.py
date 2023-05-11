from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from random import randint

token = "4tpJyVFMkkQ9mW8nFLjSStPCThvIF9ASgLpsQw8vDYEVYkttK42Z0IRZCD3X44GHiEx6aTDqMH6alHBdKhbJKw==" #Your token
org = "DevTeam"
url = "http://10.57.33.86:8087" # Your url

client = InfluxDBClient(url=url, token=token, org=org)

bucket="test"

write_api = client.write_api(write_options=SYNCHRONOUS)
   
for value in range(1000):
  
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue"+str(randint(1, 10000)))
    .field("field"+str(randint(1, 10000)), value)
  )
  write_api.write(bucket=bucket, org="DevTeam", record=point)
  print(point)