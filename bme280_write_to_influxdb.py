#!/usr/bin/python
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import time
import smbus2
import bme280

# BME280 sensor address (default address)
address = 0x76

# Initialize I2C bus
bus = smbus2.SMBus(1)

# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)

measurementString = "my_measurement"
location = "Hall"
fieldTemp = "temperature"
fieldMoist = "moisture"
fieldPressure = "pressure"
bucket = "climate"
org = "Habanero"

token = "GKMzKxEOMJv8_iVdp7UUQ3DjoRJvpu2MBlRu3dWWMGbTHb84rmX85RAthmOWuKwdv9QQq6JyM7JVYNNV8cqCDw=="

# Store the URL of your InfluxDB instance
url="http://192.168.68.101:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

try:

    # Read sensor data
    data = bme280.sample(bus, address, calibration_params)

    # Extract temperature, pressure, and humidity
    temperature = data.temperature
    pressure = data.pressure
    humidity = data.humidity

    # Write script
    write_api = client.write_api(write_options=SYNCHRONOUS)

    points_dict = [{"measurement":measurementString, "tags":{"location":location},"fields":{fieldTemp : temperature, 
                                                                                            fieldMoist : humidity, 
                                                                                        fieldPressure : pressure}}]
    write_api.write(bucket, org, points_dict)

except Exception as e:
    print('An unexpected error occurred:', str(e))