import influxdb_client, platform, time, socket, psutil, dotenv, os
from prometheus_client import start_http_server, Summary, Gauge

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from random import randint
from dotenv import load_dotenv

print("Starting ...")

if(platform.system() != "Darwin"):
  import clr
  clr.AddReference(r'OpenHardwareMonitor/OpenHardwareMonitorLib')
  from OpenHardwareMonitor.Hardware import Computer # import the .dll ( DONT WORK ON MAC )
  c = Computer()
  c.CPUEnabled = True
  c.GPUEnabled = True
  c.Open()

def updateTemperature():
  for a in range(0, len(c.Hardware[0].Sensors)):
      if "/temperature" in str(c.Hardware[0].Sensors[a].Identifier):
        cpuTemp = c.Hardware[0].Sensors[a].get_Value()
        c.Hardware[0].Update()

  for a in range(0, len(c.Hardware[1].Sensors)):
    if "/temperature" in str(c.Hardware[1].Sensors[a].Identifier):
      gpuTemp = c.Hardware[1].Sensors[a].get_Value()
      c.Hardware[1].Update()
    return [cpuTemp, gpuTemp]

def sendData(pointName, fieldName, fieldValue):
  point = (
    Point(pointName)
    # .tag(tagName, socket.gethostname())
    .field(fieldName, int(fieldValue))
  )
  write_api.write(bucket=buckeţ, org=org, record=point)

load_dotenv()

token = os.getenv("TOKEN")
org = os.getenv("ORG")
url = os.getenv("HOST")
buckeţ = os.getenv("BUCKET_NAME")

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

start_http_server(8000)

CPU_Temperature = Gauge('CPU_Temperature', 'CPU Temperature')
GPU_Temperature = Gauge('GPU_Temperature', 'GPU Temperature')
memory_usage = Gauge('memory_usage', 'Memory usage')
CPU_usage = Gauge('CPU_usage', 'CPU usage')
disk_usage = Gauge('disk_usage', 'Disk usage')

print("Initialization completed")
print("(i) Sending data")

while True:
  if(platform.system() == "Windows"):
    mesure = updateTemperature()
    if(mesure[0] != None):
      sendData("Computer", "CPU Temperature", mesure[0])
      CPU_Temperature.set(mesure[0])
    sendData("Computer", "GPU Temperature", mesure[1])
    GPU_Temperature.set(mesure[1])

  sendData("Computer", "Memory usage", psutil.virtual_memory().percent)
  sendData("Computer", "CPU usage", psutil.cpu_percent())
  sendData("Computer", "Disk usage", psutil.disk_usage('/').percent)

  memory_usage.set(psutil.virtual_memory().percent)
  CPU_usage.set(psutil.cpu_percent())
  disk_usage.set(psutil.disk_usage('/').percent)

  time.sleep(1)
