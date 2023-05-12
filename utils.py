import psutil
from influxdb_client import InfluxDBClient,Point
import time


INFLUXDB_MEASUREMENT = 'system_info'

def write_to_influxdb(cpu_percent, free_memory,free_space):
    # Create InfluxDB client
    client = InfluxDBClient(url="http://10.57.33.170:8086", token="k3vbvIGPdyGJa1q3baR5ygN9KCK_T0km5plhDLWIFWpmxoY_WnV79X-l63WBe-EDn7PkNG63sCPLlkhAH78G7w==", org="UwU")

    # Write data to InfluxDB
    point =  Point("Computer").field("cpu_percent",cpu_percent).field("free_memory",free_memory).field("free_space",free_space)
    print(point)
    client.write_api().write(bucket="Computer",org="UwU",record=point)
    # Close InfluxDB client connection
    client.close()

def get_system_info():
    # Get CPU percentage and memory information
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    free_memory = memory.available / (1024 ** 2)  # Convert to MB
    disk_usage = psutil.disk_usage("/")
    free_space = disk_usage.free  / (1024*1024*1024)
    print(f"CPU: {cpu_percent}")
    print(f"Free Memory: {free_memory}")

    # Write to InfluxDB
    write_to_influxdb(cpu_percent, free_memory,free_space)

while True:
    get_system_info()
    time.sleep(1)