from prometheus_client import start_http_server, Summary, Gauge
import time
import sys
import psutil

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds',
                       'Time spent processing request')


@REQUEST_TIME.time()
def process_request(t):
    time.sleep(t)
    print(CPU_PERCENT._value.get())


CPU_PERCENT = Gauge('cpu_percent', 'Percentage of the cpu active')

MEMORY_USED = Gauge('memo_used', 'Memory used')

BATTERY_LEFT = Gauge('battery_left', 'Percent of battery you have')

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    f = open("prometheus_data.txt", "w+")
    f.write("CPU usage in percent Memory used in percent Battery left in percent \r")
    while True:
        process_request(int(sys.argv[1]))
        CPU_PERCENT.set(psutil.cpu_percent())
        MEMORY_USED.set(psutil.virtual_memory().percent)
        BATTERY_LEFT.set(psutil.sensors_battery().percent)
        f.write(str(CPU_PERCENT._value.get())+"%                 "+str(MEMORY_USED._value.get()
                                                                       )+"%                  "+str(BATTERY_LEFT._value.get())+"%  \r")
