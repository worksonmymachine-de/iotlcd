from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from time import sleep
import asyncio
from json.decoder import JSONDecoder
from paho.mqtt import subscribe
from paho.mqtt.client import MQTTMessage

def safe_exit(signum, frame):
    exit(1)


class Display:
    def __init__(self):
        self.lcd = LCD()
        self.line1 = None
        self.line2 = None
        self.temp = None
        self.hum = None
        self.topic_hum = "/sensor/raw/bedroom/hum/"
        self.topic_temp = "/sensor/raw/bedroom/temp/"
        self.topic_date_time = "/info/time/day_time/"
        self.mqtt_server = "192.168.188.37"

    async def query_data(self):
        print("query")
        subscribe.callback(callback=self.callback, topics=[self.topic_date_time, self.topic_hum, self.topic_temp], hostname=self.mqtt_server)
        
    def callback(self, client, userdata, message):
        print(f"callback from topic {message.topic}")
        if message.topic == self.topic_date_time:
            self.line1 = str(bytes.decode(message.payload))
            print(self.line1)
        if message.topic == self.topic_hum:
            self.hum = JSONDecoder().decode(bytes.decode(message.payload))["hum"]
            print(self.hum)
        if message.topic == self.topic_temp:
            self.temp = JSONDecoder().decode(bytes.decode(message.payload))["temp"]
            print(self.temp)
        if self.hum is not None and self.temp is not None:
            self.line2 = f"{self.temp} C Hum:{self.hum}%"
        if self.line1 is not None and self.line2 is not None:
            self.lcd.text(self.line1, 1)
            self.lcd.text(self.line2, 2)
        
    async def run(self):
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        self.lcd.text(">>Init sensor!<<", 1)
        self.lcd.text("......wait......", 2)
        sleep(1)
        while True:
            await self.query_data()
            
if __name__ == "__main__":
    asyncio.run(Display().run())
    lcd.text("....shutdown....", 1)
    lcd.text("......bye!......", 2)
    sleep(1)
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    lcd.clear()




