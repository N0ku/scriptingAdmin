import os
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

BUCKET = "test"
ORG = "DevTeam"
token = os.getenv("INFLUX_TOKEN")
# Store the URL of your InfluxDB instance
url="https://us-east-1-1.aws.cloud2.influxdata.com"

client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=ORG
)

write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
write_api.write(bucket=BUCKET, org=ORG, record=p)

query_api = client.query_api()

query = 'from(bucket:"my-bucket")\
|> range(start: -10m)\
|> filter(fn:(r) => r._measurement == "my_measurement")\
|> filter(fn:(r) => r.location == "Prague")\
|> filter(fn:(r) => r._field == "temperature")'

result = query_api.query(org=ORG, query=query)

results = []
for table in result:
  for record in table.records:
    results.append((record.get_field(), record.get_value()))

print(results)