from statsd import StatsClient
import os
import random
import time

statsServer = os.environ.get('STATSD_SERVER', 'localhost:8125')
statsClient = StatsClient(host=statsServer.split(':')[0], port=8125)

def incrementCounter(metric_name):
    sample_rate = 0.1  # Adjust the sampling rate as needed
    if random.random() < sample_rate:
        statsClient.incr(metric_name)

def getTiming(metric_name, start_time):
    end_time = time.time()
    elapsed_time = end_time - start_time
    statsClient.timing(metric_name, int(elapsed_time * 1000)) 
