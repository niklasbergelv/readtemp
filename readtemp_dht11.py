#!/usr/bin/env python3

import board
import adafruit_dht
import random
import logging
import time

MAX_NUMBER_OF_FAILED_READINGS = 10
SLEEP_BETWEEN_READINGS = 2

def getrandomvalue(min, max):
    logging.debug(f"getrandomvalue, min:{min}, max:{max}")
    return random.uniform(min, max)

def readvalues(number_of_readings=1):
    logging.debug(f"readvalues, number of readings: {number_of_readings}")
    avg_temp = None
    avg_hum = None
    try:
        dhtDevice = adafruit_dht.DHT11(board.D18)
        failed_readings = 0
        readings = []
        while True:
            try:
                # temp = getrandomvalue(15, 24)  # dhtDevice.temperature
                temp = dhtDevice.temperature
                # hum = getrandomvalue(29,33)  # dhtDevice.humidity
                hum = dhtDevice.humidity
                logging.debug(f"read values, temperature:{temp}, humidity:{hum}")
                if (temp is not None) and (hum is not None):
                    readings.append((temp, hum))
                    logging.debug(f"readings-append, temp: {temp}, hum: {hum}")
                    logging.debug(f"number of readings: {len(readings)}")
                    failed_readings = 0
                    if len(readings) == number_of_readings:
                        logging.debug(f"Number of succesful readings: {len(readings)}, time to break")
                        break
                else:
                    failed_readings += 1
                    if failed_readings > MAX_NUMBER_OF_FAILED_READINGS:
                        raise Exception(f"Number of failed readings above MAX_NUMBER_OF_FAILED_READINGS: "
                                        f"{MAX_NUMBER_OF_FAILED_READINGS}")

                time.sleep(SLEEP_BETWEEN_READINGS)

            except RuntimeError as error:
                # Errors happens fairly often, DHT's are hard to read, just keep going
                logging.error(error.args[0])
                time.sleep(SLEEP_BETWEEN_READINGS)
                continue

            except Exception as error:
                dhtDevice.exit()
                raise error

        dhtDevice.exit()

        xtotal = 0
        ytotal = 0
        for x, y in readings:
            xtotal += x
            ytotal += y

        avg_temp = xtotal / len(readings)
        avg_hum = ytotal / len(readings)

    except:
        logging.error("An exception occurred")

    logging.info(f"average readings returned, temperature:{avg_temp}, humidity:{avg_hum}")



    return avg_temp, avg_hum

def main():
    logging.basicConfig(filename="readtemp_dht11.log", filemode="w", level=logging.DEBUG, format='%(asctime)s %(message)s')
    temperature, humidity = readvalues(10)
    print(f"temperature: {temperature}, humidity: {humidity}")

if __name__ == "__main__":
    main()
