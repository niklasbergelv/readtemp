#!/usr/bin/env python3

"""
    check the possiblity to make use of logger.config
"""

import sys
import readtemp_dht11
import logging
import datetime
import yaml
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

def init():
    with open("read_sensor_value_config.yml", "r") as file:
        config_values = yaml.safe_load(file)

    logging.debug(f"config_values: {config_values}")

    return config_values

def sendtoinfluxdb(bucket, org, token, url, sensorvalues):

    logging.debug(f"sendtoinfluxdb({bucket}, "
                  f"{org}, "
                  f"token_value_not_written_to_log, "
                  f"{url}, "
                  f"{sensorvalues})")

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    logging.info(f"write_api.write({bucket}, ..., "
                  f"temperature: {sensorvalues[0]}"
                  f"humidity: {sensorvalues[1]}")

    client_response = write_api.write(bucket, org, [{"measurement" : "dhtdevice",
                                   "tags": {"location" : "vardagsrum"},
                                   "fields" : {"temperature" : sensorvalues[0],
                                               "humidity" : sensorvalues[1]}}])

    if client_response is not None:
        raise Exception(f"client_response: {client_response}")
    else:
        logging.debug(f"client_response is: {client_response} as it should")

def main():
    logging.basicConfig(filename=f"read_sensor_value-{datetime.date.today()}.log", filemode="w", level=logging.DEBUG,
                        format='%(asctime)s %(message)s')
    try:
        config_values = init()

        temperature, humidity = readtemp_dht11.readvalues()
        logging.info(f"values read, temperature: {temperature}, humidity: {humidity}")
        target = config_values["target"]
        logging.debug(f"target: {target}")

        if target == "influxdb":
            influxdb_config = config_values["influxdb"]
            sendtoinfluxdb(influxdb_config["bucket"],
                           influxdb_config["org"],
                           influxdb_config["token"],
                           influxdb_config["url"],
                           (temperature, humidity))
        else:
            raise Exception(f"target: {target}, not implemented")

    except FileNotFoundError as error:
        logging.exception(f"FileNotFoundError: {error.args[0]}")
    except Exception as error:
        logging.exception(f"Exception: {error.args[0]}")
        sys.exit(error.args[0])
if __name__ == "__main__":
    main()