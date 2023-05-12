import psutil
from influxdb_client import InfluxDBClient,Point
import time


INFLUXDB_MEASUREMENT = 'system_info'

def write_to_influxdb(cpu_percent, free_memory,free_space,bytes_sent,bytes_received,packets_sent,packets_received):
    # Create InfluxDB client
    client = InfluxDBClient(url="http://192.168.165.10:8086", token="k3vbvIGPdyGJa1q3baR5ygN9KCK_T0km5plhDLWIFWpmxoY_WnV79X-l63WBe-EDn7PkNG63sCPLlkhAH78G7w==", org="UwU")

    # Write data to InfluxDB
    point =  Point("Computer").field("cpu_percent",cpu_percent).field("free_memory",free_memory).field("free_space",free_space)
    point2 = Point("Computer").field("bytes_received",bytes_received).field("bytes_sent",bytes_sent).field("packets_sent",packets_sent).field("packets_received",packets_received)

    client.write_api().write(bucket="Computer",org="UwU",record=point)
    client.write_api().write(bucket="Computer",org="UwU",record=point2)
    # Close InfluxDB client connection
    client.close()

def get_system_info():
    # Get CPU percentage and memory information
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    free_memory = memory.available / (1024 ** 2)  # Convert to MB
    disk_usage = psutil.disk_usage("/")
    free_space = disk_usage.free  / (1024*1024*1024)
    network_info = psutil.net_io_counters()
    bytes_sent = network_info.bytes_sent
    bytes_received = network_info.bytes_recv
    packets_sent = network_info.packets_sent
    packets_received = network_info.packets_recv
    print(f"CPU: {cpu_percent} %")
    print(f"Free Memory: {free_memory} MB")

    # Write to InfluxDB
    write_to_influxdb(cpu_percent, free_memory,free_space,bytes_sent,bytes_received,packets_sent,packets_received)

while True:
    get_system_info()
    time.sleep(1)