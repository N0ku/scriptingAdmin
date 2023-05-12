# use https://github.com/prometheus/client_python#exporting-to-a-pushgateway for all pip installation
from prometheus_client import start_http_server, Summary, Gauge
# import random
import time
import sys
import psutil

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
@REQUEST_TIME.time()
def process_request(t):
    time.sleep(t)
    if(psutil.sensors_battery().percent > 30):
        print(str(psutil.sensors_battery().percent) + "% de batterie")
    else:
        print(str(psutil.sensors_battery().percent) + "% de batterie. Faudrait commencer à recharger.")

CPU_PERCENT = Gauge('cpu_percent', 'Percentage of the cpu active')
CPU_PERCENT.set(psutil.cpu_percent(interval=2))

MEMORY_USED = Gauge('memo_used', 'Memory used')
MEMORY_USED.set(psutil.virtual_memory().percent) 

BATTERY_LEFT = Gauge('battery_left', 'Percent of battery you have')
BATTERY_LEFT.set(psutil.sensors_battery().percent)

# prom = PrometheusConnect("http://demo.robustperception.io:9090/", True)
# prom.all_metrics()

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    f= open("prometheus_data.txt","w+")
    f.write("CPU usage in percent Memory used in percent Battery left in percent \r")
    while True:
        process_request(int(sys.argv[1]))
        f.write(str(CPU_PERCENT._value.get())+"%   \r "+str(MEMORY_USED._value.get())+"%   \r "+str(BATTERY_LEFT._value.get())+"%  \r")
        # f.write("CPU usage in percent \r")
        # f.write(str(CPU_PERCENT._value.get())+"% \r\n")
        # f.write("Memory used in percent \r")
        # f.write(str(MEMORY_USED._value.get())+"% \r\n")
        # f.write("Battery left in percent \r")
        # f.write(str(BATTERY_LEFT._value.get())+"% \r\n")



