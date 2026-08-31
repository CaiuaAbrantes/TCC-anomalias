from influxdb_client_3 import InfluxDBClient3
import os
from dotenv import load_dotenv

load_dotenv()

def get_client():
    return InfluxDBClient3(
        host=os.getenv("INFLUX_URL"),
        token=os.getenv("INFLUX_TOKEN"),
        database=os.getenv("INFLUX_DATABASE")
    )