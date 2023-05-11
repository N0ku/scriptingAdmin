import influxdb_client, os, time, socket, clr
clr.AddReference(r'OpenHardwareMonitor/OpenHardwareMonitorLib')

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from OpenHardwareMonitor.Hardware import Computer # import the .dll ( may not work on mac )



def updateTemperature():
    for a in range(0, len(c.Hardware[0].Sensors)):
        if "/temperature" in str(c.Hardware[0].Sensors[a].Identifier):
            cpuTemp = c.Hardware[0].Sensors[a].get_Value()
            c.Hardware[0].Update()

    for a in range(0, len(c.Hardware[1].Sensors)):
        if "/temperature" in str(c.Hardware[1].Sensors[a].Identifier):
            gpuTemp = c.Hardware[1].Sensors[a].get_Value()
            c.Hardware[1].Update()

    print("CPU : {}°C   |   GPU : {}°C".format(cpuTemp, gpuTemp))



c = Computer()
c.CPUEnabled = True
c.GPUEnabled = True
c.Open()

token = "k3vbvIGPdyGJa1q3baR5ygN9KCK_T0km5plhDLWIFWpmxoY_WnV79X-l63WBe-EDn7PkNG63sCPLlkhAH78G7w=="
org = "UwU"
url = "http://192.168.1.39:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
buckeţ = "Test"
write_api = write_client.write_api(write_options=SYNCHRONOUS)

gpuTemp = 0
cpuTemp = 0

while True:
    updateTemperature()
    point = (
        Point("Computer")
        .tag("GPU", socket.gethostname())
        .field("Temperature", gpuTemp)
    )
    write_api.write(bucket=buckeţ, org=org, record=point)
    time.sleep(1)
