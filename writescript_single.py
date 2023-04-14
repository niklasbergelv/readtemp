#!/usr/bin/env python3

import logging
import time
import board
import adafruit_dht
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

logging.basicConfig(filemode="a",
                    filename="writescript.log",
                    level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s",
                    datefmt="%Y-%m-%d %I:%M:%S%p"
                    )


# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D18)


bucket = "readtemp_rpi3" 
org = "Habanero"
token = "FVU8Vs_PTv3kc2Sv78OYJJsqiVZJEtxrRHG2XJnv689feCJlz_Y6hFzsdis23xlRjp6f-hLAqBxX5JKuMpSfBQ=="
# Store the URL of your InfluxDB instance
url="http://192.168.68.103:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)

continueLoop = True
numberofreadings = 5
count = 0

while continueLoop:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        if temperature_c != None and humidity != None:
            logging.info(
                "Temp: {:.1f} C    Humidity: {}% ".format(
                temperature_c, humidity
                )
            )
            write_api.write(bucket, org,[{"measurement": "dhtDevice", "tags": {"location": "vardagsrum"}, "fields": {"temperature": temperature_c, "humidity": humidity}}])
        count += 1
        if count > numberofreadings:
            continueLoop = False
            dhtDevice.exit()
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        logging.error(error.args[0])
        time.sleep(5.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(5.0)

