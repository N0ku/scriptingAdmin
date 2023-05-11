# use https://github.com/prometheus/client_python#exporting-to-a-pushgateway for all pip installation
from prometheus_client import start_http_server, Summary
# import random
import time
import sys

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    time.sleep(t)
    print(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        process_request(int(sys.argv[1]))