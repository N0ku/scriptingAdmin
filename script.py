import influxdb_client, platform, time, socket, psutil

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from random import randint

if(platform.system() != "Darwin"):
  import clr
  clr.AddReference(r'OpenHardwareMonitor/OpenHardwareMonitorLib')
  from OpenHardwareMonitor.Hardware import Computer # import the .dll ( DONT WORK ON MAC )

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

def sendData(pointName, tagName, fieldName, fieldValue):
  point = (
    Point(pointName)
    .tag(tagName, socket.gethostname())
    .field(fieldName, int(fieldValue))
  )
  write_api.write(bucket=buckeţ, org=org, record=point)


c = Computer()
c.CPUEnabled = True
c.GPUEnabled = True
c.Open()

token = "k3vbvIGPdyGJa1q3baR5ygN9KCK_T0km5plhDLWIFWpmxoY_WnV79X-l63WBe-EDn7PkNG63sCPLlkhAH78G7w=="
org = "UwU"
url = "http://192.168.165.39:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
buckeţ = "Test"
write_api = write_client.write_api(write_options=SYNCHRONOUS)

while True:
  if(platform.system() != "Darwin"):
    mesure = updateTemperature()
    if(mesure[0] != None):
      sendData("Computer", "CPU", "Temperature", mesure[0])
    sendData("Computer", "GPU", "Temperature", mesure[1])

  sendData("Computer", "Memory", "Usage", psutil.virtual_memory().percent)
  sendData("Computer", "CPU", "Usage", psutil.cpu_freq().current)
  sendData("Computer", "Disk", "Usage", psutil.disk_usage('/').percent)
  time.sleep(1)
