from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "test"

client = InfluxDBClient(url="http://localhost:8086", token="746Ify-d_159R7Hm_SVNLsok-UGdd3iMqOg9nkGmS4YBaAMNPllhI24gEYeCkbRXJhLBKxlBt0B7lzuBn-qvJQ==", org="DevTeam")

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

p = Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)

write_api.write(bucket=bucket, record=p)

## using Table structure
tables = query_api.query('from(bucket:"test") |> range(start: -10m)')

for table in tables:
    print(table)
    for row in table.records:
        print (row.values)


## using csv library
csv_result = query_api.query_csv('from(bucket:"test") |> range(start: -10m)')
val_count = 0
for row in csv_result:
    for cell in row:
        val_count += 1