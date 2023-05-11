import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

import clr
clr.AddReference(r'OpenHardwareMonitor/OpenHardwareMonitorLib')

from OpenHardwareMonitor.Hardware import Computer

c = Computer()
c.CPUEnabled = True
c.GPUEnabled = True
c.Open()

gpuTemp = 0
cpuTemp = 0

while True:
    for a in range(0, len(c.Hardware[0].Sensors)):
        if "/temperature" in str(c.Hardware[0].Sensors[a].Identifier):
            cpuTemp = c.Hardware[0].Sensors[a].get_Value()
            c.Hardware[0].Update()

    for a in range(0, len(c.Hardware[1].Sensors)):
        if "/temperature" in str(c.Hardware[1].Sensors[a].Identifier):
            gpuTemp = c.Hardware[1].Sensors[a].get_Value()
            c.Hardware[1].Update()

    print("CPU : {}°C   |   GPU : {}°C".format(cpuTemp, gpuTemp))

token = "k3vbvIGPdyGJa1q3baR5ygN9KCK_T0km5plhDLWIFWpmxoY_WnV79X-l63WBe-EDn7PkNG63sCPLlkhAH78G7w=="
org = "UwU"
url = "http://10.57.33.40:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

