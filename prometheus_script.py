# use https://github.com/prometheus/client_python#exporting-to-a-pushgateway for all pip installation
import prometheus_client
# import random
import time
import sys
import psutil

# Create a metric to track time spent and requests made.
REQUEST_TIME = prometheus_client.Summary(
    'request_processing_seconds',
    'Time spent processing request'
)


@REQUEST_TIME.time()
def process_request(t):
    time.sleep(t)

    CPU_PERCENT = prometheus_client.Gauge(
        'cpu_percent', 'Percentage of the cpu active')
    CPU_PERCENT.set(psutil.cpu_percent(interval=2))

    MEMORY_USED = prometheus_client.Gauge('memo_used', 'Memory used')
    MEMORY_USED.set(psutil.virtual_memory().percent)

    BATTERY_LEFT = prometheus_client.Gauge(
        'battery_left', 'Percent of battery you have')
    BATTERY_LEFT.set(psutil.sensors_battery().percent)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    prometheus_client.start_http_server(8000)
    # Generate some requests.
    while True:
        process_request(int(sys.argv[1]))
